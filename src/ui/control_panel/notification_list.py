from gi.repository import GLib, Gtk, AstalNotifd
import widgets as Widget
from ui.notifications.notification import Notification

class AnimatedNotification(Widget.Box):
    def __init__(self, n):
        super().__init__(
            children = [
                Widget.Revealer(
                    name = "outer-revealer",
                    transition_type = Gtk.RevealerTransitionType.SLIDE_DOWN,
                    child = Notification(n)
                )
            ]
        )

        outer_revealer = Widget.get_children_by_name(self, "outer-revealer")[0]

        def on_resolved(*_):
            def on_outer_timeout_end():
                self.destroy()
                return GLib.SOURCE_REMOVE

            outer_revealer.set_reveal_child(False)
            GLib.timeout_add(
                priority = GLib.PRIORITY_DEFAULT,
                interval = outer_revealer.get_transition_duration(),
                function = on_outer_timeout_end
            )

        on_resolved_id = n.connect("resolved", on_resolved)

        def on_destroy(*_):
            n.disconnect(on_resolved_id)

        self.connect("destroy", on_destroy)

class NotificationList(Widget.Box):
    def __init__(self):
        super().__init__(
            name = "notification-list-box",
            orientation = Gtk.Orientation.VERTICAL
        )

        notifd = AstalNotifd.get_default()

        def on_notified(x, id, replaced):
            n = notifd.get_notification(id)
            notification = AnimatedNotification(n)
            outer_revealer = Widget.get_children_by_name(notification, "outer-revealer")[0]

            if not self.get_visible():
                self.show()

            self.insert(notification, 0)
            notification.show_all()
            outer_revealer.set_reveal_child(True)

        notifd.connect("notified", on_notified)

        ns = notifd.get_notifications()
        ns.sort(key = lambda x: x.get_id())
        for n in ns:
            notification = AnimatedNotification(n)
            outer_revealer = Widget.get_children_by_name(notification, "outer-revealer")[0]
            self.insert(notification, 0)
            outer_revealer.set_reveal_child(True)
