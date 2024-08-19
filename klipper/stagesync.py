# Support to handle heater_generic as an extension of extruder
# Specific function to optimize the management of the Aten V-ONE hotend and similar.
# more information at www.aten3d.com
#
# Copyright (C) 2024 Aten <info@aten3d.com>
# Aten is a registered trademark of Digimaker3D srl
#
# This file may be distributed under the terms of the GNU GPLv3 license.
#
# If you need to manage multiple heaters and multiple temperature sensors in a single
# hotend you can now do it cleanly. StageSync allows you to define the first heater
# with attached temperature sensor in the [extruder] section and the additional heaters
# and temperature sensors in the [heater_generic] section, also adding the "temp_ratio"
# variable which is a temperature multiplier definable for each additional heater.
#
# klippy/extras/stagesync.py

import logging

class StageSync:
    def __init__(self, config, extruder_name):
        self.printer = config.get_printer()
        self.extruder_name = config.get_name().split()[1]
        logging.info(f"Found extruder: {self.extruder_name}")
        
        stage_names = config.get('stages').split(',')
        temp_ratios = config.get('temp_ratio').split(',')

        # Lookup and map each heater with its corresponding temp_ratio
        self.heaters = []
        for stage_name, temp_ratio in zip(stage_names, temp_ratios):
            stage_name = stage_name.strip()
            try:
                heater = self.printer.lookup_object(f"heater_generic {stage_name}")
                temp_ratio = float(temp_ratio.strip())
                self.heaters.append((heater, temp_ratio))
                logging.info(f"Mapped heater: {stage_name} with temp_ratio: {temp_ratio}")
            except Exception as e:
                logging.error(f"Error mapping heater {stage_name}: {e}")

        # Register an event handler for temperature synchronization
        self.printer.register_event_handler("klippy:connect", self._connect)
        logging.info(f"StageSync for {self.extruder_name} initialized successfully.")

    def _connect(self):
        # Synchronize temperatures when the printer connects
        logging.info(f"Synchronizing temperatures for extruder: {self.extruder_name}")
        self.sync_temperatures()

    def sync_temperatures(self):
        # Apply the target temperature of the extruder to its associated heaters
        target_temp = self.extruder.get_status()['target']
        logging.info(f"Extruder target temperature: {target_temp}")
        for heater, temp_ratio in self.heaters:
            adjusted_temp = target_temp * temp_ratio
            heater.set_temp(adjusted_temp)
            logging.info(f"Set heater to: {adjusted_temp} based on temp_ratio: {temp_ratio}")

def load_config_prefix(config):
    # Extract the extruder name from the section prefix
    prefix_name = config.get_name()
    extruder_name = prefix_name.split(' ', 1)[1]  # Gets the part after "stagesync "

    logging.info(f"Loading config for stagesync: {prefix_name}")
    return StageSync(config, extruder_name)
