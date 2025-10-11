import re
from gi.repository import Gio, Gtk, Gdk

class Application(Gtk.Application):
    def __init__(
        self,
        application_id = "com.github.btvtkh.Astel",
        request_handler = None,
        **kwargs
    ):
        Gtk.Application.__init__(
            self,
            application_id = application_id,
            flags = Gio.ApplicationFlags.NON_UNIQUE,
            **kwargs
        )

        self._request_handler = request_handler
        self._screen = Gdk.Screen.get_default()
        self._css_providers = []

    def do_startup(self):
        Gtk.Application.do_startup(self)
        app_id = self.get_application_id()
        app_path = "/" + re.sub(r"\.", "/", self.get_application_id())
        app_node_info = Gio.DBusNodeInfo.new_for_xml(f"""
            <node>
                <interface name="{app_id}.Application">
                    <method name="Request">
                        <arg type="s" name="request" direction="in"/>
                    </method>
                    <method name="Quit"/>
                </interface>
            </node>
        """)

        def dbus_method_handler(connection, sender, object_path, interface, method, parameters, invocation):
            try:
                match method:
                    case "Request":
                        if self._request_handler:
                            self._request_handler(self, parameters[0])
                    case "Quit":
                        self.quit()
            except Exception as e:
                invocation.return_error_literal(
                    Gio.dbus_error_quark(),
                    Gio.DBusError.FAILED,
                    str(e)
                )

        def on_bus_acquired(connection, name):
            try:
                connection.register_object(
                    app_path,
                    app_node_info.lookup_interface(app_id + ".Application"),
                    dbus_method_handler,
                    None,
                    None
                )
            except Exception as e:
                print(e)

        def on_name_lost(*_):
            print("Another instance is already running. Exiting.")
            self.quit()

        Gio.bus_own_name(
            Gio.BusType.SESSION,
            app_id,
            Gio.BusNameOwnerFlags.NONE,
            on_bus_acquired,
            None,
            on_name_lost
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

    def get_window(self, name):
        for win in self.get_windows():
            if win.get_name() == name:
                return win

    def toggle_window(self, name):
        for win in self.get_windows():
            if win.get_name() == name:
                win.set_visible(not win.get_visible())
