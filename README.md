# lessWaste plugin for the AD5X with ZMOD and OrcaSlicer
## Based on [bambufy](https://github.com/function3d/bambufy/tree/V1.2.10) AD5X V1.2.10
## *Does not work with Bambu Studio

Changes relative to bambufy:
- Start print routine
- Start dialog
- tweaks here and there
- Large G-code parsing
- End print routine

Test conditions:
- Enabled Plugins: recommend,lessWaste,notify,timelapse
- Klipper 13
- USB camera
- zmod 1.6.6
- recommend 1.1.5
- AD5X-1.1.7-1.1.0-3.0.6-20250912-Factory firmware (Can downgrade with a flash drive. Best version IMO)
  https://github.com/ghzserg/zmod/releases/download/R/AD5X-1.1.7-1.1.0-3.0.6-20250912-Factory.tgz

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

Notes: Placing the prime tower close to the cutter area works well when using "No sparse layers (beta)". Use the "print time" and "total filament used" to compare between options.

### Option 2: Purge out the back
Description: Purge out the back like stock but with more control.

Pros: A small prime tower is required, less area needed on the build plate. Respects "flushing volumes" when purging.

Cons: The settings "Flush into object's infill" and "Flush into objects' support" do not reduce the purge amount.

Best used for: Where it is more efficient to build a small prime tower instead of a large one on every layer.

Notes: Use the "print time" and "total filament used" to compare between options.

## Settings
### Backup
Description: If backup is enabled and there are matching filament types and color filaments, they will join. The backup locations are set on start and consumed during print. If backup is triggered during a print, the lowest available filament number is activated (scans 1 -> 4). When printing, consumed channels can be refilled once there are no backups left and there is a pause.

Example below: If filament one runs out then filament two will automatically load and continue.

<img width="388" height="414" alt="image" src="https://github.com/user-attachments/assets/80828ebf-00d4-49bc-96d9-16d94ef22158" />

Example below: Double backups!

<img width="390" height="456" alt="image" src="https://github.com/user-attachments/assets/fecc7423-b68a-484b-ae93-14ecac9ef49c" />

### LEVELING
Description: Performs a bed mesh leveling in the print area at start.

### L_PURGE
Description: Creates a purge line in front or to the side of the print.

Pros: quicker than a skirt or similar priming.

### IFS
Description: With this disabled, the filament stays in the hotend from print to print.

## Flush volumes starting point
Set multiplier to 1, recalculate, then set any value lower than 90 to 90. 90 seems to be a safe value for nozzle pressure.

<img width="352" height="349" alt="volumes2" src="https://github.com/user-attachments/assets/f69af43d-5870-4b64-8b0a-5f2ac25c99b2" />

---
<div align="center">

## [❤️ Consider supporting this development ❤️](https://github.com/sponsors/Hrybmo)

</div>

## Credits
- Raúl (function3d) [bambufy](https://github.com/function3d/bambufy)
- Sergei (ghzserg) [zmod](https://github.com/ghzserg/zmod)
