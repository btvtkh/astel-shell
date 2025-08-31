from gi.repository import Gio, Gdk, Gtk

class Application(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id = "com.github.btvtkh.Astel",
        )

        self._screen = Gdk.Screen.get_default()
        self._css_providers = []

    def do_startup(self):
        Gtk.Application.do_startup(self)

        self._dbus_node_info = Gio.DBusNodeInfo.new_for_xml("""
            <node>
                <interface name="com.github.btvtkh.Astel.Application">
                    <method name="ToggleWindow">
                        <arg type="s" name="window_name" direction="in"/>
                    </method>
                    <method name="Quit"/>
                </interface>
            </node>
        """)

        self.get_dbus_connection().register_object(
            "/com/github/btvtkh/Astel",
            self._dbus_node_info.lookup_interface("com.github.btvtkh.Astel.Application"),
            self._dbus_method_handler,
            None,
            None
        )

    def _dbus_method_handler(
        self,
        connection,
        sender,
        object_path,
        interface_name,
        method_name,
        parameters,
        invocation
    ):
        try:
            match method_name:
                case "ToggleWindow":
                    window_name = parameters.unpack()[0]
                    self.toggle_window(window_name)
                case "Quit":
                    self.quit()
        except Exception as e:
            invocation.return_error_literal(
                Gio.dbus_error_quark(),
                Gio.DBusError.FAILED,
                str(e)
            )

    def reset_css(self):
        for provider in self._css_providers:
            Gtk.StyleContext.remove_provider_for_screen(self._screen, provider)
            self._css_providers.remove(provider)

    def apply_css(self, style, reset):
        if reset:
            self.reset_css()

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(style)
        self._css_providers.append(css_provider)
        Gtk.StyleContext.add_provider_for_screen(
            self._screen,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER,
        )

    def toggle_window(self, name):
        for win in self.get_windows():
            if win.get_name() == name:
                win.set_visible(not win.get_visible())
