from gi.repository import Gtk
from .base import Base

class Revealer(Gtk.Revealer, Base):
    def __init__(
        self,
        css_classes = [],
        **kwargs
    ):
        Gtk.Revealer.__init__(self, **kwargs)
        Base.__init__(self, css_classes = css_classes)

    def reveal(self):
        self.set_reveal_child(True)

    def conceal(self):
        self.set_reveal_child(False)

    def set_child(self, widget):
        if self.get_child():
            self.get_child().destroy()

        if isinstance(widget, Gtk.Widget):
            self.add(widget)
