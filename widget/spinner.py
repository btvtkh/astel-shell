from gi.repository import Gtk
from .base import Base

class Spinner(Gtk.Spinner, Base):
    def __init__(
        self,
        css_classes = [],
        **kwargs
    ):
        Gtk.Spinner.__init__(self, **kwargs)
        Base.__init__(self, css_classes = css_classes)
