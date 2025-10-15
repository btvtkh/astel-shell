import re
from gi.repository import Gio, GioUnix, Gtk, Gdk, GtkLayerShell, Pango, AstalHyprland
import widget as Widget
from .sidebar import Sidebar

hyprland = AstalHyprland.get_default()

def launch_app(app):
    desktop = GioUnix.DesktopAppInfo.new(app.get_id())
    terminal = desktop.get_string("Terminal") == "true" and Gio.AppInfo.get_default_for_uri_scheme('terminal')

    hyprland.dispatch("exec", f"{
        terminal and
            f"{terminal.get_executable()} -e {app.get_executable()}"
        or
            re.search("^env", app.get_executable()) and
                re.sub("%.", "", app.get_commandline())
            or
                app.get_executable()
    }")

def get_apps(query):
    query = re.escape(query)
    filtered = []
    filtered_any = []

    for app in Gio.AppInfo.get_all():
        if app.should_show():
            if re.search("^" + query, str(app.get_name()).casefold()):
                filtered.append(app)
            elif re.search(query, str(app.get_name()).casefold()):
                filtered_any.append(app)
            elif re.search(query, str(app.get_executable()).casefold()):
                filtered_any.append(app)
            elif re.search(query, str(app.get_description()).casefold()):
                filtered_any.append(app)

    filtered.sort(key = lambda app: app.get_name())
    filtered_any.sort(key = lambda app: app.get_name())
    filtered += filtered_any

    del filtered_any
    return filtered

def AppButton(window, app):
    ret = Widget.Button(
        css_classes = ["app-button"],
        child = Widget.Box(
            orientation = Gtk.Orientation.VERTICAL,
            children = [
                Widget.Label(
                    css_classes = ["name-label"],
                    halign = Gtk.Align.START,
                    xalign = 0,
                    ellipsize = Pango.EllipsizeMode.END,
                    max_width_chars = 45,
                    label = app.get_name()
                ),
                Widget.Label(
                    css_classes = ["description-label"],
                    halign = Gtk.Align.START,
                    xalign = 0,
                    ellipsize = Pango.EllipsizeMode.END,
                    max_width_chars = 45,
                    label = app.get_description() or "No description"
                )
            ]
        )
    )

    def on_clicked(*_):
        window.hide()
        launch_app(app)

    def on_key_press(x, event):
         if event.keyval == Gdk.KEY_Return:
            on_clicked()

    on_clicked_id = ret.connect("clicked", on_clicked)
    on_key_press_id = ret.connect("key-press-event", on_key_press)

    def on_destroy(*_):
        ret.disconnect(on_clicked_id)
        ret.disconnect(on_key_press_id)

    ret.connect("destroy", on_destroy)

    return ret

def Launcher():
    ret = Widget.LayerWindow(
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
        child = Widget.Box(
            children = [
                Widget.Box(
                    hexpand = False,
                    orientation = Gtk.Orientation.VERTICAL,
                    children = [
                        Widget.EventBox(
                            name = "outside-eventbox",
                            vexpand = True
                        ),
                        Widget.Box(
                            css_classes = ["main-box"],
                            hexpand = False,
                            vexpand = False,
                            children = [
                                Sidebar(),
                                Widget.Box(
                                    orientation = Gtk.Orientation.VERTICAL,
                                    hexpand = True,
                                    vexpand = True,
                                    children = [
                                        Widget.Entry(
                                            name = "search-entry",
                                            placeholder_text = "Search..."
                                        ),
                                        Widget.Separator(),
                                        Widget.ScrolledWindow(
                                            name = "apps-scrolled-window",
                                            vexpand = True,
                                            child = Widget.Box(
                                                name = "apps-box",
                                                orientation = Gtk.Orientation.VERTICAL
                                            )
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                Widget.EventBox(
                    name = "outside-eventbox",
                    hexpand = True
                )
            ]
        )
    )

    search_entry = Widget.get_child_by_name(ret, "search-entry")
    apps_scrolled_window = Widget.get_child_by_name(ret, "apps-scrolled-window")
    apps_box = Widget.get_child_by_name(ret, "apps-box")
    power_button = Widget.get_child_by_name(ret, "power-button")

    def on_outside_click(*_):
        ret.hide()

    def on_window_key_press(x, event):
        if event.keyval == Gdk.KEY_Escape:
            ret.hide()

    def on_visible(*_):
        if ret.get_visible():
            search_entry.set_text("")
            search_entry.set_position(-1)
            search_entry.select_region(0, -1)
            search_entry.grab_focus()
            apps_scrolled_window.get_vadjustment().set_value(
                apps_scrolled_window.get_vadjustment().get_lower()
            )

            if not apps_box.get_children():
                apps_box.set_children([
                    AppButton(ret, app) for app in get_apps("")
                ])

    def on_search_text(*_):
        apps_list = get_apps(search_entry.get_text())

        if len(apps_list) > 0:
            apps_box.set_children([
                AppButton(ret, app) for app in apps_list
            ])

            apps_scrolled_window.get_vadjustment().set_value(
                apps_scrolled_window.get_vadjustment().get_lower()
            )
        elif not isinstance(apps_box.get_children()[0], Widget.Label):
            apps_box.set_children([
                Widget.Label(
                    css_classes = ["empty-label"],
                    halign = Gtk.Align.CENTER,
                    valign = Gtk.Align.CENTER,
                    hexpand = True,
                    vexpand = True,
                    label = "No match found"
                )
            ])

    def on_search_activate(*_):
        first_child = apps_box.get_children()[0]
        if first_child and isinstance(first_child, Widget.Button):
                first_child.clicked()

    def on_power_button_clicked(*_):
        ret.get_application().toggle_window("Powermenu")

    search_entry.connect("activate", on_search_activate)
    search_entry.connect("notify::text", on_search_text)
    ret.connect("key-press-event", on_window_key_press)
    ret.connect("notify::visible", on_visible)
    power_button.connect("clicked", on_power_button_clicked)

    for i in Widget.get_children_by_name(ret, "outside-eventbox"):
        i.connect("button-press-event", on_outside_click)

    return ret
