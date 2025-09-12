from .box import Box
from .button import Button
from .entry import Entry
from .eventbox import EventBox
from .image import Image
from .label import Label
from .menu_button import MenuButton
from .revealer import Revealer
from .scale import Scale
from .scrolled_window import ScrolledWindow
from .separator import Separator
from .stack import Stack
from .window import Window

def get_children_by_name(widget, name):
    found = []

    def find_child_recursive(_widget, _name):
        if hasattr(_widget, "get_name") and _widget.get_name() == _name:
            found.append(_widget)

        if hasattr(_widget, "get_children"):
            for child in _widget.get_children():
                result = find_child_recursive(child, _name)
                if result:
                    found.append(result)
        elif hasattr(_widget, "get_child"):
            result = find_child_recursive(_widget.get_child(), _name)
            if result:
                found.append(result)

    find_child_recursive(widget, name)
    return found

__all__ = [
    "Box",
    "Button",
    "Entry",
    "EventBox",
    "Image",
    "Label",
    "MenuButton",
    "Revealer",
    "Scale",
    "ScrolledWindow",
    "Separator",
    "Stack",
    "Window",
    "get_children_by_name"
]
