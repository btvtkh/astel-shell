from gi.repository import Gtk, AstalTray
import widget as Widget

tray = AstalTray.get_default()

class TrayItem(Widget.MenuButton):
    def __init__(self, item):
        super().__init__(
            css_classes = ["menu-button"],
            use_popover = False,
            child = Widget.Image(
                name = "item-icon",
                pixel_size = 16
            )
        )

        item_icon = Widget.get_child_by_name(self, "item-icon")

        def on_gicon(*_):
            item_icon.set_from_gicon(item.get_gicon(), Gtk.IconSize.INVALID)

        def on_menu_model(*_):
            self.set_menu_model(item.get_menu_model())

        def on_action_group(*_):
            self.insert_action_group("dbusmenu", item.get_action_group())

        gicon_handler = item.connect("notify::gicon", on_gicon)
        menu_model_handler = item.connect("notify::menu-model", on_menu_model)
        action_group_handler = item.connect("notify::action-group", on_action_group)

        def on_destroy(*_):
            item.disconnect(gicon_handler)
            item.disconnect(menu_model_handler)
            item.disconnect(action_group_handler)

        self.connect("destroy", on_destroy)
        item_icon.set_from_gicon(item.get_gicon(), Gtk.IconSize.INVALID)
        self.set_menu_model(item.get_menu_model())
        self.insert_action_group("dbusmenu", item.get_action_group())

class Tray(Widget.Box):
    def __init__(self):
        super().__init__(
            name = "tray",
            children = [
                Widget.Button(
                    name = "reveal-button",
                    child = Widget.Image(
                        name = "reveal-icon",
                        icon_name = "pan-start-symbolic",
                    )
                ),
                Widget.Revealer(
                    name = "items-revealer",
                    reveal_child = False,
                    transition_type = Gtk.RevealerTransitionType.SLIDE_RIGHT,
                    child = Widget.Box(
                        name = "items-box"
                    )
                )
            ]
        )

        items_revealer = Widget.get_child_by_name(self, "items-revealer")
        items_box = Widget.get_child_by_name(self, "items-box")
        reveal_button = Widget.get_child_by_name(self, "reveal-button")
        reveal_icon = Widget.get_child_by_name(self, "reveal-icon")
        items = {}

        def on_reveal_button_clicked(*_):
            items_revealer.set_reveal_child(not items_revealer.get_reveal_child())
            reveal_icon.set_from_icon_name(
                items_revealer.get_reveal_child() and "pan-end-symbolic" or "pan-start-symbolic",
                Gtk.IconSize.BUTTON
            )

        def on_item_added(x, id):
            tray_item = TrayItem(tray.get_item(id))
            items[id] = tray_item
            items_box.add(tray_item)

        def on_item_removed(x, id):
            items[id].destroy()
            del items[id]

        reveal_button.connect("clicked", on_reveal_button_clicked)
        tray.connect("item-removed", on_item_removed)
        tray.connect("item-added", on_item_added)
