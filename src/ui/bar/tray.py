from gi.repository import Gtk, AstalTray
import widgets as Widget

class TrayItem(Widget.MenuButton):
    def __init__(self, item):
        def on_setup(self):
            item_icon = Widget.get_children_by_name(self, "item-icon")[0]

            def on_gicon(*_):
                item_icon.set_from_gicon(item.get_gicon(), Gtk.IconSize.INVALID)

            def on_menu_model(*_):
                self.set_menu_model(item.get_menu_model())

            def on_action_group(*_):
                self.insert_action_group("dbusmenu", item.get_action_group())

            on_gicon_id = item.connect("notify::gicon", on_gicon)
            on_menu_model_id = item.connect("notify::menu-model", on_menu_model)
            on_action_group_id = item.connect("notify::action-group", on_action_group)

            def on_destroy(*_):
                item.disconnect(on_gicon_id)
                item.disconnect(on_menu_model_id)
                item.disconnect(on_action_group_id)

            self.connect("destroy", on_destroy)
            item_icon.set_from_gicon(item.get_gicon(), Gtk.IconSize.INVALID)
            self.set_menu_model(item.get_menu_model())
            self.insert_action_group("dbusmenu", item.get_action_group())

        super().__init__(
            name = "item-menu-button",
            use_popover = False,
            setup = on_setup,
            child = Widget.Image(
                name = "item-icon",
                pixel_size = 16
            )
        )

class TrayWidget(Widget.Box):
    def __init__(self):
        def on_setup(self):
            tray = AstalTray.get_default()
            items_revealer = Widget.get_children_by_name(self, "items-revealer")[0]
            items_box = Widget.get_children_by_name(self, "items-box")[0]
            reveal_button = Widget.get_children_by_name(self, "reveal-button")[0]
            reveal_icon = Widget.get_children_by_name(self, "reveal-icon")[0]
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

        super().__init__(
            name = "tray-box",
            setup = on_setup,
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
