# lessWaste plugin for the AD5X with ZMOD and OrcaSlicer
## Based on [bambufy](https://github.com/function3d/bambufy/tree/V1.2.10) AD5X V1.2.10
*Does not work with Bambu Studio - removed functions for a performance boost

Changes relative to bambufy:
- Altered print start routine (stay in bucket more, raise bed in advance)
- LINE_PURGE toggle in dialog
- Handles large G-code

Test conditions:
- Enabled Plugins: recommend,lessWaste
- Klipper 13
- USB camera
- zmod 1.6.4.425.2-110-gba7dc9a8
- recommend 1.1.5-0-g1f759590
- AD5X-1.1.7-1.1.0-3.0.6-20250912-Factory firmware (Can downgrade with a flash drive. Best version IMO)
  https://github.com/ghzserg/zmod/releases/download/R/AD5X-1.1.7-1.1.0-3.0.6-20250912-Factory.tgz
- Mainsail interface

This is stable but I want to put more miles and tweaks on it before proposing anything official

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
- Use OrcaSlicer_GCODE.md for OrcaSlicer configuration.

## How to uninstall
- Run the `DISABLE_PLUGIN name=lessWaste` command from the console.
- (Optional) Go back to stock screen `DISPLAY_ON`
- (Optional) Go back to Fluidd `WEB`

## Credits
- Raúl (function3d) [bambufy](https://github.com/function3d/bambufy)
- Sergei (ghzserg) [zmod](https://github.com/ghzserg/zmod)
