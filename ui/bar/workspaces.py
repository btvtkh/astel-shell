from gi.repository import AstalHyprland
import widget as Widgets

hyprland = AstalHyprland.get_default()

class WorkspaceButton(Widgets.Button):
    def __init__(self, ws):
        super().__init__(
            child = Widgets.Label(
                label = ws.get_name()
            )
        )

        def on_focused_ws(*_):
            if ws == hyprland.get_focused_workspace():
                self.add_css_class("focused")
            else:
                self.remove_css_class("focused")

        def on_clicked(*_):
            if ws != hyprland.get_focused_workspace():
                ws.focus()

        focused_workspace_handler = hyprland.connect("notify::focused-workspace", on_focused_ws)
        clicked_handler = self.connect("clicked", on_clicked)

        def on_destroy(*_):
            hyprland.disconnect(focused_workspace_handler)
            self.disconnect(clicked_handler)

        self.connect("destroy", on_destroy)
        self.set_css_classes([ws == hyprland.get_focused_workspace() and "focused"])

class Workspaces(Widgets.Box):
    def __init__(self):
        super().__init__(
            name = "workspaces"
        )

        def on_workspaces(*_):
            for child in self.get_children():
                child.destroy()

            wss = hyprland.get_workspaces()
            wss.sort(key = lambda x: x.get_id())
            for ws in wss:
                if not (ws.get_id() >= -99 and ws.get_id() <= -2):
                    self.add(WorkspaceButton(ws))

        hyprland.connect("notify::workspaces", on_workspaces)
        on_workspaces()
