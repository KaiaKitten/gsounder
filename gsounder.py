import gi
gi.require_version("Gtk", "3.0")
gi.require_version('Gst', '1.0')
gi.require_version('GstAudio', '1.0')
from gi.repository import Gtk, Gio, Gst, GstAudio


class Interface(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="gsounder")
        self.set_border_width(10)
        self.set_default_size(400, 200)
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "gsounder"
        self.set_titlebar(hb)

        hb.pack_end(self.create_icon_button("open-menu-symbolic"))
        hb.pack_end(self.create_icon_button("edit-symbolic"))
        addbtn = self.create_icon_button("list-add-symbolic")
        addbtn.connect("clicked", self.on_button_clicked)
        hb.pack_end(addbtn)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")
        self.add(box)

        clip = Clip("jepordy", "file:///home/kyahco/Music/Random/Jeopardy.wav", None, None, 0.4)
        btn = clip.create_button()
        box.add(btn)

        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def create_icon_button(self, icon_name):
        btn = Gtk.Button()
        icon = Gio.ThemedIcon(name=icon_name)
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        btn.add(image)
        return btn

    def on_button_clicked(self, widget):
        dialog = AddDialog(self)
        respone = None
        while(respone is None):
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                print("The OK button was clicked")
                txt = dialog.uriEntry.get_text()
                print(txt)
                player.set_uri(txt)
                txt = dialog.nameEntry.get_text()
                print(txt)
                dialog.destroy()
                break
            elif response == Gtk.ResponseType.APPLY:
                print("The APPLY button was clicked")
                txt = dialog.uriEntry.get_text()
                print(txt)
                player.set_uri(txt)
                txt = dialog.nameEntry.get_text()
                print(txt)
                continue
            elif response == Gtk.ResponseType.CANCEL:
                print("The Cancel button was clicked")
                dialog.destroy()
                break


class AddDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Add Sound File", parent, 0,
                            ("_Cancel", Gtk.ResponseType.CANCEL,
                             "_Apply", Gtk.ResponseType.APPLY,
                             "_Ok", Gtk.ResponseType.OK))
        self.set_default_size(150, 100)
        self.set_border_width(10)

        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(5)
        # self.add(grid)

        namelabel = Gtk.Label("Name:")
        self.nameEntry = Gtk.Entry()
        self.nameEntry.set_activates_default(True)
        self.nameEntry.set_hexpand(True)
        urilabel = Gtk.Label("URI:")
        self.uriEntry = Gtk.Entry()
        self.uriEntry.set_activates_default(True)
        self.uriEntry.set_hexpand(True)
        vollabel = Gtk.Label("Volume:")
        vollabel.set_yalign(0.9)

        self.volEntry = Gtk.HScale().new_with_range(0, 1, 0.02)
        self.volEntry.set_value(0.5)
        self.volEntry.set_digits(2)
        self.volEntry.add_mark(0.5, Gtk.PositionType.TOP, None)
        self.volEntry.set_hexpand(True)
        self.volEntry.connect("change-value", player.set_volume_slider)
        self.volEntry.connect("format-value", self.format)

        self.playButtonImage = Gtk.Image()
        self.playButtonImage.set_from_stock("gtk-media-play", Gtk.IconSize.BUTTON)
        self.playButton = Gtk.Button.new()
        self.playButton.add(self.playButtonImage)
        self.playButton.connect("clicked", player.playToggled)

        grid.attach(namelabel, 0, 0, 1, 1)
        grid.attach_next_to(self.nameEntry, namelabel,
                            Gtk.PositionType.RIGHT, 2, 1)
        grid.attach_next_to(urilabel, namelabel,
                            Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.uriEntry, urilabel,
                            Gtk.PositionType.RIGHT, 2, 1)
        grid.attach_next_to(vollabel, urilabel,
                            Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.volEntry, vollabel,
                            Gtk.PositionType.RIGHT, 2, 1)
        grid.attach_next_to(self.playButton, vollabel,
                            Gtk.PositionType.BOTTOM, 1, 1)
        grid.show_all()

        self.get_content_area().pack_start(grid, True, True, 0)
        self.show_all()

    def format(self, scale, value):
        return str(round(value*100)) + "%"


class Player():

    def __init__(self):

        self.uri = "file:///home/kyahco/Music/Random/Under-Pressure.wav"
        self.playing = False

        # GStreamer Setup
        Gst.init_check(None)
        self.player = Gst.ElementFactory.make("playbin", "audio-player")
        self.IS_GST010 = Gst.version()[0] == 0
        fakesink = Gst.ElementFactory.make("fakesink", "fakesink")
        self.player.set_property("video-sink", fakesink)
        bus = self.player.get_bus()
        # bus.add_signal_watch_full()
        # bus.connect("message", self.on_message)
        # self.player.connect("about-to-finish",  self.on_finished)

    def get_volume(self):
        return self.player.get_property("volume")

    def set_volume(self, value):
        self.player.set_property("volume", value)

    def set_volume_slider(self, scale, scroll_type, value):
        self.player.set_property("volume", value)

    def set_uri(self, uri):
        self.uri = uri

    def play(self):
        self.player.set_property("uri", self.uri)
        self.player.set_state(Gst.State.PLAYING)

    def stop(self):
        self.player.set_state(Gst.State.NULL)

    def playToggled(self, w):
        if(self.playing is False):
            self.play()
        else:
            self.stop()

        self.playing = not(self.playing)


class Clip():

    def __init__(self, name, uri, start, end, vol):
        self.name = name
        self.uri = uri
        self.start = start
        self.end = end
        self.vol = vol

    def create_button(self):
        btn = Gtk.Button.new_with_label(self.name)
        btn.connect("clicked", self.on_button_clicked)
        return btn

    def on_button_clicked(self, widget):
        player.set_uri(self.uri)
        player.set_volume(self.vol)
        player.playToggled(widget)



if __name__ == "__main__":
    Interface()
    player = Player()
    Gtk.main()
