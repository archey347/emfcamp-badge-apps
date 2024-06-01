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

        t = time.ticks_ms() * self.delta

        for i in range(LEDS):

            tmp = ((i + t + self.offset) * math.pi) / 6

            cos_x = math.cos(tmp) ** 10

            self.setColor(i, int(cos_x * intensity))

    def setColor(self, i, intensity):
        color = tildagonos.leds[i + 1]

        if self.channel == 0:
            color = (intensity, color[1], color[2])
        elif self.channel == 1:
            color = (color[0], intensity, color[2])
        else:
            color = (color[0], color[1], intensity)

        tildagonos.leds[i + 1] = color

class ExampleApp(app.App):
    def __init__(self):
        eventbus.emit(PatternDisable())

        self.button_states = Buttons(self)
        delta = 0.01
        self.spirals = [
            Spiral(delta, 0, 0), 
            Spiral(delta, 3, 1)       
        ]

    def update(self, delta):
        global intensity
        
        mag = abs(self.spirals[0].delta)
        change = False
        if self.button_states.get(BUTTON_TYPES["UP"]):
            # The button_states do not update while you are in the background.
            # Calling clear() ensures the next time you open the app, it stays open.
            # Without it the app would close again immediately.
            mag += 0.001
            change = True
            self.button_states.clear()
        
        if self.button_states.get(BUTTON_TYPES["DOWN"]):
            mag -= 0.001
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

        out = str(round(self.spirals[0].delta, 4)) + "," + str(intensity)

        ctx.rgb(1,1,1).move_to(-80,0).text(out)
        ctx.restore()
        
__app_export__ = ExampleApp



