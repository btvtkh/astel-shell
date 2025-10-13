from gi.repository import GLib, Gtk, AstalNetwork
import widget as Widget

network = AstalNetwork.get_default()
wifi = network.get_wifi()

def AccessPointMenu(ap, ap_stack):
    ret = Widget.Box(
        name = "access-point-menu",
        orientation = Gtk.Orientation.VERTICAL,
        children = [
            Widget.Box(
                css_classes = ["header-box"],
                children = [
                    Widget.Button(
                        name = "access-point-menu-close-button",
                        css_classes = ["close-button"],
                        child = Widget.Image(
                            icon_name = "pan-start-symbolic"
                        )
                    ),
                    Widget.Label(
                        css_classes = ["title-label"],
                        label = ap.get_ssid() or "Unnamed"
                    )
                ]
            ),
            wifi.get_active_access_point() != ap and Widget.Box(
                css_classes = ["password-box"],
                children = [
                    Widget.Entry(
                        name = "access-point-menu-password-entry",
                        css_classes = ["password-entry"],
                        hexpand = True,
                        visibility = False,
                        placeholder_text = "Password"
                    ),
                    Widget.Button(
                        name = "access-point-menu-password-obscure-button",
                        css_classes = ["obscure-button"],
                        child = Widget.Image(
                            icon_name = "view-conceal-symbolic"
                        )
                    )
                ]
            ),
            Widget.Button(
                name = "access-point-menu-connect-button",
                css_classes = ["connect-button"],
                child = Widget.Label(
                    label = wifi.get_active_access_point() == ap and "Disconnect" or "Connect"
                )
            )
        ]
    )

    close_button = Widget.get_child_by_name(ret, "access-point-menu-close-button")
    password_entry = Widget.get_child_by_name(ret, "access-point-menu-password-entry")
    obscure_button = Widget.get_child_by_name(ret, "access-point-menu-password-obscure-button")
    connect_button = Widget.get_child_by_name(ret, "access-point-menu-connect-button")

    def close_menu():
        ap_stack.set_visible_child_name("access-points-list-scrolled-window")

        def on_transition_duration_end():
            ret.destroy()
            return GLib.SOURCE_REMOVE

        GLib.timeout_add(
            ap_stack.get_transition_duration(),
            on_transition_duration_end,
        )

    def on_obscure_button_clicked(*_):
        password_entry.set_visibility(not password_entry.get_visibility())

    def on_password_entry_visibility(*_):
        obscure_button.get_child().set_from_icon_name(
            password_entry.get_visibility() and "view-reveal-symbolic" or "view-conceal-symbolic",
            Gtk.IconSize.BUTTON
        )

    def on_connect_button_clicked(*_):
        if wifi.get_active_access_point() != ap:
            def on_activate(x, res):
                ap.activate_finish(res)
                close_menu()

            if ap.get_requires_password() and password_entry.get_text():
                ap.activate(password_entry.get_text(), on_activate)
            else:
                ap.activate("", on_activate)
        else:
            def on_deactivate(x, res):
                wifi.deactivate_connection_finish(res)
                close_menu()

            wifi.deactivate_connection(on_deactivate)

    def on_close_button_clicked(*_):
        close_menu()

    close_button_clicked_handler = close_button.connect("clicked", on_close_button_clicked)
    connect_button_clicked_handler = connect_button.connect("clicked", on_connect_button_clicked)

    obscure_button_clicked_handler = None
    password_entry_visibility_handler = None

    if password_entry and obscure_button:
        obscure_button_clicked_handler = obscure_button.connect("clicked", on_obscure_button_clicked)
        password_entry_visibility_handler = password_entry.connect("notify::visibility", on_password_entry_visibility)

    def on_destroy(*_):
        close_button.disconnect(close_button_clicked_handler)
        connect_button.disconnect(connect_button_clicked_handler)

        if obscure_button and obscure_button_clicked_handler:
            obscure_button.disconnect(obscure_button_clicked_handler)

        if password_entry and password_entry_visibility_handler:
            password_entry.disconnect(password_entry_visibility_handler)

    ret.connect("destroy", on_destroy)

    return ret

def AccessPointItem(ap, ap_stack):
    ret = Widget.Button(
        name = "access-point-item",
        child = Widget.Box(
            children = [
                Widget.Image(
                    css_classes = ["strength-icon-image"],
                    icon_name = ap.get_icon_name(),
                    pixel_size = 32
                ),
                Widget.Box(
                    orientation = Gtk.Orientation.VERTICAL,
                    hexpand = True,
                    children = [
                        Widget.Label(
                            css_classes = ["ssid-label"],
                            halign = Gtk.Align.START,
                            xalign = 0,
                            label = ap.get_ssid() or "Unnamed"
                        ),
                        Widget.Label(
                            name = "access-point-bssid-label",
                            css_classes = ["bssid-label"],
                            halign = Gtk.Align.START,
                            xalign = 0,
                            label = ap.get_bssid()
                        )
                    ]
                )
            ]
        )
    )

    bssid_label = Widget.get_child_by_name(ret, "access-point-bssid-label")

    def on_active_access_point(*_):
        if wifi.get_active_access_point() == ap:
            bssid_label.set_label("Connected")
        elif bssid_label.get_label() == "Connected":
            bssid_label.set_label(ap.get_bssid())

    def on_clicked(*_):
        ap_menu = AccessPointMenu(ap, ap_stack)
        ap_stack.add_named(ap_menu, ap_menu.get_name())
        ap_stack.set_visible_child(ap_menu)

    active_access_point_handler = wifi.connect("notify::active-access-point", on_active_access_point)
    clicked_handler = ret.connect("clicked", on_clicked)

    def on_destroy(*_):
        wifi.disconnect(active_access_point_handler)
        ret.disconnect(clicked_handler)

    ret.connect("destroy", on_destroy)
    on_active_access_point()

    return ret

