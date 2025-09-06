from gi.repository import Gtk
from .base import Base

class Box(Gtk.Box, Base):
    def __init__(
        self,
        children = [],
        css_classes = [],
        setup = None,
        **kwargs
    ):
        Gtk.Box.__init__(self, **kwargs)
        Base.__init__(
            self,
            css_classes = css_classes,
            setup = setup
        )

        self.set_children(children)

    def set_children(self, widgets):
        for child in self.get_children():
            child.destroy()

        for widget in widgets:
            self.add(widget)
