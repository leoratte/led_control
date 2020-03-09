import pigpio
import json
import logging

from led import Led


class Controller:
    def __init__(self, config_path):
        self.logger = logging.getLogger(__name__)
        with open(config_path, "r") as f:
            config = json.load(f)
            f.close()
        self.leds = dict()
        pizw = pigpio.pi()
        for led_group in config.get("leds"):
            self.leds[led_group.get("name")] = Led(led_group.get("name"), pizw, led_group.get("pins"))
        self.web_config = dict()
        self.web_config["leds"] = list(self.leds.keys())
        self.web_config["animations"] = config["animations"]
        self.logger.info("Configuration from {} loaded with {} LED(s)".format(config_path, len(self.leds)))

    def parse(self, data):
        if "name" in data:
            self.logger.info("Message parsed")
            led_name = data.pop("name")
            if led_name == "all":
                for led in self.leds.values():
                    self.set_led(led, data)
            elif led_name in self.leds:
                self.set_led(self.leds[led_name], data)
            else:
                self.logger.warning("Unknown led '{}'".format(led_name))
        else:
            self.logger.warning("Message does not contain led name")

    def set_led(self, led, data):
        led.set(data)

    def get_webconfig(self):
        return self.web_config
