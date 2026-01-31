#!/usr/bin/env python3
import sys
import os
import re
import hashlib
import time
CHUNK_SIZE = 65536
PRINTER_PATH = "/tmp/printer"

# ------------------------------------------------------------
# STREAMING HELPERS
# ------------------------------------------------------------

def stream_detect_slicer_and_metadata(path):
    """Streaming pass: detect slicer, detect _IFS_COLORS, extract metadata lines,
       extract filament colors/types, feedrates, and capture first layer."""
    slicer = ""
    already = None
    colors = []
    types = []
    feedrates = ""
    version = "1.2.2"
    filament_colour_line = ""
    filament_type_line = ""
    filament_max_vol_line = ""
    change_filament_line = ""
    metadata_lines = {}
    first_layer_lines = []
    in_first_layer = False
    after_layer_count = 0
    tools = set()

    metadata_keys = [
        "; nozzle_temperature =",
        "; hot_plate_temp =",
        "; filament_colour =",
        "; nozzle_diameter =",
        "; filament_type =",
        "; layer_height =",
        "; estimated printing time",
        "; filament_settings_id = ",
        "; total filament length",
        "; total filament weight",
    ]

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            # Detect slicer (first 20 lines only)
            if not slicer:
                if "BambuStudio" in line:
                    slicer = "bambu"
                elif "OrcaSlicer" in line:
                    slicer = "orca"

            # Detect already processed
            if already is None and line.startswith("; _IFS_COLORS"):
                already = line.strip() + "\n"
                #break #todo - optimize this later

            # Capture metadata lines for Bambu
            if slicer != "orca":
                for key in metadata_keys:
                    if key in line and key not in metadata_lines:
                        metadata_lines[key] = line.strip()

            # Capture filament colors/types
            if line.startswith("; filament_colour ="):
                filament_colour_line = line
            if line.startswith("; filament_type ="):
                filament_type_line = line

            # Capture feedrates
            if line.startswith("; filament_max_volumetric_speed ="):
                filament_max_vol_line = line

            # Capture change_filament_gcode version - either one for now
            if version == "1.2.2" and ("less_waste:" in line or "Bambufy:" in line):    
                m = re.search(r"(less_waste:|Bambufy:)\s*v([\d.]+)", line)
                if m:
                    version = m.group(2)

            # First layer extraction using Orca markers
            if line.startswith(";AFTER_LAYER_CHANGE"):
                after_layer_count += 1
                if after_layer_count == 1:
                    in_first_layer = True
                    continue
                elif after_layer_count == 2:
                    in_first_layer = False
                    
            if in_first_layer:
                first_layer_lines.append(line)

            if line.startswith("T"):
                part = line[1:].split()[0]
                if part.isdigit():
                    tools.add(part)

    # Parse colors/types
    if filament_colour_line:
        colors = [v.strip() for v in filament_colour_line.split("=", 1)[1].split(";") if v.strip()]
    if filament_type_line:
        types = [v.strip() for v in filament_type_line.split("=", 1)[1].split(";") if v.strip()]

    # Parse feedrates
    if filament_max_vol_line:
        vals = filament_max_vol_line.split("=", 1)[1].strip().split(",")
        feedrates = ",".join(str(round(float(v) / 4 * 3 * 60)) for v in vals)

    # Build bambu metadata block
    bambu_metadata = ""
    if slicer == "bambu":
        def get_val(key):
            if key not in metadata_lines:
                return ""
            line = metadata_lines[key]
            return line.split("=", 1)[1].split(",")[0].strip()

        nozzle_temp = get_val("; nozzle_temperature =")
        bed_temp = get_val("; hot_plate_temp =")
        nozzle_diameter = metadata_lines.get("; nozzle_diameter =", "")
        filament_colour = metadata_lines.get("; filament_colour =", "")
        filament_type = metadata_lines.get("; filament_type =", "")
        layer_height = metadata_lines.get("; layer_height =", "")
        est_time = metadata_lines.get("; estimated printing time", "")
        filament_id = metadata_lines.get("; filament_settings_id = ", "")

        used_mm_line = metadata_lines.get("; total filament length", "")
        filament_used_mm = ""
        if used_mm_line:
            filament_used_mm = f"; filament used [mm] = {used_mm_line.split(':')[1].strip()}"

        used_g_line = metadata_lines.get("; total filament weight", "")
        filament_used_g = ""
        total_filament_used_g = ""
        if used_g_line:
            weights = used_g_line.split(':')[1].strip()
            filament_used_g = f"; filament used [g] = {weights}"
            total_filament_used_g = f"; total filament used [g] = {sum(float(x) for x in weights.split(','))}"

        bambu_metadata = (
            f"\n{filament_used_mm}\n"
            f"{filament_used_g}\n"
            f"{total_filament_used_g}\n"
            f"{est_time}\n"
            f"{filament_type}\n"
            f"{filament_id}\n"
            f"{layer_height}\n"
            f"{nozzle_diameter}\n"
            f"{filament_colour}\n"
            f"; first_layer_bed_temperature = {bed_temp}\n"
            f"; first_layer_temperature = {nozzle_temp}\n"
        )

    return (
        slicer,
        already,
        colors,
        types,
        feedrates,
        version,
        "".join(first_layer_lines),
        bambu_metadata,
        sorted(tools)
    )

