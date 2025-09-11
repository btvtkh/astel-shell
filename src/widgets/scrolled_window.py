from gi.repository import Gtk
from .base import Base

class ScrolledWindow(Gtk.ScrolledWindow, Base):
    def __init__(
        self,
        css_classes = [],
        **kwargs
    ):
        Gtk.ScrolledWindow.__init__(self, **kwargs)
        Base.__init__(self, css_classes = css_classes)
