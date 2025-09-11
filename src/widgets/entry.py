from gi.repository import Gtk
from .base import Base

class Entry(Gtk.Entry, Base):
    def __init__(
        self,
        css_classes = [],
        **kwargs
    ):
        Gtk.Entry.__init__(self, **kwargs)
        Base.__init__(self, css_classes = css_classes)
