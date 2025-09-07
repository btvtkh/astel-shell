from gi.repository import Gtk
from .base import Base

class Image(Gtk.Image, Base):
    def __init__(
        self,
        css_classes = [],
        setup = None,
        **kwargs
    ):
        Gtk.Image.__init__(self, **kwargs)
        Base.__init__(self, css_classes = css_classes, setup = setup)
