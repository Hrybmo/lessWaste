# WIP - BETA
Requirements
- AD5X and Orcaslicer
- using ZMOD global settings
- awesome optimization based on bambufy, focusing on purging out the back with a minimal prime tower
- might be a seperate project or pushed back depending on where this goes
- Compatability with .25 mm, .40 mm, and .6 mm nozzles
  
Whats working
- LINE_PURGE from ZMOD global setting

# lessWate AD5X
   - Compatible with Orca slicer ([3MF](https://github.com/function3d/bambufy/releases/download/v1.1.0/ArticulatedCuteTurtle_Multicolor4Color_Orca.3mf))
   - Purge sequences fully controlled by the slicer (same behavior as
   Bambu Lab printers)
   - Accurate time and material usage estimates
   - 24 mm retraction before filament cut on every color change (saves ~7
   meters of filament across 300 color changes)
   - Reduced purge multiplier (≈ 0.7) possible without color mixing in
   most prints
   - `Flush into object infill` `flush into object supports` and `flush into object`
   effectively reduce filament waste
   - **Material-to-waste ratio rarely exceeds 50%, even on 4-color prints** (0.2mm layer height, weight print > 70g)
   - **Mainsail displays true colors directly from the slicer**
   - **45 seconds color change time**
   - Bed leveling before print (Level On/Off)
   - External spool printing (IFS On/Off)
   - Backup printing mode – up to 4 kg of uninterrupted printing (Backup
   On/Off)
   - Automatic fallback when IFS runs out: the remaining filament in the
   printhead is used until the next color change
   - Filament state detection at print_start to identify the active
   filament in the extruder
   - Detection of jams, breaks and filament runout
   - Improved routine for automatic print recovery after power outages or
   errors

## How to install

- Install [zmod](https://github.com/ghzserg/zmod) following the [instructions](https://github.com/ghzserg/zmod/wiki/Setup_en#installing-the-mod)
- Change the native display to **Guppyscreen** running the `DISPLAY_OFF` command
- Change web ui to **Mainsail** running the `WEB` command
- In Mainsail, go to Machine tab, /config/mod_data/user.moonraker.conf and add the following:   
[update_manager lessWaste]   
type: git_repo   
channel: dev   
path: /root/printer_data/config/mod_data/plugins/lessWaste   
origin: https://github.com/Hrybmo/lessWaste.git   
is_system_service: False   
primary_branch: master
- Run `ENABLE_PLUGIN name=lessWaste` command from the console.
- Use MACHINE_GCODE.md for Orcaslicer settings.

## How to uninstall
- Run the `DISABLE_PLUGIN name=lessWaste` command from the console.
- (Optional) Go back to stock screen `DISPLAY_ON`
- (Optional) Go back to Fluidd `WEB`

## Credits
- Raúl (function3d) [bambufy](https://github.com/function3d/bambufy)
- Sergei (ghzserg) [zmod](https://github.com/ghzserg/zmod)
