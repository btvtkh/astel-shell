from gi.repository import Gtk

class Base(Gtk.Widget):
    def __init__(
        self,
        visible = True,
        css_classes = [],
        **kwargs
    ):
        Gtk.Widget.__init__(self, **kwargs)
        self.set_css_classes(css_classes)
        self.set_visible(visible)

    def add_css_class(self, css_class):
        if isinstance(css_class, str):
            self.get_style_context().add_class(css_class)

    def remove_css_class(self, css_class):
        if isinstance(css_class, str):
            self.get_style_context().remove_class(css_class)

    def get_css_classes(self):
        return self.get_style_context().list_classes()

    def set_css_classes(self, css_classes):
        for rc in self.get_css_classes():
            self.remove_css_class(rc)

        for ac in css_classes:
            self.add_css_class(ac)
