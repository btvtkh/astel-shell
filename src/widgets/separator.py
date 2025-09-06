from gi.repository import Gtk
from .base import Base

class Separator(Gtk.Separator, Base):
    def __init__(
        self,
        css_classes = [],
        setup = None,
        **kwargs
    ):
        Gtk.Separator.__init__(self, **kwargs)
        Base.__init__(
            self,
            css_classes = css_classes,
            setup = setup
        )
