# (C) 2025 ghzserg https://github.com/ghzserg/zmod/
import csv
import os
import re
import time
from pathlib import Path

try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("❌ Error: deep_translator missing. Install it with: pip install deep_translator")

def main():
    print("🚀 High-Speed Auto-Translation Started...")
    master_file = 'master_translations.csv'
    pattern = re.compile(r'===(?!=)(.*?)(?<!=)===')
    
    # Target languages for Google Translate
    lang_map = {
        'ru': 'ru', 'de': 'de', 'es': 'es', 'fr': 'fr', 
        'it': 'it', 'ja': 'ja', 'ko': 'ko', 'pt': 'pt', 
        'tr': 'tr', 'zh': 'zh-CN'
    }

    # 1. SMART PATH DETECTION
    cfg_files = list(Path('./').glob('*.cfg'))
    base_path = Path('./')
    if not cfg_files:
        cfg_files = list(Path('../').glob('*.cfg'))
        base_path = Path('../')

    print(f"📂 Scanning files in {base_path.absolute()}")

    required_tags = set()
    for cfg in cfg_files:
        with open(cfg, 'r', encoding='utf-8') as f:
            tags = pattern.findall(f.read())
            for t in tags:
                required_tags.add(t.strip())

    if not required_tags:
        print("❌ No tags found!")
        return

    # 2. LOAD/CREATE MASTER TABLE
    rows = []
    csv_keys = set()
    header = ["en"] + list(lang_map.keys())
    
    if os.path.exists(master_file):
        with open(master_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            try:
                header = next(reader)
                # Ensure header contains 'en' and matches our map
                for row in reader:
                    if row:
                        csv_keys.add(row[0].strip())
                        rows.append(row)
            except StopIteration:
                pass

    # 3. FAST BATCH TRANSLATION
    missing_tags = sorted(list(required_tags - csv_keys))
    
    if missing_tags:
        print(f"🌐 Found {len(missing_tags)} new tags. Batch translating...")
        batch_results = {lang: [] for lang in lang_map.keys()}

        for lang_header, target_code in lang_map.items():
            print(f"   Translating batch for [{lang_header}]...", end=" ", flush=True)
            try:
                translated_list = GoogleTranslator(source='en', target=target_code).translate_batch(missing_tags)
                batch_results[lang_header] = translated_list
                print("Done")
                time.sleep(0.5) 
            except Exception as e:
                print(f"Failed! ({e})")
                batch_results[lang_header] = ["" for _ in missing_tags]

        for i, tag in enumerate(missing_tags):
            new_row = [tag]
            for lang_header in lang_map.keys():
                new_row.append(batch_results[lang_header][i])
            rows.append(new_row)
        
        with open(master_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(header)
            writer.writerows(rows)
        print(f"💾 {master_file} updated.")

    # 4. EXPORT TO FOLDERS (Including English)
    print("📂 Exporting folders...")
    
    # Build the full dictionary of translations
    final_translations = {h: {} for h in header[1:]}
    for row in rows:
        en_text = row[0]
        for i, h in enumerate(header[1:]):
            if i+1 < len(row):
                final_translations[h][en_text] = row[i+1]

    # Add 'en' to the output list - it just maps key to itself
    all_output_langs = list(lang_map.keys()) + ['en']

    for lang_code in all_output_langs:
        output_dir = base_path / lang_code
        output_dir.mkdir(exist_ok=True)
        
        mapping = final_translations.get(lang_code, {})

        for cfg_file in cfg_files:
            with open(cfg_file, 'r', encoding='utf-8') as f_in:
                content = f_in.read()
            
            # For 'en', we just remove the === markers but keep the text inside
            if lang_code == 'en':
                new_content = pattern.sub(lambda m: m.group(1).strip(), content)
            else:
                new_content = pattern.sub(lambda m: mapping.get(m.group(1).strip(), f"==={m.group(1).strip()}==="), content)
            
            with open(output_dir / cfg_file.name, 'w', encoding='utf-8') as f_out:
                f_out.write(new_content)
        
        print(f"   ✅ [{lang_code}] generated.")
    
    print("\n✨ All tasks complete! Check your folders.")

if __name__ == "__main__":
    main()