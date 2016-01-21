import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio


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
        response = dialog.run()

        txt = dialog.uriEntry.get_text()
        print(txt)
        txt = dialog.nameEntry.get_text()
        print(txt)
        txt = dialog.volEntry.get_value()
        print(txt)

        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

        dialog.destroy()


class AddDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Add Sound File", parent, 0,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
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
        self.volEntry = Gtk.HScale().new(Gtk.Adjustment(101, 0, 101, 1, 1, 1))
        self.volEntry.set_digits(0)
        self.volEntry.add_mark(50, Gtk.PositionType.TOP, None)
        self.volEntry.set_hexpand(True)

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

        grid.show_all()

        self.get_content_area().pack_start(grid, True, True, 0)
        self.show_all()

if __name__ == "__main__":
    Interface()
    Gtk.main()
