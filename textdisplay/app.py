import time

import app
import settings
from app_components import TextDialog, clear_background
from events.input import BUTTON_TYPES, Buttons
from perf_timer import PerfTimer
from .message import GetMessage

class NameBadge(app.App):
    name = None

    # colors used for the main name part
    bg_color = (0, 0, 0)
    fg_color = (255, 255, 255)

    # colors used for the 'hello my name is' part
    header_bg_color = (0, 150, 0)
    header_fg_color = (255, 255, 255)

    def __init__(self):
        super().__init__()
        self.button_states = Buttons(self)
        self.message = ""
        self.last_time = 0

    async def run(self, render_update):
        last_time = time.ticks_ms()
        while True:
            cur_time = time.ticks_ms()
            delta_ticks = time.ticks_diff(cur_time, last_time)
            with PerfTimer(f"Updating {self}"):
                self.update(delta_ticks)
            await render_update()
            last_time = cur_time

            
    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            # quit the app
            self.minimise()
            self.button_states.clear()

        cur_time = time.ticks_ms()
        if cur_time - self.last_time > 10000:
            self.updateMessage()
            self.button_states.clear()
            self.last_time = cur_time

    def draw(self, ctx):
        clear_background(ctx)

        ctx.text_align = ctx.CENTER

        # draw backgrounds
        ctx.rgb(*self.bg_color).rectangle(-120, -120, 240, 240).fill()
        ctx.rgb(*self.header_bg_color).rectangle(-120, -120, 240, 100).fill()

        ctx.font_size = 56
        ctx.font = "Arimo Bold"
        ctx.rgb(*self.header_fg_color).move_to(0, -60).text("Hello")
        ctx.rgb(*self.fg_color).move_to(0, 60).text(self.message)

        ctx.font_size = 28
        ctx.font = "Arimo Bold"
        ctx.rgb(*self.header_fg_color).move_to(0, -30).text("my message is")

        self.draw_overlays(ctx)

    def updateMessage(self):
        try:
            self.message = GetMessage()
        except Exception as e:
            1+1


__app_export__ = NameBadge