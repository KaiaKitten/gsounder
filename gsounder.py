import gi
gi.require_version("Gtk", "3.0")
gi.require_version('Gst', '1.0')
gi.require_version('GstAudio', '1.0')
gi.require_version('Json', '1.0')
from gi.repository import Gtk, Gio, Gst, GstAudio, Gio, Json, GLib


class Interface(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="GSounder")
        self.set_border_width(0)
        self.set_default_size(400, 200)
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "GSounder"
        self.set_titlebar(hb)

        hb.pack_end(self.create_icon_button("open-menu"))
        hb.pack_end(self.create_icon_button("edit"))
        hb.pack_end(self.create_icon_button("edit-delete"))
        addbtn = self.create_icon_button("list-add")
        addbtn.connect("clicked", self.on_button_clicked)
        hb.pack_end(addbtn)

        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_vexpand(False)
        self.progressbar.set_hexpand(False)
        self.progressbar.set_margin_bottom(0)
        self.progressbar.set_margin_top(0)

        box = Gtk.VBox.new(False, 0)
        box.pack_start(self.progressbar, False, False, 0)
        box.set_valign(Gtk.Align.BASELINE)
        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_valign(Gtk.Align.BASELINE)
        self.flowbox.set_homogeneous(True)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.flowbox.set_margin_right(5)
        self.flowbox.set_margin_left(5)

        box.pack_start(self.flowbox, True, True, 5)

        self.add(box)

        self.data = Data()
        self.data.read_buttons(self.flowbox)

        self.connect("delete-event", self.quit)
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
                clip = Clip(dialog.nameEntry.get_text(),
                            dialog.uriEntry.get_text(),
                            dialog.volEntry.get_value(),
                            " ", " ",  " ")
                btn = clip.create_button()
                self.flowbox.insert(btn, -1)
                self.show_all()
                clip.button_json()
                dialog.destroy()
                break
            elif response == Gtk.ResponseType.APPLY:
                player.set_uri(dialog.uriEntry.get_text())
                continue
            elif response == Gtk.ResponseType.CANCEL:
                dialog.destroy()
                break

    def quit(self, widget, event):
        self.data.save_buttons()
        Gtk.main_quit()

    def updateProgress(self):
        if player.playing == False:
            return False
            print("stoping")
        duration = player.player.query_duration(Gst.Format.TIME)[1]
        position = player.player.query_position(Gst.Format.TIME)[1]
        fraction = position/duration
        print(fraction)
        self.progressbar.set_fraction(fraction)
        return True


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

        self.fileButton = Gtk.Button("Browse")
        self.fileButton.connect("clicked", self.on_file_clicked)

        self.playButtonImage = Gtk.Image()
        self.playButtonImage.set_from_stock("gtk-media-play",
                                            Gtk.IconSize.BUTTON)
        self.playButton = Gtk.Button.new()
        self.playButton.add(self.playButtonImage)
        self.playButton.connect("clicked", player.playToggled)
        self.playButton.set_valign(Gtk.Align.END)

        grid.attach(namelabel, 0, 0, 1, 1)
        grid.attach_next_to(self.nameEntry, namelabel,
                            Gtk.PositionType.RIGHT, 3, 1)
        grid.attach_next_to(urilabel, namelabel,
                            Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.uriEntry, urilabel,
                            Gtk.PositionType.RIGHT, 2, 1)
        grid.attach_next_to(self.fileButton, self.uriEntry,
                            Gtk.PositionType.RIGHT, 1, 1)
        grid.attach_next_to(vollabel, urilabel,
                            Gtk.PositionType.BOTTOM, 1, 1)
        grid.attach_next_to(self.volEntry, vollabel,
                            Gtk.PositionType.RIGHT, 2, 1)
        grid.attach_next_to(self.playButton, self.volEntry,
                            Gtk.PositionType.RIGHT, 1, 1)
        grid.show_all()

        self.get_content_area().pack_start(grid, True, True, 0)
        self.show_all()

    def format(self, scale, value):
        return str(round(value*100)) + "%"

    def on_file_clicked(self, widget):
        dialog = Gtk.FileChooserDialog("Please choose a file", self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.uriEntry.set_text("file://" + dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            pass
        dialog.show_all()
        dialog.destroy()


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
        GLib.timeout_add(100, interface.updateProgress)

    def stop(self):
        self.player.set_state(Gst.State.NULL)

    def playToggled(self, w):
        if(self.playing is False):
            self.play()
        else:
            self.stop()

        self.playing = not(self.playing)


class Data():

    def __init__(self):
        self.json = Json.Builder.new()
        self.json.begin_array()

    def read_buttons(self, widget):
        self.parser = Json.Parser.new()
        try:
            self.parser.load_from_file("./data.json")
        except:
            return
        reader = Json.Reader.new(self.parser.get_root())
        count = reader.count_elements()
        for i in range(count):
            reader.read_element(i)
            count = reader.count_elements()
            reader.read_element(0)
            name = reader.get_string_value()
            reader.end_element()
            reader.read_element(1)
            uri = reader.get_string_value()
            reader.end_element()
            reader.read_element(2)
            vol = reader.get_int_value()
            reader.end_element()
            reader.read_element(3)
            start = reader.get_string_value()
            reader.end_element()
            reader.read_element(4)
            end = reader.get_string_value()
            reader.end_element()
            reader.read_element(5)
            key = reader.get_string_value()
            reader.end_element()
            reader.end_element()
            reader.end_element()
            self.json.begin_array()
            self.json.add_string_value(name)
            self.json.add_string_value(uri)
            self.json.add_int_value(vol)
            self.json.add_string_value(start)
            self.json.add_string_value(end)
            self.json.add_string_value(key)
            self.json.end_array()
            clip = Clip(name, uri, vol, start, end, key)
            btn = clip.create_button()
            widget.insert(btn, -1)

    def save_buttons(self):
        self.json.end_array()
        gen = Json.Generator.new()
        gen.set_root(self.json.get_root())
        f = Gio.File.new_for_path("./data.json")
        stream = f.replace(None, False, Gio.FileCreateFlags.NONE, None)
        gen.to_stream(stream, None)


class Clip():

    def __init__(self, name, uri, vol, start, end, key):
        self.name = name
        self.uri = uri
        self.start = start
        self.end = end
        self.vol = vol
        self.key = key

    def create_button(self):
        btn = Gtk.Button.new_with_label(self.name)
        btn.connect("clicked", self.on_button_clicked)
        return btn

    def button_json(self):
        # interface.data.json.set_member_name(self.name)
        interface.data.json.begin_array()
        interface.data.json.add_string_value(self.name)
        interface.data.json.add_string_value(self.uri)
        interface.data.json.add_double_value(self.vol)
        interface.data.json.add_string_value(self.start)
        interface.data.json.add_string_value(self.end)
        interface.data.json.add_string_value(self.key)
        interface.data.json.end_array()

    def on_button_clicked(self, widget):
        player.set_uri(self.uri)
        player.set_volume(self.vol)
        player.playToggled(widget)


if __name__ == "__main__":
    interface = Interface()
    player = Player()
    Gtk.main()
