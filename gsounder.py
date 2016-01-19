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
        hb.pack_end(self.create_icon_button("list-add-symbolic"))

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

if __name__ == "__main__":
    Interface()
    Gtk.main()
