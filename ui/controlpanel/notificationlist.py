from gi.repository import GLib, Gtk, AstalNotifd
import widget as Widget
from ui.notifications.notification import Notification

notifd = AstalNotifd.get_default()

def AnimatedNotification(n):
    return Widget.Box(
        css_classes = ["animated-notification-box"],
        children = [
            Widget.Revealer(
                name = "outer-revealer",
                transition_type = Gtk.RevealerTransitionType.SLIDE_DOWN,
                child = Notification(n)
            )
        ]
    )

def NotificationList():
    ret = Widget.Box(
        name = "notification-list",
        orientation = Gtk.Orientation.VERTICAL,
        children = [
            Widget.Box(
                css_classes = ["header-box"],
                children = [
                    Widget.Label(
                        css_classes = ["title-label"],
                        label = "Notifications"
                    ),
                    Widget.Box(
                        halign = Gtk.Align.END,
                        hexpand = True,
                        children = [
                            Widget.Button(
                                name = "clear-button",
                                css_classes = ["clear-button"],
                                child = Widget.Image(
                                    icon_name = "user-trash-symbolic"
                                )
                            )
                        ]
                    )
                ]
            ),
            Widget.ScrolledWindow(
                name = "notifications-scrolled-window",
                vexpand = True,
                child = Widget.Box(
                    name = "notifications-box",
                    orientation = Gtk.Orientation.VERTICAL
                )
            )
        ]
    )

    notifications = {}
    notifications_box = Widget.get_child_by_name(ret, "notifications-box")
    clear_button = Widget.get_child_by_name(ret, "clear-button")

    def on_resolved(x, id, reason):
        notification = notifications[id]
        outer_revealer = Widget.get_child_by_name(notification, "outer-revealer")

        def on_outer_timeout_end():
            notification.destroy()
            del notifications[id]

            if len(notifications_box.get_children()) == 0:
                notifications_box.set_children([
                    Widget.Label(
                        css_classes = ["empty-label"],
                        halign = Gtk.Align.CENTER,
                        valign = Gtk.Align.CENTER,
                        hexpand = True,
                        vexpand = True,
                        label = "No notifications"
                    )
                ])

            return GLib.SOURCE_REMOVE

        outer_revealer.set_reveal_child(False)
        GLib.timeout_add(
            outer_revealer.get_transition_duration(),
            on_outer_timeout_end
        )

    def on_notified(x, id, replaced):
        n = notifd.get_notification(id)
        notification = AnimatedNotification(n)
        notifications[id] = notification
        outer_revealer = Widget.get_child_by_name(notification, "outer-revealer")

        if notifications_box.get_children() and isinstance(notifications_box.get_children()[0], Widget.Label):
            notifications_box.get_children()[0].destroy()

        notifications_box.add_at_index(notification, 0)
        outer_revealer.set_reveal_child(True)

    def on_clear_button_clicked(*_):
        for n in notifd.get_notifications():
            n.dismiss()

    notifd.connect("resolved", on_resolved)
    notifd.connect("notified", on_notified)
    clear_button.connect("clicked", on_clear_button_clicked)

    ns = notifd.get_notifications()
    ns.sort(key = lambda x: x.get_id())
    if len(ns) > 0:
        for n in ns:
            on_notified(None, n.get_id(), False)
    else:
        notifications_box.set_children([
            Widget.Label(
                css_classes = ["empty-label"],
                halign = Gtk.Align.CENTER,
                valign = Gtk.Align.CENTER,
                hexpand = True,
                vexpand = True,
                label = "No notifications"
            )
        ])

    return ret
