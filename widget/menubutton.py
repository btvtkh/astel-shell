from gi.repository import Gtk
from .base import Base

class MenuButton(Gtk.MenuButton, Base):
    def __init__(
        self,
        css_classes = [],
        **kwargs
    ):
        Gtk.MenuButton.__init__(self, **kwargs)
        Base.__init__(self, css_classes = css_classes)

    def set_child(self, widget):
        child = self.get_child()
        if child:
            child.destroy()

        if isinstance(widget, Gtk.Widget):
            self.add(widget)
