import asyncio
import app
import time
import math
from tildagonos import tildagonos

from events.input import Buttons, BUTTON_TYPES
from system.eventbus import eventbus
from system.patterndisplay.events import *


LEDS = 12
intensity = 255

class Spiral:
    def __init__(self, delta, offset, channel):
        self.delta = delta
        self.channel = channel
        self.offset = offset

    def update(self):

        t = self.getT()

        for i in range(LEDS):
            self.setColor(i, self.getColour(i, t))

    def getT(self):
        return time.time_ns() * self.delta * 0.000001

    def getColour(self, i, t):
        tmp = ((i + t + self.offset) * math.pi) / 6

        cos_x = math.cos(tmp) ** 20

        tmp = cos_x * intensity

        # src: https://assets.lutron.com/a/documents/measured_vs_perceived.pdf
        result = intensity * ((tmp / intensity) ** 2)

        return int(result)

    def setColor(self, i, intensity):
        color = tildagonos.leds[i + 1]

        if self.channel == 0:
            color = (intensity, color[1], color[2])
        elif self.channel == 1:
            color = (color[0], intensity, color[2])
        else:
            color = (color[0], color[1], intensity)

        i = LEDS - i

        tildagonos.leds[i] = color

class ExampleApp(app.App):
    def __init__(self):
        eventbus.emit(PatternDisable())

        self.text = ""
        self.button_states = Buttons(self)
        delta = 0.001
        self.spirals = [
            Spiral(delta, 0, 0), 
            Spiral(delta, 2, 1),
            Spiral(delta, 4, 2)       
        ]

    def update(self, delta):
        global intensity
        
        mag = abs(self.spirals[0].delta)
        change = False
        if self.button_states.get(BUTTON_TYPES["UP"]):
            # The button_states do not update while you are in the background.
            # Calling clear() ensures the next time you open the app, it stays open.
            # Without it the app would close again immediately.
            mag += 0.0001
            change = True
            self.button_states.clear()
        
        if self.button_states.get(BUTTON_TYPES["DOWN"]):
            mag -= 0.0001
            change = True
            self.button_states.clear()

        if self.button_states.get(BUTTON_TYPES["LEFT"]):
            intensity -= 10
            intensity = max(0, intensity)

        if self.button_states.get(BUTTON_TYPES["RIGHT"]):
            intensity += 10
            intensity = min(255, intensity)

        if change:
            mag = max(0, mag)

            for spiral in self.spirals:
                if spiral.delta > 0:
                    spiral.delta = mag
                else:
                    spiral.delta = -mag
        
        self.updateLEDs()

    def updateLEDs(self):
        for i in range(LEDS):
            tildagonos.leds[i + 1] = (0, 0, 0)

        for spiral in self.spirals:
            spiral.update()

        tildagonos.leds.write()

    def draw(self, ctx):
        ctx.save()
        ctx.rgb(0, 0, 0).rectangle(-120,-120,240,240).fill()
        ctx.rgb(1,1,1).move_to(-90,0).text(self.text)

        segments = 24
        segment_width = 2 * math.pi / segments

        for i in range(segments):
            led_rad = (i / segments) * LEDS
            rad = (i / segments) * 2 * math.pi

            a = int(led_rad)
            b = a + 1 % LEDS

            colour = tildagonos.leds[LEDS - a]
            ctx.rgb(colour[0], colour[1], colour[2]).arc(0, 0, 90, rad, rad + segment_width, 0).stroke()

        ctx.restore()
        
__app_export__ = ExampleApp



