import logging
import abc
import time

from rpi_ws281x import PixelStrip, Color

from animation import AnimationHandler
from util import hex2rgb


class Led(abc.ABC):
    def __init__(self, led_id, name):
        self.logger = logging.getLogger(__name__)
        self.id = led_id
        self.name = name
        self.animation = AnimationHandler(self)
        self.color = (0, 0, 0)
        self.set_color((0, 0, 0))

    def get_id(self):
        return self.id

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

    def animation(self, data):
        self.animation.set_data(data)

    @abc.abstractmethod
    def set_color(self, color):
        pass


class AnalogLed(Led):
    def __init__(self, led_id, name, rasp_pi, pins):
        super().__init__(led_id, name)
        self.rasp_pi = rasp_pi
        self.pins = pins

    def set_color(self, color):
        self.color = color
        for i in range(3):
            if color[i] > 255 or color[i] < 0:
                raise Exception
        for i in range(3):
            self.rasp_pi.set_PWM_dutycycle(self.pins[i], color[i])


class DigitalLed(Led):
    def __init__(self, led_id, name, pin, led_count):
        super().__init__(led_id, name)
        # self.pin = pin
        # self.led_count = led_count
        LED_COUNT = led_count  # Number of LED pixels.
        LED_PIN = pin  # GPIO pin connected to the pixels (18 uses PWM!).
        # LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
        LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
        LED_DMA = 10  # DMA channel to use for generating signal (try 10)
        LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
        LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
        LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()

    def set_color(self, color):
        self.colorWipe(self.strip, Color(color[0], color[1], color[2]), wait_ms=1)

    def colorWipe(self, strip, color, wait_ms=50):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)