def WifiPage():
    ret = Widget.Box(
        name = "wifi-page",
        orientation = Gtk.Orientation.VERTICAL,
        children = [
            Widget.Stack(
                name = "access-points-stack",
                vexpand = True,
                transition_type = Gtk.StackTransitionType.SLIDE_LEFT_RIGHT,
                children = [
                    Widget.ScrolledWindow(
                        name = "access-points-list-scrolled-window",
                        vexpand = True,
                        child = Widget.Box(
                            orientation = Gtk.Orientation.VERTICAL,
                            name = "access-points-list-box"
                        )
                    )
                ]
            ),
            Widget.Box(
                css_classes = ["bottombar-box"],
                children = [
                    Widget.Button(
                        name = "wifi-page-close-button",
                        child = Widget.Image(
                            icon_name = "pan-start-symbolic"
                        )
                    ),
                    Widget.Box(
                        hexpand = True,
                        halign = Gtk.Align.END,
                        children = [
                            Widget.Button(
                                name = "wifi-page-scan-button",
                                child = Widget.Image(
                                    icon_name = "view-refresh-symbolic"
                                )
                            ),
                            Widget.Separator(),
                            Widget.Switch(
                                name = "wifi-page-toggle-switch"
                            )
                        ]
                    )
                ]
            )
        ]
    )

    ap_stack = Widget.get_child_by_name(ret, "access-points-stack")
    ap_list_box = Widget.get_child_by_name(ret, "access-points-list-box")
    page_close_button = Widget.get_child_by_name(ret, "wifi-page-close-button")
    scan_button = Widget.get_child_by_name(ret, "wifi-page-scan-button")
    toggle_switch = Widget.get_child_by_name(ret, "wifi-page-toggle-switch")
    toggle_switch_handled = False

    def on_wifi_enabled(*_):
        if wifi and wifi.get_enabled():
            if not toggle_switch_handled and toggle_switch.get_active() != True:
                toggle_switch.set_active(True)

            if wifi.get_access_points():
                ap_list_box.set_children([
                    AccessPointItem(ap, ap_stack) for ap in wifi.get_access_points()
                ])
            else:
                ap_list_box.set_children([
                    Widget.Spinner(
                        css_classes = ["wait-spinner"],
                        halign = Gtk.Align.CENTER,
                        valign = Gtk.Align.CENTER,
                        hexpand = True,
                        vexpand = True,
                        active = True
                    )
                ])
        else:
            if not toggle_switch_handled and toggle_switch.get_active() != False:
                toggle_switch.set_active(False)

            ap_list_box.set_children([
                Widget.Label(
                    css_classes = ["empty-label"],
                    halign = Gtk.Align.CENTER,
                    valign = Gtk.Align.CENTER,
                    hexpand = True,
                    vexpand = True,
                    label = "Wifi disabled"
                )
            ])

            ap_stack.destroy_named("access-point-menu")
            ap_stack.set_visible_child_name("access-points-list-scrolled-window")

    def on_access_points(*_):
        if wifi and wifi.get_enabled() and wifi.get_access_points():
            ap_list_box.set_children([
                AccessPointItem(ap, ap_stack) for ap in wifi.get_access_points()
            ])

    def on_wifi_scanning(*_):
        if wifi and wifi.get_scanning():
            scan_button.set_child(Widget.Spinner( active = True ))
        elif not isinstance(scan_button.get_child(), Widget.Image):
            scan_button.set_child(Widget.Image(icon_name = "view-refresh-symbolic"))

    def on_scan_button_clicked(*_):
        if wifi and wifi.get_enabled() and not wifi.get_scanning():
            wifi.scan()

    def on_toggle_switch_active(*_):
        nonlocal toggle_switch_handled
        if wifi and wifi.get_enabled() != toggle_switch.get_active():
            toggle_switch_handled = True
            wifi.set_enabled(toggle_switch.get_active())
            toggle_switch_handled = False

    def on_page_close_button_clicked(*_):
        ap_stack.destroy_named("access-point-menu")
        ap_stack.set_visible_child_name("access-points-list-scrolled-window")

    page_close_button.connect("clicked", on_page_close_button_clicked)
    toggle_switch.connect("notify::active", on_toggle_switch_active)
    scan_button.connect("clicked", on_scan_button_clicked)

    if wifi:
        wifi.connect("notify::scanning", on_wifi_scanning)
        wifi.connect("notify::access-points", on_access_points)
        wifi.connect("notify::enabled", on_wifi_enabled)

    on_wifi_enabled()

    return ret
