from gi.repository import AstalHyprland
import widget as Widget

hyprland = AstalHyprland.get_default()

class KbLayout(Widget.Box):
    def __init__(self):
        super().__init__(
            name = "kb-layout",
            children = [
                Widget.Label(
                    name = "kb-label",
                    label = "En"
                )
            ]
        )

        kb_label = Widget.get_child_by_name(self, "kb-label")

        def on_keyboard_layout(x, kb, lt):
            kb_label.set_label(lt[:2])

        hyprland.connect("keyboard-layout", on_keyboard_layout)
