# lessWaste plugin for the AD5X with ZMOD and OrcaSlicer
## Based on [bambufy](https://github.com/function3d/bambufy/tree/V1.2.10) AD5X V1.2.10

### Goals: To minimize waste and print time.
### Features: Backups, Channel swap, Virtual channels, Purge control, Recovery, and start UI.
 
### For unlocking IFS on boot:

_IFS_VARS ifs_unlock_after_boot=1

_IFS_VARS ifs_unlock_after_boot=0

### Test conditions:
- OrcaSlicer 2.3.2
- Enabled Plugins: recommend,lessWaste,notify,timelapse
- Klipper 12
- USB camera
- zmod 1.7.0
- recommend 1.1.6
- zmod md5 post proccessing
- AD5X 3.0.3

*In theory this should work with Bambu studio using [bambufy](https://github.com/function3d/bambufy/tree/V1.2.10) G-code but is not tested.
## How to install
- Install [zmod](https://github.com/ghzserg/zmod) following the [instructions](https://github.com/ghzserg/zmod/wiki/Setup_en#installing-the-mod)   
- Change the native display to **Guppyscreen** running the `DISPLAY_OFF` command
- (Optional) Change web ui to **Mainsail** running the `WEB` command
- Run `ENABLE_EXTRA_PLUGINS` command to enable the external plugin repository
- Run `ENABLE_PLUGIN name=lesswaste` command from the console (recommend should be enabled already)
- Use [OrcaSlicer_GCODE.md](https://github.com/Hrybmo/lessWaste/blob/master/OrcaSlicer_GCODE.md) or [OrcaSlicer .3mf](https://github.com/Hrybmo/lessWaste/blob/master/lessWaste_ad5x_OrcaSlicer_V2.3mf) for slicer configuration.

## How to uninstall
- Run the `DISABLE_PLUGIN name=lesswaste` command from the console.
- (Optional) Go back to stock screen `DISPLAY_ON`
- (Optional) Go back to Fluidd `WEB`

## Creating less waste
You have two main options and depending on the type of print, one may be better than the other.

### Option 1: Purge in prime tower
Description: Instead of purging out the back, a prime tower is used for purging.

Pros: The settings "Flush into object's infill", "Flush into objects' support", and "flushing volumes" are respected.

Cons: A large prime tower is generally required, taking up volume.

Best used for: Flushing into things. 

Notes: Place the prime tower close to the cutter area when using "No sparse layers (beta)".

### Option 2: Purge out the back
Description: Purge out the back like stock but with more control.

Pros: A small or no prime tower is needed. Respects "flushing volumes" when purging.

Cons: The settings "Flush into object's infill" and "Flush into objects' support" do not reduce the purge amount.

Best used for: Where it is more efficient to build a small or no prime tower instead of a large one on every layer.

## Settings
### Backup
Description: If backup is enabled and there are matching filament types and color filaments, they will join. The backup locations are set on start and consumed during print. If backup is triggered during a print, the lowest available filament number is activated (scans 1 -> 4). When printing, consumed channels can be refilled once there are no backups left and/or there is a pause. Backup is not available in Virtual channel mode.

Example below: If filament one runs out then filament two will automatically load and continue.

<img width="388" height="414" alt="image" src="https://github.com/user-attachments/assets/80828ebf-00d4-49bc-96d9-16d94ef22158" />

### LEVELING
Description: Performs a bed mesh leveling in the print area at start.

### START_P
Description: Control the purge out the back when starting a print.
- OFF = No start purge
- ON = Run start purge
- T+C = Run start purge when the Type or Color is different than last filament run in the hotend
- TYPE = Run start purge when the Type is different than last filament in the hotend

### L_PURGE
Description: Creates a purge line in front or to the side of the print.

Pros: quicker than a skirt or similar priming.

### IFS
Description: With this disabled, the filament stays in the hotend from print to print.

### Dialog
Description: Provide on screen information when issues occur.

### Channel swap
Description: press the tool in the dialog to swap with another location.

### UNLOCK IFS
Description: Unlocks IFS if ever needed.

## Flush volumes starting point (OrcaSlicer)
### Locations:
- Nozzle volume: Orca->Printer Settings->Printable space
- Multiplier: Set Flush Volumes->multiplier

### Goal:
Set Black -> White color transition ~ 90 mm^3, White -> Black mm^3 user adjust. 

Assumes with a small prime tower, if no prime tower then may need to increase both color transition amounts.

NOTE: Updated [color change g-code](https://github.com/Hrybmo/lessWaste/blob/master/OrcaSlicer_GCODE.md) as of V1.2.31

### Standard setting:
- Nozzle volume = 14 mm^3
- Multiplier = 1

<img width="409" height="410" alt="image" src="https://github.com/user-attachments/assets/5703983b-23f6-45c5-9ae4-7382a4bdfeb0" />

### Troubleshooting:
- If gettings false jam errors during filament changes, follow the Zmod FAQ for "Filament jam detected (IFS)" and add extra detection length in user.cfg, the value below is a reference and might need adjustment.
```
[zmod_ifs_motion_sensor ifs_motion_sensor]
detection_length: 15
```
- Use Klipper 12 (UPDATE_MCU FORCE=12) if running into "timer too close" issues.

---
<div align="center">

## [Github](https://github.com/sponsors/Hrybmo)/[Paypal](https://paypal.me/JJH4)
</div>

## Credits
- Raúl (function3d) [bambufy](https://github.com/function3d/bambufy)
- Sergei (ghzserg) [zmod](https://github.com/ghzserg/zmod)
