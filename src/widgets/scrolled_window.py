from gi.repository import Gtk
from .base import Base

class ScrolledWindow(Gtk.ScrolledWindow, Base):
    def __init__(
        self,
        css_classes = [],
        setup = None,
        **kwargs
    ):
        Gtk.ScrolledWindow.__init__(self, **kwargs)
        Base.__init__(self, css_classes = css_classes, setup = setup)
