from gi.repository import Gtk
from .base import Base

class CheckButton(Gtk.CheckButton, Base):
    def __init__(
        self,
        css_classes = [],
        **kwargs
    ):
        Gtk.CheckButton.__init__(self, **kwargs)
        Base.__init__(self, css_classes = css_classes)
