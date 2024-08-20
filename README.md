# StageSync
StageSync is a plugin for Klipper that allows you to synchronize a primary heater with secondary heaters. The plugin allows you to define a primary heater, monitor its target temperature, and apply a customizable temperature multiplier to each additional heater. Each secondary heater is then set automatically on the desired temperature, calculated by multiplying the target temperature of the main heater by a specified value. This is useful for managing scenarios where it is necessary to keep several heating zones in sync with one main heater, ensuring that the relative temperatures are always in proportion.

# Key Points
## Main Heater Monitoring:
The plugin focuses on monitoring the target temperature of the main heater.
## Synchronization of secondary heaters:
Secondary heaters are automatically synchronized with the temperature of the primary heater.
## Flexibility:
Each secondary heater can have its own temperature multiplier, allowing precise control of temperatures.
