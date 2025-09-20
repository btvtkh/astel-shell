from gi.repository import Gtk
from .base import Base

class Label(Gtk.Label, Base):
    def __init__(
        self,
        css_classes = [],
        **kwargs
    ):
        Gtk.Label.__init__(self, **kwargs)
        Base.__init__(self, css_classes = css_classes)
