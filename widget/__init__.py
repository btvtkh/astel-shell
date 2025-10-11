from .box import Box
from .button import Button
from .checkbutton import CheckButton
from .entry import Entry
from .eventbox import EventBox
from .image import Image
from .label import Label
from .layerwindow import LayerWindow
from .menubutton import MenuButton
from .overlay import Overlay
from .revealer import Revealer
from .scale import Scale
from .scrolledwindow import ScrolledWindow
from .separator import Separator
from .spinner import Spinner
from .stack import Stack
from .switch import Switch

def get_child_by_name(widget, name):
    if hasattr(widget, "get_name") and widget.get_name() == name:
        return widget
    elif hasattr(widget, "get_children"):
       for child in widget.get_children():
            result = get_child_by_name(child, name)
            if result:
                return result
    elif hasattr(widget, "get_child"):
        result = get_child_by_name(widget.get_child(), name)
        if result:
            return result

def get_children_by_name(widget, name):
    found = []

    def find_child_recursive(_widget, _name):
        if hasattr(_widget, "get_name") and _widget.get_name() == _name:
            found.append(_widget)
        elif hasattr(_widget, "get_children"):
            for child in _widget.get_children():
                result = find_child_recursive(child, _name)
                if result:
                    found.append(result)
        elif hasattr(_widget, "get_child"):
            result = find_child_recursive(_widget.get_child(), _name)
            if result:
                found.append(result)

    find_child_recursive(widget, name)
    return len(found) > 0 and found or None

__all__ = [
    "Box",
    "Button",
    "CheckButton",
    "Entry",
    "EventBox",
    "Image",
    "Label",
    "LayerWindow",
    "MenuButton",
    "Overlay",
    "Revealer",
    "Scale",
    "ScrolledWindow",
    "Separator",
    "Spinner",
    "Stack",
    "Switch",
    "get_child_by_name",
    "get_children_by_name"
]
