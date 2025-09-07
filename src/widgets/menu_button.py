from gi.repository import Gtk
from .base import Base

class MenuButton(Gtk.MenuButton, Base):
    def __init__(
        self,
        css_classes = [],
        setup = None,
        **kwargs
    ):
        Gtk.MenuButton.__init__(self, **kwargs)
        Base.__init__(self, css_classes = css_classes, setup = setup)
