# StageSync
StageSync is a klipper plugin that allows you to handle [heater_generic] as an extension of [extruder]



## What is it for:

If you need to manage multiple heaters and multiple temperature sensors in a single hotend you can now do it cleanly.
StageSync allows you to define the first heater with attached temperature sensor in the [extruder] section and the additional heaters and temperature sensors in the [heater_generic] section, also adding the "temp_ratio" variable which is a temperature multiplier definable for each additional heater.
