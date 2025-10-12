from gi.repository import Gtk
from .base import Base

class CenterBox(Gtk.Box, Base):
    def __init__(
        self,
        start_widget = None,
        center_widget = None,
        end_widget = None,
        css_classes = [],
        **kwargs
    ):
        Gtk.Box.__init__(self, **kwargs)
        self._start_widget = None
        self._end_widget = None
        self.set_start_widget(start_widget)
        self.set_center_widget(center_widget)
        self.set_end_widget(end_widget)
        Base.__init__(self, css_classes = css_classes)

    def set_start_widget(self, widget):
        if self._start_widget:
            self._start_widget.destroy()
            self._start_widget = None

        if isinstance(widget, Gtk.Widget):
            self.pack_start(widget, True, True, 0)
            self._start_widget = widget

    def get_start_widget(self):
        return self._start_widget

    def set_end_widget(self, widget):
        if self._end_widget:
            self._end_widget.destroy()
            self._end_widget = None

        if isinstance(widget, Gtk.Widget):
            self.pack_end(widget, True, True, 0)
            self._end_widget = widget

    def get_end_widget(self):
        return self._end_widget

