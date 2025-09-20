from gi.repository import GLib, Gtk, GtkLayerShell, AstalNotifd
import widget as Widget
from .notification import Notification

notifd = AstalNotifd.get_default()

class AnimatedNotification(Widget.Box):
    def __init__(self, n):
        super().__init__(
            css_classes = ["animated-notification-box"],
            halign = Gtk.Align.END,
            children = [
                Widget.Revealer(
                    name = "outer-revealer",
                    transition_type = Gtk.RevealerTransitionType.SLIDE_DOWN,
                    child = Widget.Revealer(
                        name = "inner-revealer",
                        transition_type = Gtk.RevealerTransitionType.SLIDE_LEFT,
                        child = Notification(n)
                    )
                )
            ]
        )

class Notifications(Widget.LayerWindow):
    def __init__(self):
        super().__init__(
            name = "Notifications",
            namespace = "Astel-Notifications",
            layer = GtkLayerShell.Layer.TOP,
            anchors = [
                GtkLayerShell.Edge.TOP,
                GtkLayerShell.Edge.RIGHT
            ],
            child = Widget.Box(
                css_classes = ["main-box"],
                orientation = Gtk.Orientation.VERTICAL,
                valign = Gtk.Align.START
            )
        )

        notifications = {}
        main_box = self.get_child()

        def on_resolved(x, id, reason):
            if not id in notifications:
                return

            notification = notifications[id]
            outer_revealer = Widget.get_child_by_name(notification, "outer-revealer")
            inner_revealer = Widget.get_child_by_name(notification, "inner-revealer")

            def on_outer_timeout_end():
                notification.destroy()

                if id in notifications:
                    del notifications[id]

                if self.get_visible() and not main_box.get_children():
                    self.hide()

                return GLib.SOURCE_REMOVE

            def on_inner_timeout_end():
                outer_revealer.set_reveal_child(False)
                GLib.timeout_add(
                    outer_revealer.get_transition_duration(),
                    on_outer_timeout_end
                )
                return GLib.SOURCE_REMOVE

            inner_revealer.set_reveal_child(False)
            GLib.timeout_add(
                inner_revealer.get_transition_duration(),
                on_inner_timeout_end
            )

        def on_notified(x, id, replaced):
            n = notifd.get_notification(id)
            notification = AnimatedNotification(n)
            notifications[id] = notification
            outer_revealer = Widget.get_child_by_name(notification, "outer-revealer")
            inner_revealer = Widget.get_child_by_name(notification, "inner-revealer")

            if not self.get_visible():
                self.show()

            main_box.insert(notification, 0)
            outer_revealer.set_reveal_child(True)

            def on_outer_timeout_end():
                inner_revealer.set_reveal_child(True)
                return GLib.SOURCE_REMOVE

            GLib.timeout_add(
                outer_revealer.get_transition_duration(),
                on_outer_timeout_end
            )

            def on_display_timeout_end():
                on_resolved(None, id, False)
                return GLib.SOURCE_REMOVE

            GLib.timeout_add_seconds(5, on_display_timeout_end)

        notifd.connect("resolved", on_resolved)
        notifd.connect("notified", on_notified)

        ns = notifd.get_notifications()
        ns.sort(key = lambda x: x.get_id())
        for n in ns:
            on_notified(None, n.get_id(), False)
