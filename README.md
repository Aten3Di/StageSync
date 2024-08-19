# StageSync
StageSync is a klipper plugin that allows you to handle [heater_generic] as an extension of [extruder]



## What is it for:

If you need to manage multiple heaters and multiple temperature sensors in a single hotend you can now do it cleanly.
StageSync allows you to define the first heater with attached temperature sensor in the [extruder] section and the additional heaters and temperature sensors in the [heater_generic] section, also adding the "temp_ratio" variable which is a temperature multiplier definable for each additional heater.


## Configuration:

### [stagesync]
Support for additional heaters synchronized to an extruder's temperatures (any number of sections can be defined with a "stagesync" prefix).
```
[stagesync extruder_config_name]
#stages: stage1, stage2
#   Define the name of the additional heater to synchronize with the extruder.
#   If there are more than one heaters they must be divided by a comma.
#   This parameter must be provided.
#temp_ratio: 1.0, 0.9
#   Defines the value that changes the target temperature of each heater synchronized
#   with an extruder. It specifies a percentage of the target extruder temperature
#   to apply to the heater. Each value corresponds to the respective heater divided
#   by a comma. The value range is from 0 (0%) to 2.00 (200%). This value is optional
#   and if not defined a multiplier of 1.0 will be applied.

```
