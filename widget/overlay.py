from gi.repository import Gtk
from .base import Base

class Overlay(Gtk.Overlay, Base):
    def __init__(
        self,
        pass_through = False,
        child = None,
        overlays = [],
        css_classes = [],
        **kwargs
    ):
        Gtk.Overlay.__init__(self, **kwargs)
        self._pass_through = pass_through
        self.set_child(child)
        self.set_overlays(overlays)
        Base.__init__(self, css_classes = css_classes)

    def set_pass_through(self, pass_through):
        if isinstance(pass_through, bool) and pass_through != self._pass_through:
            self._pass_through = pass_through

            for child in self.get_children():
                self.set_overlay_pass_through(child, self._pass_through)

    def get_pass_through(self):
        return self._pass_through

    def set_overlays(self, widgets):
        for child in self.get_children():
            if child != self.get_child():
                child.destroy()

        for widget in widgets:
            if isinstance(widget, Gtk.Widget):
                self.add_overlay(widget)
                self.set_overlay_pass_through(widget, self._pass_through)

    def get_overlays(self):
        ret = []

        for child in self.get_children():
            if child != self.get_child():
                ret.append(child)

        return len(ret) > 0 and ret or None

    def set_child(self, widget):
        if self.get_child():
            self.get_child().destroy()

        if isinstance(widget, Gtk.Widget):
            self.add(widget)
