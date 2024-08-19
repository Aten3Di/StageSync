# StageSync allows you to define a main heater and synchronize additional
# heaters to it by adding a temperature multiplier to each one.
#
# Support for optimizing management of the Aten V-ONE hotend and similar.
# more information at www.aten3d.com
#
# Copyright (C) 2024 Aten <info@aten3d.com>
# Aten is a registered trademark of Digimaker3D srl
#
# This file may be distributed under the terms of the GNU GPLv3 license.
#
# klippy/extras/stagesync.py

import logging

class StageSync:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.heater_name = config.get_name().split()[1]
        self.heater = None
        self.stages = []  # Used to maintain the association between stages and temp_ratio
        self.last_target_temp = None  # Stores the last target temperature for comparison
        self.printer.register_event_handler("klippy:connect",
                                            self.handle_connect)

        logging.info(f"StageSync initialized for heater: {self.heater_name}")

        stage_names = config.get('stages').split(',')
        temp_ratios = config.get('temp_ratio').split(',')

        # Save the names and temp_ratios for future mapping
        for stage_name, temp_ratio in zip(stage_names, temp_ratios):
            try:
                stage = self.printer.lookup_object(stage_name.strip())
                if not stage:
                    raise Exception(f"Stage {stage_name} not found")
                
                self.stages.append((stage, float(temp_ratio.strip())))
                logging.info(f"Mapped stage: {stage_name.strip()} with temp_ratio: {temp_ratio.strip()}")
            except Exception as e:
                logging.error(f"Error mapping stage {stage_name.strip()}: {e}")

        # Register the handler for synchronization when the system is ready
        self.printer.register_event_handler("klippy:ready", self.handle_ready)

    def handle_connect(self):
        try:
            pheaters = self.printer.lookup_object('heaters')
            self.heater = pheaters.lookup_heater(self.heater_name)
            logging.info("Heater %s initialized successfully", self.heater_name)
            reactor = self.printer.get_reactor()
            self.check_timer = reactor.register_timer(self.check_event, reactor.NOW)
        except Exception as e:
            logging.error(f"Error initializing heater {self.heater_name}: {e}")

    def handle_ready(self):
        try:
            # Synchronize temperatures on the first run
            self.sync_temperatures(self.last_target_temp)
        except Exception as e:
            logging.error(f"Error during temperature synchronization for heater {self.heater_name}: {e}")

    def check_event(self, eventtime):
        try:
            temp, target = self.heater.get_temp(eventtime)
            if temp >= target or target is None or target <= 0.:
                logging.error(f"Failed to get target temperature for {self.heater_name}.")
                return

            logging.info(f"Heater target temperature: {target}")

            if target != self.last_target_temp:
                self.last_target_temp = target
                self.sync_temperatures(target)
        except Exception as e:
            logging.error(f"Error in temperature callback for {self.heater_name}: {e}")

    def sync_temperatures(self, target):
        logging.info("Syncing temperatures...")
        if not self.heater:
            logging.error(f"Heater {self.heater_name} is not available.")
            return

        logging.info(f"Heater target temperature: {target}")

        # Apply the temperature to the stages using a G-code command
        for stage, temp_ratio in self.stages:
            adjusted_temp = target * temp_ratio
            stage_name = stage.get_name()  # Assuming the get_name() method exists and returns the stage name
            gcode_command = f'SET_HEATER_TEMPERATURE HEATER="{stage_name}" TARGET="{adjusted_temp}"'
            logging.info(f"Sending G-code command: {gcode_command}")
            try:
                self.printer.run_script(gcode_command)
                logging.info(f"G-code command sent successfully: {gcode_command}")
            except Exception as e:
                logging.error(f"Failed to send G-code command for stage {stage_name}: {e}")

def load_config_prefix(config):
    logging.info(f"Loading config for stagesync: {config.get_name()}")
    return StageSync(config)


    logging.info(f"Loading config for stagesync: {prefix_name}")
    return StageSync(config, extruder_name)
