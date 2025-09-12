from gi.repository import AstalHyprland
import widgets as Widget

class KbLayout(Widget.Box):
    def __init__(self):
        super().__init__(
            name = "kb-layout-box",
            children = [
                Widget.Label(
                    name = "kb-label",
                    label = "En"
                )
            ]
        )

        hyprland = AstalHyprland.get_default()
        kb_label = Widget.get_children_by_name(self, "kb-label")[0]

        def on_keyboard_layout(x, kb, lt):
            kb_label.set_label(lt[:2])

        hyprland.connect("keyboard-layout", on_keyboard_layout)
