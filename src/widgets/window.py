from gi.repository import Gtk, GtkLayerShell
from .base import Base

GTK_LAYER_SHELL_EDGES = [
    GtkLayerShell.Edge.TOP,
    GtkLayerShell.Edge.BOTTOM,
    GtkLayerShell.Edge.LEFT,
    GtkLayerShell.Edge.RIGHT,
]

class Window(Gtk.Window, Base):
    def __init__(
        self,
        namespace = None,
        monitor = None,
        auto_exclusive_zone = False,
        layer = None,
        anchors = [],
        keyboard_mode = None,
        visible = False,
        css_classes = [],
        setup = None,
        width_request = 1,
        height_request = 1,
        **kwargs
    ):
        Gtk.Window.__init__(
            self,
            width_request = width_request,
            height_request = height_request,
            **kwargs
        )

        GtkLayerShell.init_for_window(self)

        Base.__init__(
            self,
            css_classes = css_classes,
            setup = setup
        )

        self.set_namespace(namespace)
        self.set_monitor(monitor)
        self.set_auto_exclusive_zone(auto_exclusive_zone)
        self.set_layer(layer)
        self.set_anchors(anchors)
        self.set_keyboard_mode(keyboard_mode)
        self.set_visible(visible)

    def set_namespace(self, namespace):
        if namespace is not None and namespace != "":
            GtkLayerShell.set_namespace(self, namespace)

    def get_namespace(self):
        return GtkLayerShell.get_namespace(self)

    def set_monitor(self, monitor):
        if monitor != None:
            GtkLayerShell.set_monitor(self, monitor)

    def get_monitor(self):
        return GtkLayerShell.get_monitor(self)

    def set_auto_exclusive_zone(self, auto_exclusive_zone):
        if auto_exclusive_zone:
            GtkLayerShell.auto_exclusive_zone_enable(self)

    def get_auto_exclusive_zone(self):
        return GtkLayerShell.auto_exclusive_zone_is_enabled(self)

    def set_layer(self, layer):
        if layer != None:
            GtkLayerShell.set_layer(self, layer)

    def get_layer(self):
        return GtkLayerShell.get_layer(self)

    def set_anchors(self, edges):
        for edge in edges:
            if edge in GTK_LAYER_SHELL_EDGES:
                GtkLayerShell.set_anchor(self, edge, True)
            else:
                GtkLayerShell.set_anchor(self, edge, False)

    def get_anchors(self):
        ret = []
        for edge in GTK_LAYER_SHELL_EDGES:
            if GtkLayerShell.get_anchor(self, edge):
                ret.append(edge)
        return ret

    def set_keyboard_mode(self, keyboard_mode):
        if keyboard_mode is not None:
            GtkLayerShell.set_keyboard_mode(self, keyboard_mode)

    def get_keyboard_mode(self):
        return GtkLayerShell.get_keyboard_mode(self)
