from gi.repository import Gtk, AstalWp
import widget as Widget

wp = AstalWp.get_default()
audio = wp.get_audio()

def AudioSliders():
    ret = Widget.Box(
        name = "audio-sliders",
        orientation = Gtk.Orientation.VERTICAL,
        children = [
            Widget.Box(
                name = "speaker",
                css_classes = ["slider-container"],
                children = [
                    Widget.Button(
                        name = "speaker-mute-button",
                        css_classes = ["mute-button"],
                        child = Widget.Image(
                            name = "speaker-mute-icon",
                            icon_name = "audio-volume-muted-symbolic"
                        )
                    ),
                    Widget.Scale(
                        name = "speaker-volume-slider",
                        css_classes = ["volume-slider"],
                        hexpand = True
                    ),
                    Widget.Label(
                        name = "speaker-volume-label",
                        css_classes = ["volume-label"],
                        width_chars = 5,
                        label = "0%"
                    )
                ]
            ),
            Widget.Box(
                name = "microphone",
                css_classes = ["slider-container"],
                children = [
                    Widget.Button(
                        name = "microphone-mute-button",
                        css_classes = ["mute-button"],
                        child = Widget.Image(
                            name = "microphone-mute-icon",
                            icon_name = "microphone-disabled-symbolic"
                        )
                    ),
                    Widget.Scale(
                        name = "microphone-volume-slider",
                        css_classes = ["volume-slider"],
                        hexpand = True
                    ),
                    Widget.Label(
                        name = "microphone-volume-label",
                        css_classes = ["volume-label"],
                        width_chars = 5,
                        label = "0%"
                    )
                ]
            )
        ]
    )

    speaker = audio.get_default_speaker()
    microphone = audio.get_default_microphone()
    speaker_mute_button = Widget.get_child_by_name(ret, "speaker-mute-button")
    speaker_mute_icon = Widget.get_child_by_name(ret, "speaker-mute-icon")
    speaker_volume_slider = Widget.get_child_by_name(ret, "speaker-volume-slider")
    speaker_volume_label = Widget.get_child_by_name(ret, "speaker-volume-label")
    microphone_mute_button = Widget.get_child_by_name(ret, "microphone-mute-button")
    microphone_mute_icon = Widget.get_child_by_name(ret, "microphone-mute-icon")
    microphone_volume_slider = Widget.get_child_by_name(ret, "microphone-volume-slider")
    microphone_volume_label = Widget.get_child_by_name(ret, "microphone-volume-label")

    def on_speaker_mute(*_):
        if speaker and speaker.get_mute():
            speaker_volume_slider.add_css_class("mute")
            speaker_mute_button.add_css_class("mute")
            speaker_mute_icon.set_from_icon_name(
                "audio-volume-muted-symbolic",
                Gtk.IconSize.BUTTON
            )
        else:
            speaker_volume_slider.remove_css_class("mute")
            speaker_mute_button.remove_css_class("mute")
            speaker_mute_icon.set_from_icon_name(
                "audio-volume-high-symbolic",
                Gtk.IconSize.BUTTON
            )

    def on_speaker_volume(*_):
        if speaker: speaker_volume_slider.set_value(speaker.get_volume())

    def on_speaker_volume_slider_value(*_):
        speaker_volume_label.set_label(f"{speaker_volume_slider.get_value():.0%}")
        if speaker: speaker.set_volume(speaker_volume_slider.get_value())

    def on_speaker_mute_button_clicked(*_):
        if speaker: speaker.set_mute(not speaker.get_mute())

    def on_microphone_mute(*_):
        if microphone and microphone.get_mute():
            microphone_volume_slider.add_css_class("mute")
            microphone_mute_button.add_css_class("mute")
            microphone_mute_icon.set_from_icon_name(
                "microphone-disabled-symbolic",
                Gtk.IconSize.BUTTON
            )
        else:
            microphone_volume_slider.remove_css_class("mute")
            microphone_mute_button.remove_css_class("mute")
            microphone_mute_icon.set_from_icon_name(
                "microphone-sensitivity-high-symbolic",
                Gtk.IconSize.BUTTON
            )

    def on_microphone_volume(*_):
        if microphone: microphone_volume_slider.set_value(microphone.get_volume())

    def on_microphone_volume_slider_value(*_):
        microphone_volume_label.set_label(f"{microphone_volume_slider.get_value():.0%}")
        if microphone: microphone.set_volume(microphone_volume_slider.get_value())

    def on_microphone_mute_button_clicked(*_):
        if microphone: microphone.set_mute(not microphone.get_mute())

    speaker_volume_slider.connect("value-changed", on_speaker_volume_slider_value)
    speaker_mute_button.connect("clicked", on_speaker_mute_button_clicked)
    microphone_volume_slider.connect("value-changed", on_microphone_volume_slider_value)
    microphone_mute_button.connect("clicked", on_microphone_mute_button_clicked)

    if speaker:
        speaker.connect("notify::mute", on_speaker_mute)
        speaker.connect("notify::volume", on_speaker_volume)

    if microphone:
        microphone.connect("notify::mute", on_microphone_mute)
        microphone.connect("notify::volume", on_microphone_volume)

    return ret
