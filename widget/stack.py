from gi.repository import Gtk
from .base import Base

class Stack(Gtk.Stack, Base):
    def __init__(
        self,
        children = [],
        css_classes = [],
        **kwargs
    ):
        Gtk.Stack.__init__(self, **kwargs)
        self.set_children(children)

        Base.__init__(self, css_classes = css_classes)

    def destroy_named(self, name):
        for child in self.get_children():
            if child.get_name() == name:
                child.destroy()

    def set_children(self, widgets):
        for child in self.get_children():
            child.destroy()

        for widget in widgets:
            if isinstance(widget, Gtk.Widget) and widget.get_name():
                self.add_named(widget, widget.get_name())

