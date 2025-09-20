from gi.repository import Gtk
from .base import Base

class EventBox(Gtk.EventBox, Base):
    def __init__(
        self,
        css_classes = [],
        **kwargs
    ):
        Gtk.EventBox.__init__(self, **kwargs)
        Base.__init__(self, css_classes = css_classes)
