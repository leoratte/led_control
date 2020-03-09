import logging
import threading
import time

from animations import *


class AnimationHandler:
    def __init__(self, led):
        self.led = led
        self.logger = logging.getLogger(__name__)
        self.animationSpeed = 1
        self.animationRunning = False
        self.animationType = AnimationRandom()
        self.thread = threading.Thread(target=self.animation)

    def set_data(self, data):
        speed = 1
        if "animationSpeed" in data:
            speed = data.pop("animationSpeed")
        else:
            self.logger.warning("Animation speed defaulted to 1")
        self.set_animation_speed(speed)
        if "animationType" in data:
            animation_type = data["animationType"]
            self.set_animation_type(animation_type, data)
            self.logger.info("Led {} set to animation {}".format(self.led.get_name(), animation_type))
        else:
            self.logger.warning("No animation type was set")

    def set_animation_type(self, animation_type, data):
        if animation_type == "stop":
            self.stop()
            return
        elif animation_type == "breathing":
            self.animationType = AnimationBreathing(self.led.get_color())
        elif animation_type == "random":
            self.animationType = AnimationRandom()
        elif animation_type == "colorcircle":
            self.animationType = AnimationColorCircle()
        elif animation_type == "colorcirclebreathing":
            self.animationType = AnimationColorCircleBreathing()
        elif animation_type == "randombreathing":
            self.animationType = AnimationRandomBreathing()
        elif animation_type == "custom":
            self.animationType = AnimationCustom(data)
        else:
            self.logger.warning("Unknown animation type '{}'".format(animation_type))
            return
        self.start()

    def set_animation_speed(self, animation_speed):
        self.animationSpeed = animation_speed

    def start(self):
        if not self.animationRunning:
            self.animationRunning = True
            self.thread.start()

    def stop(self):
        if self.animationRunning:
            self.animationRunning = False
            self.thread.join()
            self.thread = threading.Thread(target=self.animation)

    def is_running(self):
        return self.animationRunning

    def animation(self):
        while self.animationRunning:
            self.led.set_color(self.animationType.next_color())
            time.sleep(self.animationType.get_delay() * 1 / self.animationSpeed)


