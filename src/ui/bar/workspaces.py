from gi.repository import AstalHyprland
import widgets as Widgets

class WorkspaceButton(Widgets.Button):
    def __init__(self, ws):
        hyprland = AstalHyprland.get_default()

        def on_focused_ws(*_):
            if ws == hyprland.get_focused_workspace():
                self.get_style_context().add_class("focused")
            else:
                self.get_style_context().remove_class("focused")

        def on_clicked(*_):
            if ws != hyprland.get_focused_workspace():
                ws.focus()

        def on_button_setup(self):
            on_focused_ws_id = hyprland.connect("notify::focused-workspace", on_focused_ws)
            on_clicked_id = self.connect("clicked", on_clicked)

            def on_destroy(*_):
                hyprland.disconnect(on_focused_ws_id)
                self.disconnect(on_clicked_id)

            self.connect("destroy", on_destroy)

        super().__init__(
            css_classes = [
                "workspace-button",
                ws == hyprland.get_focused_workspace() and "focused" or ""
            ],
            setup = on_button_setup,
            child = Widgets.Label(
                label = ws.get_name()
            )
        )

class WorkspacesWidget(Widgets.Box):
    def __init__(self):
        hyprland = AstalHyprland.get_default()

        def on_workspaces(*_):
            for child in self.get_children():
                child.destroy()

            wss = hyprland.get_workspaces()
            wss.sort(key = lambda x: x.get_id())
            for ws in wss:
                if not (ws.get_id() >= -99 and ws.get_id() <= -2):
                    self.add(WorkspaceButton(ws))

        def on_box_setup(*_):
            hyprland.connect("notify::workspaces", on_workspaces)

        super().__init__(
            css_classes = ["workspaces-box"],
            setup = on_box_setup
        )

        on_workspaces()
