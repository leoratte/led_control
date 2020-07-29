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
        self.led_list = dict()
        rasp_pi = pigpio.pi()
        for led_group in config.get("leds"):
            self.led_list[led_group.get("id")] = Led(led_group.get("id"), led_group.get("name"), rasp_pi, led_group.get("pins"))
        self.web_config = dict()
        self.web_config["leds"] = list(self.led_list.keys())
        self.web_config["animations"] = config["animations"]
        self.logger.info("Configuration from {} loaded with {} LED(s)".format(config_path, len(self.led_list)))

    def parse(self, data):
        if "id" in data:
            self.logger.info("Message parsed")
            led_id = data.pop("id")
            if led_id == 0:
                for led in self.led_list.values():
                    self.set_led(led, data)
            elif led_id in self.led_list:
                self.set_led(self.led_list[led_id], data)
            else:
                self.logger.warning("Unknown led '{}'".format(led_id))
        else:
            self.logger.warning("Message does not contain led id")

    def set_led(self, led, data):
        led.set(data)

    def get_webconfig(self):
        return self.web_config
