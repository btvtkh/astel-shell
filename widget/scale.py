from gi.repository import Gtk
from .base import Base

class Scale(Gtk.Scale, Base):
    def __init__(
        self,
        value = 0.0,
        minimum = 0.0,
        maximum = 1.0,
        step = 0.05,
        page = 0.01,
        draw_value = False,
        css_classes = [],
        **kwargs
    ):
        Gtk.Scale.__init__(self, **kwargs)
        self._is_dragging = False
        self.set_adjustment(
            Gtk.Adjustment(
                float(value),
                float(minimum),
                float(maximum),
                float(step),
                float(page),
                float(0)
            )
        )
        self.set_draw_value(draw_value)
        Base.__init__(self, css_classes = css_classes)

        def on_button_press_event(*_):
            self._is_dragging = True

        def on_button_release_event(*_):
            self._is_dragging = False

        def on_key_press_event(*_):
            self._is_dragging = True

        def on_key_release_event(*_):
            self._is_dragging = False

        def on_scroll_event(x, event):
            self._is_dragging = True

            if event.delta_y < 0:
                self.get_adjustment().set_value(self.get_value() + self.get_step())
            else:
                self.get_adjustment().set_value(self.get_value() - self.get_step())

            self._is_dragging = False

        button_press_event_handler = self.connect("button-press-event", on_button_press_event)
        button_release_event_handler = self.connect("button-release-event", on_button_release_event)
        key_press_event_handler = self.connect("key-press-event", on_key_press_event)
        key_release_event_handler = self.connect("key-release-event", on_key_release_event)
        scroll_event_handler = self.connect("scroll-event", on_scroll_event)

        def on_destroy(*_):
            self.disconnect(button_press_event_handler)
            self.disconnect(button_release_event_handler)
            self.disconnect(key_press_event_handler)
            self.disconnect(key_release_event_handler)
            self.disconnect(scroll_event_handler)

        self.connect("destroy", on_destroy)

    def is_dragging(self):
        return self._is_dragging

    def set_value(self, value):
        if not self.is_dragging():
            self.get_adjustment().set_value(float(value))

    def get_value(self):
        return self.get_adjustment().get_value()

    def set_minimum(self, min):
        self.get_adjustment().set_lower(float(min))

    def get_minimum(self):
        return self.get_adjustment().get_lower()

    def set_maximum(self, max):
        self.get_adjustment().set_upper(float(max))

    def get_maximum(self):
        return self.get_adjustment().get_upper()

    def set_step(self, step):
        self.get_adjustment().set_step_increment(float(step))

    def get_step(self):
        return self.get_adjustment().get_step_increment()

    def set_page(self, page):
        self.get_adjustment().set_page_increment(float(page))

    def get_page(self):
        return self.get_adjustment().get_page_increment()