def get_exclude_object_define_streaming(first_layer_text):
    """Compute bounding box from first layer G-code."""
    minx = miny = float("inf")
    maxx = maxy = float("-inf")

    for line in first_layer_text.splitlines():
        parts = line.split()
        if not parts:
            continue
        if parts[0] not in ("G1", "G2", "G3"):
            continue

        x = y = e = None
        for p in parts[1:]:
            if p.startswith("X"):
                x = float(p[1:])
            elif p.startswith("Y"):
                y = float(p[1:])
            elif p.startswith("E"):
                e = float(p[1:])

        if e is None or e <= 0:
            continue

        if x is not None:
            minx = min(minx, x)
            maxx = max(maxx, x)
        if y is not None:
            miny = min(miny, y)
            maxy = max(maxy, y)

    if minx == float("inf"):
        return None

    cx = (minx + maxx) / 2
    cy = (miny + maxy) / 2

    return (
        f"EXCLUDE_OBJECT_DEFINE NAME=First_Layer CENTER={cx:.4f},{cy:.4f} "
        f"POLYGON=[[{minx:.6f},{miny:.6f}],"
        f"[{maxx:.6f},{miny:.6f}],"
        f"[{maxx:.6f},{maxy:.6f}],"
        f"[{minx:.6f},{maxy:.6f}]]"
    )

# ------------------------------------------------------------
# STREAMING MD5 REWRITE
# ------------------------------------------------------------

def process_gcode_streaming_atomic(file_path, ifs_colors, bambu_metadata):
    temp_path = file_path + ".tmp"

    md5 = hashlib.md5()
    header_line = "; " + ifs_colors + "\n"
    md5.update(header_line.encode("utf-8"))

    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            md5.update(chunk)

    md5.update(bambu_metadata.encode("utf-8"))
    md5_line = "; MD5:" + md5.hexdigest() + "\n"

    with open(temp_path, "wb") as out, open(file_path, "rb") as f:
        out.write(md5_line.encode("utf-8"))
        out.write(header_line.encode("utf-8"))

        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            out.write(chunk)

        out.write(bambu_metadata.encode("utf-8"))

    try:
        os.remove(file_path)
    except OSError:
        pass

    os.rename(temp_path, file_path)

# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Use: preprint.py <file.gcode>")
        sys.exit(1)

    file_path = sys.argv[1]
    print("Parsing G-code...")
    start = time.time()
    (
        slicer,
        already,
        colors,
        types,
        feedrates,
        version,
        first_layer,
        bambu_metadata,
        tools
    ) = stream_detect_slicer_and_metadata(file_path)
    end = time.time()
    print("Complete - " + f" took {end - start:.4f} seconds")

    exclude = get_exclude_object_define_streaming(first_layer)

    ifs_colors = (
        f'_IFS_COLORS START=1 '
        f'TYPES={",".join(types)} '
        f'E_FEEDRATES={feedrates} '
        f'COLORS={",".join(c[1:] for c in colors)} '
        f'TOOLS={",".join(tools)} '
        f'VERSION={version} '
        f'EXCLUDE="{exclude}"'
    )

    if already:
        print("Already post-processed" + "\n")
        #print(already)
        with open(PRINTER_PATH, "a", encoding="utf-8") as f:
            f.write(ifs_colors + "\n")
        sys.exit(0)

    #print(ifs_colors + "\n")
    print("Generating G-code MD5...")
    start = time.time()
    process_gcode_streaming_atomic(file_path, ifs_colors, bambu_metadata)
    end = time.time()
    print("Complete - " + f" took {end - start:.4f} seconds")
    if not any(k.startswith("SLIC3R_") for k in os.environ):
        with open(PRINTER_PATH, "a", encoding="utf-8") as f:
            f.write(ifs_colors + "\n")


if __name__ == "__main__":
    main()
