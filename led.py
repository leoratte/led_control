import logging

from animation import AnimationHandler
from util import hex2rgb


class Led:
    def __init__(self, name, pizw, pins):
        self.logger = logging.getLogger(__name__)
        self.name = name
        self.pizw = pizw
        self.animation = AnimationHandler(self)
        self.color = (0, 0, 0)
        self.pins = pins

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color

    def set(self, data):
        if "type" in data:
            t = data.get("type")
            if t == "static":
                self.static_color(data)
            elif t == "animation":
                self.animation.set_data(data)
            else:
                self.logger.warning("Unknown type '{]'".format(t))
        else:
            self.logger.warning("Type not set")

    def static_color(self, data):
        if "color" in data:
            color = hex2rgb(data["color"])
            self.animation.stop()
            self.set_color(color)
            self.logger.info("Led {} set to static {}".format(self.name, data["color"]))
        else:
            self.logger.warning("No static color set")

    def set_color(self, color):
        self.color = color
        for i in range(3):
            if color[i] > 255 or color[i] < 0:
                raise Exception
        for i in range(3):
            self.pizw.set_PWM_dutycycle(self.pins[i], color[i])

    def animation(self, data):
        self.animation.set_data(data)
