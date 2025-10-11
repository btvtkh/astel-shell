import time
from datetime import datetime
from gi.repository import GLib
import widget as Widget

def calc_interval(interval):
    return interval - int(time.time()) % interval

def Clock():
    ret = Widget.Box(
        name = "clock",
        children = [
            Widget.Label(
                name = "time-label",
            ),
            Widget.Separator(),
            Widget.Label(
                name = "date-label"
            )
        ]
    )

    time_label = Widget.get_child_by_name(ret, "time-label")
    date_label = Widget.get_child_by_name(ret, "date-label")

    def timeout_callback():
        date_label.set_label(datetime.now().strftime("%d %b, %a"))
        time_label.set_label(datetime.now().strftime("%H:%M"))
        GLib.timeout_add_seconds(calc_interval(60), timeout_callback)
        return GLib.SOURCE_REMOVE

    timeout_callback()

    return ret
