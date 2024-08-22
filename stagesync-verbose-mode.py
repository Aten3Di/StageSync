# StageSync allows you to define a main heater and synchronize additional
# heaters to it by adding a temperature multiplier to each one.
#
#####.#####.#####. DISCLAMER .#####.#####.#####
#####.##### ONLY FOR DEVELOPER USE! #####.#####
#
# rename the file to stagesync.py to use it!
#
# StageSync - Verbose Mode
#
# This version of the StageSync file has been configured in verbose mode,
# ideal for development and debugging purposes. In this mode, the code includes
# numerous detailed logs that provide an exhaustive trace of the operations 
# performed. This can be extremely useful for identifying and resolving issues,
# but may be intrusive in production environments.
#
# Use this version only when detailed monitoring of system behavior is required.
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
        self.gcode = self.printer.lookup_object('gcode')  # Lookup the gcode object
        self.printer.register_event_handler("klippy:connect", self.handle_connect)

        logging.info(f"StageSync heater found: {self.heater_name}")

        stage_names = config.get('stages').split(',')
        temp_ratios = config.get('temp_ratio').split(',')

        # Save the names and temp_ratios for future mapping
        for stage_name, temp_ratio in zip(stage_names, temp_ratios):
            try:
                temp_ratio_value = float(temp_ratio.strip())
                
                # Validate temp_ratio
                if temp_ratio_value < 0 or temp_ratio_value > 2.0:
                    self.ratio_fault(stage_name.strip(), temp_ratio_value)

                # Attempt to look up the heater object by name using general object lookup
                stage = self.printer.lookup_object('heater', stage_name.strip())
                if stage is None:
                    self.stages_fault(stage_name.strip())
                
                self.stages.append((stage, temp_ratio_value))
                logging.info(f"StageSync stages: {stage_name.strip()} with temp_ratio: {temp_ratio.strip()}")
            except Exception as e:
                self.mapping_fault(stage_name.strip(), e)

        # Register the handler for synchronization when the system is ready
        self.printer.register_event_handler("klippy:ready", self.handle_ready)

    def handle_connect(self):
        try:
            pheaters = self.printer.lookup_object('heaters')
            self.heater = pheaters.lookup_heater(self.heater_name)
            logging.info("StageSync heater: %s initialized", self.heater_name)
            reactor = self.printer.get_reactor()
            self.check_timer = reactor.register_timer(self.check_event, reactor.NOW)
        except Exception as e:
            self.heater_fault(self.heater_name, e)

    def handle_ready(self):
        try:
            # Synchronize temperatures on the first run
            self.sync_temperatures(self.last_target_temp)
        except Exception as e:
            logging.error(f"StageSync: Error during temperature synchronization for heater {self.heater_name}: {e}")

    def check_event(self, eventtime):
        try:
            temp, target = self.heater.get_temp(eventtime)
            if target is None or target <= 0.:
                logging.warning(f"StageSync: Invalid target temperature for {self.heater_name}. Retrying...")
                return eventtime + 1.0  # Retry after 1 second

            if target != self.last_target_temp:
                self.last_target_temp = target
                self.sync_temperatures(target)

            # Schedule the next check in 1 second
            next_check_time = eventtime + 1.0
            logging.info(f"StageSync: Scheduling next check at {next_check_time}")
            return next_check_time

        except Exception as e:
            logging.error(f"StageSync: Error in temperature callback for {self.heater_name}: {e}")
            return eventtime + 1.0  # Retry after 1 second

    def sync_temperatures(self, target):
        logging.info("StageSyncing temperatures...")
        if not self.heater:
            logging.error(f"StageSync Heater {self.heater_name} is not available.")
            return

        if target is None:
            logging.error(f"StageSync: Cannot sync temperatures, target temperature is None.")
            return

        logging.info(f"StageSync: Heater target temperature: {target}")

        # Apply the temperature to the stages using a G-code command
        for stage, temp_ratio in self.stages:
            adjusted_temp = target * temp_ratio
            stage_name = stage.get_name() if hasattr(stage, 'get_name') else stage
            gcode_command = f'SET_HEATER_TEMPERATURE HEATER="{stage_name}" TARGET="{adjusted_temp}"'
            try:
                self.gcode.run_script(gcode_command)  # Use gcode object to send the command
                logging.info(f"StageSync G-code command sent successfully: {gcode_command}")
            except Exception as e:
                self.gcode_fault(stage_name.strip(), e)

    def ratio_fault(self, stage_name, temp_ratio_value):
        msg = f"StageSync: temp_ratio for stage '{stage_name}' is out of bounds: {temp_ratio_value}"
        logging.error(msg)
        self.printer.invoke_shutdown(msg)
        return self.printer.get_reactor().NEVER

    def stages_fault(self, stage_name):
        msg = f"StageSync: stage '{stage_name}' not found"
        logging.error(msg)
        self.printer.invoke_shutdown(msg)
        return self.printer.get_reactor().NEVER

    def heater_fault(self, heater_name, error):
        msg = f"StageSync: Error initializing heater '{heater_name}': {error}"
        logging.error(msg)
        self.printer.invoke_shutdown(msg)
        return self.printer.get_reactor().NEVER

    def mapping_fault(self, stage_name, error):
        msg = f"StageSync: Error mapping stage '{stage_name}': {error}"
        logging.error(msg)
        self.printer.invoke_shutdown(msg)
        return self.printer.get_reactor().NEVER

    def gcode_fault(self, stage_name, error):
        msg = f"StageSync: Temperature synchronization via G-code failed! '{stage_name}': {error}"
        logging.error(msg)
        self.printer.invoke_shutdown(msg)
        return self.printer.get_reactor().NEVER

def load_config_prefix(config):
    logging.info(f"Loading config for StageSync: {config.get_name()}")
    return StageSync(config)
