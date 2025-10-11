from gi.repository import Gtk, Pango, AstalHyprland
import widget as Widget

hyprland = AstalHyprland.get_default()

def ClientButton(c):
    ret = Widget.Box(
        css_classes = ["client-box"],
        hexpand = False,
        children = [
            Widget.Overlay(
                name = "client-overlay",
                pass_through = True,
                overlay = [
                    Widget.Box(
                        name = "client-indicator",
                        css_classes = ["indicator"],
                        valign = Gtk.Align.END,
                        hexpand = True
                    )
                ],
                child = Widget.Button(
                    name = "client-button",
                    child = Widget.Label(
                        max_width_chars = 15,
                        ellipsize = Pango.EllipsizeMode.END,
                        label = c.get_initial_class() or "Untitled"
                    )
                )
            )
        ]
    )

    button = Widget.get_child_by_name(ret, "client-button")

    def on_focused_client(*_):
        if c == hyprland.get_focused_client():
            ret.add_css_class("focused")
        else:
            ret.remove_css_class("focused")

    def on_focused_workspace(*_):
        ret.set_visible(c.get_workspace() == hyprland.get_focused_workspace())

    def on_clicked(*_):
        if c != hyprland.get_focused_client():
            c.focus()

        if c.get_floating():
            hyprland.dispatch("alterzorder", f"top, {c.get_address()}")

    focused_client_handler = hyprland.connect("notify::focused-client", on_focused_client)
    focused_workspace_handler = hyprland.connect("notify::focused-workspace", on_focused_workspace)
    client_moved_handler = hyprland.connect("client-moved", on_focused_workspace)
    clicked_handler = button.connect("clicked", on_clicked)

    def on_destroy(*_):
        hyprland.disconnect(focused_client_handler)
        hyprland.disconnect(focused_workspace_handler)
        hyprland.disconnect(client_moved_handler)
        button.disconnect(clicked_handler)

    ret.connect("destroy", on_destroy)
    ret.set_visible(c.get_workspace() == hyprland.get_focused_workspace())
    ret.add_css_class(c == hyprland.get_focused_client() and "focused")

    return ret

def Clients():
    ret = Widget.Box(name = "clients")

    def on_clients(*_):
        ret.set_children([
            ClientButton(c) for c in hyprland.get_clients()
        ])

    hyprland.connect("notify::clients", on_clients)
    on_clients()

    return ret
