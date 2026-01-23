# lessWaste plugin for the AD5X with ZMOD and OrcaSlicer
## Based on [bambufy](https://github.com/function3d/bambufy/tree/V1.2.10) AD5X V1.2.10
*Does not work with Bambu Studio - removed functions for a performance boost

Changes relative to bambufy:
- Start print routine
  - Reduce ooze
  - Raise bed in advance
- Start dialog
  - Full backup
  - Purge line toggle
  - Layout change
- Handles large G-code
- End print routine
  - Reduce ooze
  - Purge filament that is stuck in the tube between the extruder and IFS when the reel is empty

Test conditions:
- Enabled Plugins: recommend,lessWaste
- Klipper 13
- USB camera
- zmod 1.6.5.464-44-g60a108a0
- recommend 1.1.5-0-g1f759590
- AD5X-1.1.7-1.1.0-3.0.6-20250912-Factory firmware (Can downgrade with a flash drive. Best version IMO)
  https://github.com/ghzserg/zmod/releases/download/R/AD5X-1.1.7-1.1.0-3.0.6-20250912-Factory.tgz

This is stable but I want to put more miles and tweaks on it before proposing anything official

## How to install
- Downgrade to 1.1.7 Firmware if needed on AD5X (removes forced start routine) 
- Install [zmod](https://github.com/ghzserg/zmod) following the [instructions](https://github.com/ghzserg/zmod/wiki/Setup_en#installing-the-mod)   
- Change the native display to **Guppyscreen** running the `DISPLAY_OFF` command
- (Optional) Change web ui to **Mainsail** running the `WEB` command
- In ui, go to Machine/configuration tab, /config/mod_data/user.moonraker.conf, and add the following:   
[update_manager lessWaste]   
type: git_repo   
channel: dev   
path: /root/printer_data/config/mod_data/plugins/lessWaste   
origin: https://github.com/Hrybmo/lessWaste.git   
is_system_service: False   
primary_branch: master
- Run `ENABLE_PLUGIN name=lessWaste` command from the console (recommend should be enabled already)
- Use OrcaSlicer_GCODE.md for OrcaSlicer configuration.

## How to uninstall
- Run the `DISABLE_PLUGIN name=lessWaste` command from the console.
- (Optional) Go back to stock screen `DISPLAY_ON`
- (Optional) Go back to Fluidd `WEB`

## Creating less waste
You have two options and depending on the type of print, one may be better than the other.

### Option 1: Purge in prime tower
Description: Instead of purging out the back, a prime tower is used for purging.

Pros: The settings "Flush into object's infill", "Flush into objects' support", and "flushing volumes" are respected.

Cons: A large prime tower is generally required, taking up volume.

Best used for: Flushing into things. 

Notes: Placing the prime tower close to the cutter area works well to reduce oozing and is required if using "No sparse layers (beta)". Use the "print time" and "total filament used" to compare between options.

### Option 2: Purge out the back
Description: Purge out the back like stock but with more control.

Pros: A small prime tower is required, less area needed on the build plate. Respects "flushing volumes" when purging.

Cons: The settings "Flush into object's infill" and "Flush into objects' support" do not reduce the purge amount.

Best used for: Where it is more efficient to build a small prime tower instead of a large one on every layer.

Notes: Use the "print time" and "total filament used" to compare between options.

## Settings
### Backup
Description: If backup is enabled and there are matching filament types and color filaments, they will join. The backup locations are set on start and consumed during print. If backup is triggered during a print, the lowest available filament number is activated.

Example below: T0 does not have a backup but T2 does. If filament three runs out then filament two will automatically load and continue.

<img width="393" height="275" alt="image" src="https://github.com/user-attachments/assets/45b99d51-f7ab-459e-8a60-ea5f0dcfee8b" />

Example below: The location is empty so not available for backup. 

<img width="384" height="275" alt="image" src="https://github.com/user-attachments/assets/2d418d09-53fd-48c3-ba74-056e871fd745" />

Example below: Missing key filament so unable to start the print.

<img width="382" height="273" alt="image" src="https://github.com/user-attachments/assets/973b2448-5b69-4dfa-8d10-4c89decbc966" />

Example below: Double backups!

<img width="388" height="278" alt="image" src="https://github.com/user-attachments/assets/d09fc2c0-131d-419f-833c-8f8f543b35b2" />

### LEVELING
Description: Performs a bed mesh leveling in the print area at start.

### LINE_PURGE
Description: Creates a purge line in front or to the side of the print.

Pros: quicker than a skirt or similar primer.

### IFS
Description: With this disabled, the filament stays in the hotend from print to print.

## Flush volumes starting point
Set multiplier to 1, recalculate, then set any value lower than 90 to 90.

<img width="352" height="349" alt="volumes2" src="https://github.com/user-attachments/assets/f69af43d-5870-4b64-8b0a-5f2ac25c99b2" />

---
<div align="center">

## [❤️ Consider supporting this development ❤️](https://github.com/sponsors/Hrybmo)

</div>

## Credits
- Raúl (function3d) [bambufy](https://github.com/function3d/bambufy)
- Sergei (ghzserg) [zmod](https://github.com/ghzserg/zmod)
