import gi.repository
gi.require_version('Budgie', '1.0')
from gi.repository import Budgie, GObject, Gtk, Gio
import os


"""
Budgie EmptyPopover

Author: Heavily Modified fro CountDown applet by Jacob Vlijm
Copyright © 2017-2020 Ubuntu Budgie Developers
Website=https://ubuntubudgie.org
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or any later version. This
program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE. See the GNU General Public License for more details. You
should have received a copy of the GNU General Public License along with this
program.  If not, see <http://www.gnu.org/licenses/>.
"""

class EmptyPopover(GObject.GObject, Budgie.Plugin):
    """ This is simply an entry point into your Budgie Applet implementation.
        Note you must always override Object, and implement Plugin.
    """

    # Good manners, make sure we have unique name in GObject type system
    __gtype_name__ = "EmptyPopover"

    def __init__(self):
        """ Initialisation is important.
        """
        GObject.Object.__init__(self)

    def do_get_panel_widget(self, uuid):
        """ This is where the real fun happens. Return a new Budgie.Applet
            instance with the given UUID. The UUID is determined by the
            BudgiePanelManager, and is used for lifetime tracking.
        """
        return EmptyPopoverApplet(uuid)


class EmptyPopoverSettings(Gtk.Grid):
    def __init__(self, setting):

        super().__init__()
        self.setting = setting
        # maingrid
        self.show_all()


class EmptyPopoverApplet(Budgie.Applet):
    """ Budgie.Applet is in fact a Gtk.Bin """

    def __init__(self, uuid):

        self.tab_message = ""
        Budgie.Applet.__init__(self)
        self.uuid = uuid

        # applet appearance
        self.icon = Gtk.Image()
        self.icon.set_from_icon_name(
            "mail-unread-symbolic", Gtk.IconSize.MENU
        )
        self.box = Gtk.EventBox()
        self.box.add(self.icon)
        self.add(self.box)
        self.popover = Budgie.Popover.new(self.box)
        
        self.maingrid = Gtk.Grid()
        self.popover.add(self.maingrid)

        """ maingrid is where to attach all the functions for the budgie popup
        """

        self.maingrid.attach(Gtk.Label("Label 1   "), 0, 0, 1, 1)
        self.maingrid.attach(Gtk.Label("Label 1   "), 0, 1, 1, 1)
        self.maingrid.attach(Gtk.Label("Label 3   "), 0, 2, 1, 1)
        self.maingrid.attach(Gtk.Label("Label 4   "), 0, 3, 1, 1)
        self.maingrid.attach(Gtk.Label("Label 5   "), 1, 0, 1, 1)
        self.maingrid.attach(Gtk.Label("Label 6   "), 1, 1, 1, 1)
        self.maingrid.attach(Gtk.Label("Label 7   "), 1, 2, 1, 1)
        self.maingrid.attach(Gtk.Label("Label 8   "), 1, 3, 1, 1)


        self.maingrid.show_all()
        self.box.show_all()
        self.show_all()
        self.box.connect("button-press-event", self.on_press)


    def on_press(self, box, arg):
        self.manager.show_popover(self.box)

    def do_update_popovers(self, manager):
        self.manager = manager
        self.manager.register_popover(self.box, self.popover)

    def do_get_settings_ui(self):
        """Return the applet settings with given uuid"""
        return EmptyPopoverSettings(self.get_applet_settings(self.uuid))

    def do_supports_settings(self):
        """Return True if support setting through Budgie Setting,
        False otherwise.
        """
        return True
