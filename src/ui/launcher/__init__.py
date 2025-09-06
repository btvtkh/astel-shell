import re
from gi.repository import Gio, Gdk, Gtk, GtkLayerShell, Pango, AstalHyprland
import widgets as Widgets
from .sidebar import SidebarWidget

def launch_app(app):
    desktop = Gio.DesktopAppInfo.new(app.get_id())
    term = desktop.get_string("Terminal") == "true" and Gio.AppInfo.get_default_for_uri_scheme('terminal') or False

    AstalHyprland.get_default().dispatch("exec", f"{
        term and
            f"{term.get_executable()} -e {app.get_executable()}"
        or
            re.search("^env", app.get_executable()) and
                re.sub("%a", "", app.get_commandline())
            or
                app.get_executable()
    }")

def filter_apps(apps, query):
    query = re.escape(query)
    filtered = []
    filtered_any = []

    for app in apps:
        if app.should_show():
            if re.search("^" + query, app.get_name().casefold()):
                filtered.append(app)
            elif re.search(query, app.get_name().casefold()):
                filtered_any.append(app)
            elif re.search(query, app.get_executable().casefold()):
                filtered_any.append(app)
            elif re.search(query, app.get_description().casefold()):
                filtered_any.append(app)

    filtered.sort(key = lambda app: app.get_name())
    filtered_any.sort(key = lambda app: app.get_name())
    filtered += filtered_any

    del filtered_any
    return filtered

class AppButton(Widgets.Button):
    def __init__(self, window, app):
        def on_clicked(*_):
            window.hide()
            launch_app(app)

        def on_key_press(x, event):
             if event.keyval == Gdk.KEY_Return:
                on_clicked()

        def on_button_setup(self):
            on_clicked_id = self.connect("clicked", on_clicked)
            on_key_press_id = self.connect("key-press-event", on_key_press)

            def on_destroy(*_):
                self.disconnect(on_clicked_id)
                self.disconnect(on_key_press_id)

            self.connect("destroy", on_destroy)

        super().__init__(
            css_classes = ["app-button"],
            setup = on_button_setup,
            child = Widgets.Box(
                orientation = Gtk.Orientation.VERTICAL,
                children = [
                    Widgets.Label(
                        css_classes = ["name-label"],
                        halign = Gtk.Align.START,
                        xalign = 0,
                        ellipsize = Pango.EllipsizeMode.END,
                        max_width_chars = 45,
                        label = app.get_name()
                    ),
                    Widgets.Label(
                        css_classes = ["description-label"],
                        halign = Gtk.Align.START,
                        xalign = 0,
                        ellipsize = Pango.EllipsizeMode.END,
                        max_width_chars = 45,
                        label = app.get_description()
                    )
                ]
            )
        )

class Launcher(Widgets.Window):
    def __init__(self):
        search_entry = Widgets.Entry(
            css_classes = ["search-entry"],
            placeholder_text = "Search..."
        )

        apps_box = Widgets.Box(
            orientation = Gtk.Orientation.VERTICAL
        )

        apps_scrolled_window = Widgets.ScrolledWindow(
            css_classes = ["apps-scrolled-window"],
            hexpand = False,
            vexpand = False,
            child = apps_box
        )

        def on_window_key_press(self, event):
            if event.keyval == Gdk.KEY_Escape:
                self.hide()

        def on_evetbox_click(*_):
            self.hide()

        def on_visible(*_):
            if self.get_visible():
                search_entry.set_text("")
                search_entry.set_position(-1)
                search_entry.select_region(0, -1)
                search_entry.grab_focus()
                apps_scrolled_window.get_vadjustment().set_value(
                    apps_scrolled_window.get_vadjustment().get_lower()
                )

                if not apps_box.get_children():
                    apps_box.set_children([
                        AppButton(self, app) for app in filter_apps(Gio.AppInfo.get_all(), "")
                    ])

                self.show_all()

        def on_search_text(*_):
            apps_list = filter_apps(Gio.AppInfo.get_all(), search_entry.get_text())

            if len(apps_list) > 0:
                apps_box.set_children([AppButton(self, app) for app in apps_list])
            else:
                apps_box.set_children([
                    Widgets.Box(
                        halign = Gtk.Align.CENTER,
                        valign = Gtk.Align.CENTER,
                        hexpand = True,
                        vexpand = True,
                        children = [
                            Widgets.Label(
                                css_classes = ["no-match-label"],
                                label = "No match found"
                            )
                        ]
                    )
                ])

            apps_box.show_all()

        def on_search_activate(*_):
            if apps_box.get_children():
                if isinstance(apps_box.get_children()[0], Gtk.Button):
                    apps_box.get_children()[0].clicked()

        def on_window_setup(self):
            search_entry.connect("activate", on_search_activate)
            search_entry.connect("notify::text", on_search_text)
            self.connect("key-press-event", on_window_key_press)
            self.connect("notify::visible", on_visible)

        super().__init__(
            name = "Launcher",
            namespace = "Astel-Launcher",
            layer = GtkLayerShell.Layer.TOP,
            anchors = [
                GtkLayerShell.Edge.TOP,
                GtkLayerShell.Edge.BOTTOM,
                GtkLayerShell.Edge.RIGHT,
                GtkLayerShell.Edge.LEFT
            ],
            keyboard_mode = GtkLayerShell.KeyboardMode.ON_DEMAND,
            setup = on_window_setup,
            css_classes = ["launcher-window"],
            child = Widgets.Box(
                children = [
                    Widgets.Box(
                        hexpand = False,
                        orientation = Gtk.Orientation.VERTICAL,
                        children = [
                            Widgets.EventBox(
                                vexpand = True,
                                setup = lambda w: w.connect(
                                    "button-press-event",
                                    on_evetbox_click
                                )
                            ),
                            Widgets.Box(
                                css_classes = ["launcher-box"],
                                children = [
                                    SidebarWidget(self),
                                    Widgets.Box(
                                        orientation = Gtk.Orientation.VERTICAL,
                                        children = [
                                            search_entry,
                                            Widgets.Separator(),
                                            apps_scrolled_window
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    Widgets.EventBox(
                        hexpand = True,
                        setup = lambda w: w.connect(
                            "button-press-event",
                            on_evetbox_click
                        )
                    )
                ]
            )
        )
