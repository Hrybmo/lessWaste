# lessWaste plugin for the AD5X with ZMOD and OrcaSlicer
## Based on [bambufy](https://github.com/function3d/bambufy/tree/V1.2.10) AD5X V1.2.10
*Does not work with Bambu Studio - removed functions for a performance boost

Changes relative to bambufy:
- Start print routine
  - Reduce oozing
  - Raise bed in advance
- Start dialog
  - Backup functional
  - Purge line added
  - Layout change
- Handles large G-code
- End print routine
  - Reduce oozing
  - Purge filament that is stuck in the tube between the extruder and IFS when the reel is empty

Test conditions:
- Enabled Plugins: recommend,lessWaste
- Klipper 13
- USB camera
- zmod 1.6.5.464-24-gcead783b
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

Best used for: High levels of filament swaps.

Notes: Placing the prime tower close to the cutter area works well to reduce oozing and is required if using "No sparse layers (beta)". Use the print time and total filament used to compare between options.

### Option 2: Purge out the back
Description: Purge out the back like stock but with more control.

Pros: A small prime tower is required, less area needed on the build plate. Respects "flushing volumes".

Cons: The settings "Flush into object's infill" and "Flush into objects' support" do not reduce the purge amount (OrcaSlicer issue).

Best used for: Infrequent filament swaps where it is more efficient to build a small prime tower instead of a large one on every layer.

Notes: Use the print time and total filament used to compare between options.

## Flush volumes starting point
Set multiplier to 1, recalculate, then set any value lower than 90 to 90.

<img width="352" height="349" alt="volumes2" src="https://github.com/user-attachments/assets/f69af43d-5870-4b64-8b0a-5f2ac25c99b2" />

## Credits
- Raúl (function3d) [bambufy](https://github.com/function3d/bambufy)
- Sergei (ghzserg) [zmod](https://github.com/ghzserg/zmod)
