# Machine G-code for Orca slicer

## Orca slicer: Machine start G-code

```
START_PRINT EXTRUDER_TEMP=[nozzle_temperature_initial_layer] BED_TEMP=[bed_temperature_initial_layer_single] TOOL={initial_no_support_extruder}
SET_PRINT_STATS_INFO TOTAL_LAYER=[total_layer_count]
```

## Machine end G-code

```
END_PRINT
```

## Layer change G-code

```
;AFTER_LAYER_CHANGE
;[layer_z]
SET_PRINT_STATS_INFO CURRENT_LAYER={layer_num + 1}
; layer num/total_layer_count: {layer_num+1}/[total_layer_count]
```


## Orca slicer
If you have created your profile without using the 3MF I provided, then take these settings into account in addition to these Machines gcode:
- Printer settings
  - Multimaterial
    - Filament load time: 23
    - Filament unload time: 23
  - Extruder
    - Retraction when switching material length: 2
    - Extra length on restart: 0
- Material setting
  - Multimaterial
    - Minimal purge on prime tower: 15
   
##  Orca slicer: Change filament G-code, unified: poop and nopoop
With this unified gcode for filament change, you only need to enable or disable this option to purge in the tower(nopoop) or in the form of poops. 

The Bambufy change filament version works also.

<img width="618" height="419" alt="image" src="https://github.com/user-attachments/assets/9554da95-0ee1-4b77-a690-e9f084397978" />

Change filament G-code:
```
; Machine: AD5X
; less_waste: v1.2.3
{if old_filament_temp < new_filament_temp}
M104 S[new_filament_temp]
{endif}

M204 S7000

{if purge_in_prime_tower || flush_length == 0}
{if toolchange_count > 1}
_NOPOOP
{endif}
G1 Z{max_layer_z + 3.0} F1200
T[next_extruder]
{else}
G1 Z{max_layer_z + 3.0} F1200
T[next_extruder]
{if flush_length > 1}
_GOTO_TRASH
{endif}
; Two flushes or a single large one
{if first_flush_volume > 50}
; First flush
G1 E{first_flush_volume} F{old_filament_e_feedrate/2}
M106 P1 S200
G4 P2000
M106 P1 S0
G1 E-[new_retract_length_toolchange] F1800
_SBROS_TRASH
G1 E[new_retract_length_toolchange] F1800
; Second flush
M104 S[new_filament_temp]
G1 E{second_flush_volume} F{new_filament_e_feedrate/2}
M106 P1 S200
G4 P2000
M106 P1 S0
G1 E-[new_retract_length_toolchange] F1800
_SBROS_TRASH
{else}
; Combo flush
G1 E{first_flush_volume} F{old_filament_e_feedrate/2}
M104 S[new_filament_temp]
G1 E{second_flush_volume} F{new_filament_e_feedrate/2}
M106 P1 S200
G4 P2000
M106 P1 S0
G1 E-[new_retract_length_toolchange] F1800
_SBROS_TRASH
{endif}
{endif}
{if toolchange_count > 1}
G1 Y220 ;Exit trash
{endif}
{if layer_z <= (initial_layer_print_height + 0.001)}
M204 S[initial_layer_acceleration]
{else}
M204 S[default_acceleration]
{endif}
```

## Pause G-code

```
PAUSE
```
## Filename format
Helps to have a unique filename at times
```
{input_filename_base}_{timestamp}.gcode
```