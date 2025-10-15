from gi.repository import Gtk, Gdk, GtkLayerShell
from .base import Base

GTK_LAYER_SHELL_EDGES = [
    GtkLayerShell.Edge.TOP,
    GtkLayerShell.Edge.BOTTOM,
    GtkLayerShell.Edge.LEFT,
    GtkLayerShell.Edge.RIGHT,
]

class LayerWindow(Gtk.Window, Base):
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
        self.set_namespace(namespace)
        self.set_monitor(monitor)
        self.set_auto_exclusive_zone(auto_exclusive_zone)
        self.set_layer(layer)
        self.set_anchors(anchors)
        self.set_keyboard_mode(keyboard_mode)
        Base.__init__(self, css_classes = css_classes)
        self.set_visible(visible)

    def set_namespace(self, namespace):
        if isinstance(namespace, str) and namespace != "":
            GtkLayerShell.set_namespace(self, namespace)

    def get_namespace(self):
        return GtkLayerShell.get_namespace(self)

    def set_monitor(self, monitor):
        if isinstance(monitor, Gdk.Monitor):
            GtkLayerShell.set_monitor(self, monitor)

    def get_monitor(self):
        return GtkLayerShell.get_monitor(self)

    def set_auto_exclusive_zone(self, auto_exclusive_zone):
        if isinstance(auto_exclusive_zone, bool):
            if auto_exclusive_zone:
                GtkLayerShell.auto_exclusive_zone_enable(self)
            else:
                GtkLayerShell.set_exclusive_zone(self, 0)

    def get_auto_exclusive_zone(self):
        return GtkLayerShell.auto_exclusive_zone_is_enabled(self)

    def set_layer(self, layer):
        if isinstance(layer, GtkLayerShell.Layer):
            GtkLayerShell.set_layer(self, layer)

    def get_layer(self):
        return GtkLayerShell.get_layer(self)

    def set_anchors(self, edges):
        for edge in GTK_LAYER_SHELL_EDGES:
            GtkLayerShell.set_anchor(self, edge, edge in edges)

    def get_anchors(self):
        ret = []

        for edge in GTK_LAYER_SHELL_EDGES:
            if GtkLayerShell.get_anchor(self, edge):
                ret.append(edge)

        return len(ret) > 0 and ret or None

    def set_keyboard_mode(self, keyboard_mode):
        if isinstance(keyboard_mode, GtkLayerShell.KeyboardMode):
            GtkLayerShell.set_keyboard_mode(self, keyboard_mode)

    def get_keyboard_mode(self):
        return GtkLayerShell.get_keyboard_mode(self)

    def set_child(self, widget):
        child = self.get_child()
        if child:
            child.destroy()

        if isinstance(widget, Gtk.Widget):
            self.add(widget)
