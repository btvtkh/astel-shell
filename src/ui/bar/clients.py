from gi.repository import Pango, AstalHyprland
import widget as Widget

hyprland = AstalHyprland.get_default()

class ClientButton(Widget.Button):
    def __init__(self, c):
        super().__init__(
            child = Widget.Label(
                max_width_chars = 15,
                ellipsize = Pango.EllipsizeMode.END,
                label = c.get_initial_class() or "Untitled"
            )
        )

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

        focused_client_handler = hyprland.connect("notify::focused-client", on_focused_client)
        focused_workspace_handler = hyprland.connect("notify::focused-workspace", on_focused_workspace)
        client_moved_handler = hyprland.connect("client-moved", on_focused_workspace)
        clicked_handler = self.connect("clicked", on_clicked)

        def on_destroy(*_):
            hyprland.disconnect(focused_client_handler)
            hyprland.disconnect(focused_workspace_handler)
            hyprland.disconnect(client_moved_handler)
            self.disconnect(clicked_handler)

        self.connect("destroy", on_destroy)
        self.set_css_classes([c == hyprland.get_focused_client() and "focused"])
        self.set_visible(c.get_workspace() == hyprland.get_focused_workspace())

class Clients(Widget.Box):
    def __init__(self):
        super().__init__(
            name = "clients"
        )

        def on_clients(*_):
            self.set_children([
                ClientButton(c) for c in hyprland.get_clients()
            ])

        hyprland.connect("notify::clients", on_clients)
        on_clients()
