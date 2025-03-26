import math
import pygame as pg


class Window:

    def __init__(
        self,
        width,  # width of the graphics window (in pixels)
        height,  # height of the graphics window (in pixels)
        title,  # title appearing at the top of the window (str)
        bgcolor="white",  # background color of the window (str)
    ):
        pg.init()
        pg.display.set_caption(title)
        self.width = width
        self.height = height
        self.clock = pg.time.Clock()
        self.surface = pg.display.set_mode((width, height))
        self.bgcolor = bgcolor
        self.surface.fill(bgcolor)
        self.graphics = []
        self.callbacks = []
        self.event_handlers = dict()

    def paste(self, graphic, x, y):
        """Pastes a graphic (e.g. Rectangle, Textbox) at the designated (x, y) position."""
        self.graphics.append((graphic, x, y))

    def remove(self, graphic):
        """Removes a graphic from the window."""
        self.graphics = [(g, x, y) for (g, x, y) in self.graphics if g != graphic]

    def clear(self):
        """Removes everything from the window."""
        self.graphics = []

    def refresh(self):
        """Redraws the window and handles any recent events."""
        self.surface.fill(self.bgcolor)
        for graphic, x, y in self.graphics:
            self.surface.blit(graphic.surface, (x, y))
        pg.display.flip()
        quit_now = False
        self.clock.tick(60)
        events = pg.event.get()
        for event in events:
            if event.type >= pg.USEREVENT and event.type <= pg.USEREVENT + len(
                self.callbacks
            ):
                interval, callback = self.callbacks[event.type - pg.USEREVENT]
                pg.time.set_timer(event, interval)
                callback()
            elif event.type == pg.MOUSEBUTTONDOWN and "click" in self.event_handlers:
                func = self.event_handlers["click"]
                func(event.pos[0], event.pos[1])
            elif event.type == pg.MOUSEMOTION and "mousemove" in self.event_handlers:
                func = self.event_handlers["mousemove"]
                func(event.pos[0], event.pos[1])
            elif event.type == pg.QUIT:
                quit_now = True
        return quit_now

    def call_every_k_milliseconds(self, k, func):
        """Calls the provided function every k milliseconds."""
        self.callbacks.append((k, func))
        pg.time.set_timer(pg.USEREVENT + len(self.callbacks) - 1, k)

    def listen_for(self, event_type, func):
        """Asks the window to call the provided function when a specified event occurs.

        Supported events:
        - "mousemove": whenever the mouse moves, func(x, y) is called,
                       where (x, y) is the new mouse position
        - "click": whenever the mouse button is clicked, func(x, y) is
                   called, where (x, y) is the position of the click
        """
        self.event_handlers[event_type] = func

    def graphic_at(self, x, y):
        """Returns the topmost graphic that covers position (x, y)."""
        for graphic, graphic_x, graphic_y in self.graphics:
            if graphic._covers(x - graphic_x, y - graphic_y):
                return graphic
        return None


class Rectangle:
    def __init__(
        self,
        width,
        height,
        outline_color,
        fill_color,
    ):
        self.width = width
        self.height = height
        self.surface = pg.Surface((width, height))
        self.surface.fill(outline_color)
        self.fill_color = fill_color
        pg.draw.rect(
            self.surface,
            fill_color,
            pg.Rect(1, 1, width - 2, height - 2),
        )

    def change_fill_color(self, fill_color):
        self.fill_color = fill_color
        pg.draw.rect(
            self.surface,
            fill_color,
            pg.Rect(1, 1, self.width - 2, self.height - 2),
        )

    def _covers(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height


class Circle:
    def __init__(
        self,
        diameter,
        color,
    ):
        self.diameter = diameter
        self.surface = pg.Surface((diameter, diameter), pg.SRCALPHA)
        self.surface.fill((0,0,0,0))
        self.color = color
        self._draw()

    def change_color(self, color):
        self.color = color
        self._draw()

    def _draw(self):
        pg.draw.circle(
            self.surface,
            self.color,
            (self.diameter//2, self.diameter//2),
            self.diameter//2,
        )

    def _covers(self, x, y):
        radius = self.diameter // 2
        return math.sqrt((radius-x)**2 + (radius-y)**2) < self.diameter



class Textbox:
    def __init__(
        self,
        width,  # width of the textbox (in pixels)
        height,  # height of the textbox (in pixels)
        msg,  # message inside the textbox (str)
        text_color,  # color of the text (str)
        font_name="Arial",  # font of the text (str)
        font_size=12,  # font size (int)
        fill_color=None,  # background color of the textbox (None if transparent)
    ):
        font = pg.font.SysFont(font_name, font_size)
        self.surface = pg.Surface((width, height), pg.SRCALPHA)
        if fill_color == None:
            self.surface.fill((0, 0, 0, 0))
        else:
            self.surface.fill(fill_color)
        text = font.render(msg, 1, text_color)
        text_w, text_h = text.get_size()
        self.surface.blit(
            text,
            (width // 2 - text_w // 2, height // 2 - text_h // 2),
        )

    def _covers(self, x, y):
        return False
