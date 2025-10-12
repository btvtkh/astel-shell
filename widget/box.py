from gi.repository import Gtk
from .base import Base

class Box(Gtk.Box, Base):
    def __init__(
        self,
        children = [],
        css_classes = [],
        **kwargs
    ):
        Gtk.Box.__init__(self, **kwargs)
        self.set_children(children)
        Base.__init__(self, css_classes = css_classes)

    def add_at_index(self, widget, index):
        self.add(widget)
        self.reorder_child(widget, index)

    def set_children(self, widgets):
        for child in self.get_children():
            child.destroy()

        for widget in widgets:
            if isinstance(widget, Gtk.Widget):
                self.add(widget)

