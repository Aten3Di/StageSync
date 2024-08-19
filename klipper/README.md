# Installation:
ssh into your Klipper device and execute the following commands:

- Clone and install the software
```
cd  ~
git clone https://github.com/Aten3Di/StageSync.git
```
- run the installation script.
```
~/StageSync/klipper/install_stagesync.sh
```
- Add the following section to moonraker.conf if your printer runs Moonraker and then you can update StageSync with 1 click via the klipper web page or screen.
```
[update_manager StageSync]
type: git_repo
primary_branch: new
channel: dev
path: ~/StageSync
origin: https://github.com/Aten3Di/StageSync.git
install_script: ./klipper/install_stagesync.sh
is_system_service: False
managed_services: klipper
info_tags:
  desc=StageSync
```

# Configuration:

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
