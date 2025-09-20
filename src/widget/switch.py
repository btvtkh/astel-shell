from gi.repository import Gtk
from .base import Base

class Switch(Gtk.Switch, Base):
    def __init__(
        self,
        css_classes = [],
        **kwargs
    ):
        Gtk.Switch.__init__(self, **kwargs)
        Base.__init__(self, css_classes = css_classes)
