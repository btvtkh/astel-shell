from gi.repository import Gdk, Gtk
from .ipc_service import IpcService

class Application(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id = "com.github.btvtkh.astel-shell"
        )

        IpcService(self)

    def init_css(self, style):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(style)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER,
        )

    def toggle_window(self, name):
        for win in self.get_windows():
            if win.get_name() == name:
                win.set_visible(not win.get_visible())

