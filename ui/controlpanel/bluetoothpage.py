from gi.repository import Gtk, AstalBluetooth
import widget as Widget

bluetooth = AstalBluetooth.get_default()
adapter = bluetooth.get_adapter()

def DeviceItem(dev):
    ret = Widget.Button(
        name = "device-item",
        child = Widget.Box(
            children = [
                Widget.Image(
                    css_classes = ["icon-image"],
                    icon_name = dev.get_icon() and f"{dev.get_icon()}-symbolic" or "bluetooth-active-symbolic",
                    pixel_size = 32
                ),
                Widget.Box(
                    orientation = Gtk.Orientation.VERTICAL,
                    hexpand = True,
                    children = [
                        Widget.Label(
                            css_classes = ["name-label"],
                            halign = Gtk.Align.START,
                            xalign = 0,
                            label = dev.get_name() or "Unnamed"
                        ),
                        Widget.Label(
                            name = "device-item-description-label",
                            css_classes = ["address-label"],
                            halign = Gtk.Align.START,
                            xalign = 0,
                            label = dev.get_connected() and "Connected" or dev.get_address()
                        )
                    ]
                )
            ]
        )
    )

    description_label = Widget.get_child_by_name(ret, "device-item-description-label")

    def on_device_connected(*_):
        if dev.get_connected():
            description_label.set_label("Connected")
        else:
            description_label.set_label(dev.get_address())

    def on_clicked(*_):
        if not dev.get_connected():
            def on_connect_device(x, res):
                dev.connect_device_finish(res)

            dev.connect_device(on_connect_device)
        else:
            def on_disconnect_device(x, res):
                dev.disconnect_device_finish(res)

            dev.disconnect_device(on_disconnect_device)

    clicked_handler = ret.connect("clicked", on_clicked)
    connected_handler = dev.connect("notify::connected", on_device_connected)

    def on_destroy(*_):
        ret.disconnect(clicked_handler)
        dev.disconnect(connected_handler)

    ret.connect("destroy", on_destroy)

    return ret

def BluetoothPage():
    ret = Widget.Box(
        name = "bluetooth-page",
        orientation = Gtk.Orientation.VERTICAL,
        children = [
            Widget.Stack(
                name = "devices-stack",
                vexpand = True,
                transition_type = Gtk.StackTransitionType.SLIDE_LEFT_RIGHT,
                children = [
                    Widget.ScrolledWindow(
                        name = "devices-list-scrolled-window",
                        vexpand = True,
                        child = Widget.Box(
                            orientation = Gtk.Orientation.VERTICAL,
                            name = "devices-list-box"
                        )
                    )
                ]
            ),
            Widget.Box(
                css_classes = ["bottombar-box"],
                children = [
                    Widget.Button(
                        name = "bluetooth-page-close-button",
                        child = Widget.Image(
                            icon_name = "pan-start-symbolic"
                        )
                    ),
                    Widget.Box(
                        hexpand = True,
                        halign = Gtk.Align.END,
                        children = [
                            Widget.Button(
                                name = "bluetooth-page-discover-button",
                                child = Widget.Image(
                                    icon_name = "system-search-symbolic"
                                )
                            ),
                            Widget.Separator(),
                            Widget.Switch(
                                name = "bluetooth-page-toggle-switch"
                            )
                        ]
                    )
                ]
            )
        ]
    )

    devices_list_box = Widget.get_child_by_name(ret, "devices-list-box")
    discover_button = Widget.get_child_by_name(ret, "bluetooth-page-discover-button")
    toggle_switch = Widget.get_child_by_name(ret, "bluetooth-page-toggle-switch")
    toggle_switch_handled = False

    def on_adapter_powered(*_):
        if bluetooth and adapter and adapter.get_powered():
            if not toggle_switch_handled and toggle_switch.get_active() != True:
                toggle_switch.set_active(True)

            if bluetooth.get_devices():
                devices_list_box.set_children([
                    DeviceItem(dev) for dev in bluetooth.get_devices()
                ])
            else:
                devices_list_box.set_children([
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

            devices_list_box.set_children([
                Widget.Label(
                    css_classes = ["empty-label"],
                    halign = Gtk.Align.CENTER,
                    valign = Gtk.Align.CENTER,
                    hexpand = True,
                    vexpand = True,
                    label = "Bluetooth disabled"
                )
            ])

    def on_bluetooth_devices(*_):
        if bluetooth and adapter and adapter.get_powered() and bluetooth.get_devices():
            devices_list_box.set_children([
                DeviceItem(dev) for dev in bluetooth.get_devices()
            ])

    def on_toggle_switch_active(*_):
        nonlocal toggle_switch_handled
        if adapter and adapter.get_powered() != toggle_switch.get_active():
            toggle_switch_handled = True
            adapter.set_powered(toggle_switch.get_active())
            toggle_switch_handled = False

    def on_adapter_discovering(*_):
        if adapter and adapter.get_discovering():
            discover_button.set_child(Widget.Spinner(active = True))
        elif not isinstance(discover_button.get_child(), Widget.Image):
            discover_button.set_child(Widget.Image(icon_name = "system-search-symbolic"))

    def on_discover_button_clicked(*_):
        if adapter and adapter.get_powered():
            if adapter.get_discovering():
                adapter.stop_discovery()
            else:
                adapter.start_discovery()

    toggle_switch.connect("notify::active", on_toggle_switch_active)
    discover_button.connect("clicked", on_discover_button_clicked)

    if bluetooth: bluetooth.connect("notify::devices", on_bluetooth_devices)
    if adapter:
        adapter.connect("notify::discovering", on_adapter_discovering)
        adapter.connect("notify::powered", on_adapter_powered)

    on_adapter_powered()

    return ret
