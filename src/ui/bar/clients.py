from gi.repository import Pango, AstalHyprland
import widgets as Widgets

class ClientButton(Widgets.Button):
    def __init__(self, c):
        super().__init__(
            name = "client-button",
            child = Widgets.Label(
                max_width_chars = 15,
                ellipsize = Pango.EllipsizeMode.END,
                label = c.get_initial_class() or "Untitled"
            )
        )

        hyprland = AstalHyprland.get_default()

        def on_focused_client(*_):
            if c == hyprland.get_focused_client():
                self.add_css_class("focused")
            else:
                self.remove_css_class("focused")

        def on_focused_workspace(*_):
            self.set_visible(c.get_workspace() == hyprland.get_focused_workspace())

        def on_clicked(*_):
            if c != hyprland.get_focused_client():
                c.focus()

            if c.get_floating():
                hyprland.dispatch("alterzorder", f"top, {c.get_address()}")

        on_focused_c_id = hyprland.connect("notify::focused-client", on_focused_client)
        on_focused_ws_id = hyprland.connect("notify::focused-workspace", on_focused_workspace)
        on_c_moved_id = hyprland.connect("client-moved", on_focused_workspace)
        on_clicked_id = self.connect("clicked", on_clicked)

        def on_destroy(*_):
            hyprland.disconnect(on_focused_c_id)
            hyprland.disconnect(on_focused_ws_id)
            hyprland.disconnect(on_c_moved_id)
            self.disconnect(on_clicked_id)

        self.connect("destroy", on_destroy)
        self.set_css_classes([c == hyprland.get_focused_client() and "focused"])
        self.set_visible(c.get_workspace() == hyprland.get_focused_workspace())

class Clients(Widgets.Box):
    def __init__(self):
        super().__init__(
            name = "clients-box"
        )

        hyprland = AstalHyprland.get_default()

        def on_clients(*_):
            self.set_children([
                ClientButton(c) for c in hyprland.get_clients()
            ])

        hyprland.connect("notify::clients", on_clients)
        on_clients()
