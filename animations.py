import colorsys
import abc
from random import randint

from util import hex2rgb


class Animation(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def next_color():
        pass

    @staticmethod
    @abc.abstractmethod
    def get_delay():
        pass


class AnimationAbstractBreathing(Animation, abc.ABC):
    def __init__(self):
        self.down = True
        self.percentage = 1

    def breath(self):
        if self.down:
            if self.percentage > 0:
                self.percentage -= 0.01
            else:
                self.down = False
                self.percentage += 0.01
        else:
            if self.percentage < 1:
                self.percentage += 0.01
            else:
                self.down = True
                self.percentage -= 0.01
        self.percentage = round(self.percentage, 2)


class AnimationRandom(Animation):
    @staticmethod
    def next_color():
        return randint(0, 255), randint(0, 255), randint(0, 255)

    @staticmethod
    def get_delay():
        return 0.5


class AnimationBreathing(AnimationAbstractBreathing):
    def __init__(self, color):
        super().__init__()
        if max(color):
            multiplier = 255 / max(color)
            self.color = (round(multiplier * color[0]),
                          round(multiplier * color[1]),
                          round(multiplier * color[2]))
        else:
            self.color = (0, 0, 0)

    def next_color(self):
        self.breath()
        return (round(self.percentage * self.color[0]),
                round(self.percentage * self.color[1]),
                round(self.percentage * self.color[2]))

    @staticmethod
    def get_delay():
        return 0.05


class AnimationColorCircle(Animation):
    def __init__(self):
        self.hue = 0

    def next_color(self):
        self.hue = (self.hue + 1) % 360
        color = colorsys.hsv_to_rgb(self.hue / 360, 1, 1)
        return (round(255 * color[0]),
                round(255 * color[1]),
                round(255 * color[2]))

    @staticmethod
    def get_delay():
        return 0.05


class AnimationColorCircleBreathing(AnimationAbstractBreathing):
    def __init__(self):
        super().__init__()
        self.hue = 0

    def next_color(self):
        self.breath()
        if self.percentage <= 0:
            self.hue = (self.hue + 50) % 360
        color = colorsys.hsv_to_rgb(self.hue / 360, 1, 1)
        return (round(self.percentage * 255 * color[0]),
                round(self.percentage * 255 * color[1]),
                round(self.percentage * 255 * color[2]))

    @staticmethod
    def get_delay():
        return 0.05


class AnimationRandomBreathing(AnimationAbstractBreathing):
    def __init__(self):
        super().__init__()
        self.color = (4 * randint(0, 63), 4 * randint(0, 63), 4 * randint(0, 63))

    def next_color(self):
        self.breath()
        if self.percentage <= 0:
            self.color = (4 * randint(0, 63), 4 * randint(0, 63), 4 * randint(0, 63))
        return (round(self.percentage * self.color[0]),
                round(self.percentage * self.color[1]),
                round(self.percentage * self.color[2]))

    @staticmethod
    def get_delay():
        return 0.05


class AnimationCustom(Animation):
    def __init__(self, data):
        self.steps = data["animationSteps"]
        self.stepCounter = 0
        self.currentStep = self.steps[0]
        self.fadePercentage = 0

    def next_step(self):
        self.stepCounter = (self.stepCounter + 1) % len(self.steps)
        self.currentStep = self.steps[self.stepCounter]

    def fade(self):
        self.fadePercentage = (self.fadePercentage + 1) % 100
        if not self.fadePercentage:
            self.next_step()

    def next_color(self):
        self.fade()
        start_color = hex2rgb(self.currentStep["startColor"][1:7])
        end_color = hex2rgb(self.currentStep["endColor"][1:7])
        color_vector = (end_color[0] - start_color[0],
                        end_color[1] - start_color[1],
                        end_color[2] - start_color[2])
        return (round(start_color[0] + self.fadePercentage / 100 * color_vector[0]),
                round(start_color[1] + self.fadePercentage / 100 * color_vector[1]),
                round(start_color[2] + self.fadePercentage / 100 * color_vector[2]))

    @staticmethod
    def get_delay():
        return 0.05
