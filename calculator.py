import gi.repository
gi.require_version('Budgie', '1.0')
from gi.repository import Budgie, GObject, Gtk, Gio
import os


"""
Budgie EmptyPopover

Author: Heavily Modified from CountDown applet by Jacob Vlijm
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

class Calculator(GObject.GObject, Budgie.Plugin):
    """ This is simply an entry point into your Budgie Applet implementation.
        Note you must always override Object, and implement Plugin.
    """

    # Good manners, make sure we have unique name in GObject type system
    __gtype_name__ = "Calculator"

    def __init__(self):
        """ Initialisation is important.
        """
        GObject.Object.__init__(self)

    def do_get_panel_widget(self, uuid):
        """ This is where the real fun happens. Return a new Budgie.Applet
            instance with the given UUID. The UUID is determined by the
            BudgiePanelManager, and is used for lifetime tracking.
        """
        return CalculatorApplet(uuid)


class CalculatorApplet(Budgie.Applet):
    """ Budgie.Applet is in fact a Gtk.Bin """

    def __init__(self, uuid):
    
        box_padding = 3
        grid_padding = 3

        self.tab_message = ""
        Budgie.Applet.__init__(self)
        self.uuid = uuid

        # applet appearance
        self.icon = Gtk.Image()
        self.icon.set_from_icon_name(
            "gnome-calculator", Gtk.IconSize.MENU
        )
        self.panel_box = Gtk.EventBox()
        self.panel_box.add(self.icon)
        self.add(self.panel_box)
        self.popover = Budgie.Popover.new(self.panel_box)
        
        self.grid      = Gtk.Grid     ()
        self.sep       = Gtk.Separator()
        self.entry     = Gtk.Entry    ()
        self.entry_box = Gtk.Box      ()
        self.box       = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.box.pack_start(self.entry_box, True , True , box_padding)
        self.box.pack_start(self.sep      , True , True , 0        )
        self.box.pack_end  (self.grid     , True, True, box_padding)
        
        self.entry_box.pack_start(self.entry, True, True, box_padding)

        self.grid.set_row_spacing(grid_padding)
        self.grid.set_column_spacing(grid_padding)

        # This is where all the buttons are defined.
        self.buttonC      = Gtk.Button.new_with_label('C')
        self.button1      = Gtk.Button.new_with_label('1')
        self.button2      = Gtk.Button.new_with_label('2')
        self.button3      = Gtk.Button.new_with_label('3')
        self.button4      = Gtk.Button.new_with_label('4')
        self.button5      = Gtk.Button.new_with_label('5')
        self.button6      = Gtk.Button.new_with_label('6')
        self.button7      = Gtk.Button.new_with_label('7')
        self.button8      = Gtk.Button.new_with_label('8')
        self.button9      = Gtk.Button.new_with_label('9')
        self.button0      = Gtk.Button.new_with_label('0')
        self.buttonbpar   = Gtk.Button.new_with_label('(')
        self.buttonfpar   = Gtk.Button.new_with_label(')')
        self.buttonplus   = Gtk.Button.new_with_label('+')
        self.buttonequal  = Gtk.Button.new_with_label('=')
        self.buttonminus  = Gtk.Button.new_with_label('-')
        self.buttondivide = Gtk.Button.new_with_label('÷')
        self.buttonmulti  = Gtk.Button.new_with_label('×')
        self.buttondot    = Gtk.Button.new_with_label('.')
        self.buttonback   = Gtk.Button.new_with_label('🠄')
        self.buttonroot   = Gtk.Button.new_with_label('')
        self.buttonpower  = Gtk.Button.new_with_label('^')

        self.button1.connect("clicked",self.fnc_button1)
        self.button2.connect("clicked",self.fnc_button2)
        self.button3.connect("clicked",self.fnc_button3)
        self.button4.connect("clicked",self.fnc_button4)
        self.button5.connect("clicked",self.fnc_button5)
        self.button6.connect("clicked",self.fnc_button6)
        self.button7.connect("clicked",self.fnc_button7)
        self.button8.connect("clicked",self.fnc_button8)
        self.button9.connect("clicked",self.fnc_button9)
        self.button0.connect("clicked",self.fnc_button0)
        self.buttonplus.connect("clicked",self.fnc_buttonplus)
        self.buttonfpar.connect("clicked",self.fnc_buttonfpar)
        self.buttonbpar.connect("clicked",self.fnc_buttonbpar)
        self.buttonminus.connect("clicked",self.fnc_buttonminus)
        self.buttondivide.connect("clicked",self.fnc_buttondivide)
        self.buttonmulti.connect("clicked",self.fnc_buttonmulti)
        self.buttondot.connect("clicked",self.fnc_buttondot)
        self.buttonpower.connect('clicked',self.fnc_buttonpower)
        

        self.buttonequal.connect('clicked', self.go            )
        self.buttonback.connect ('clicked', self.backspace_func)
        self.buttonC.connect    ('clicked', self.clear         )

        self.grid.set_border_width(3)
        
        
        # Here all the buttons are positioned.
        self.grid.attach(self.buttonC     , 1, 1, 1, 1)
        self.grid.attach(self.buttonbpar  , 2, 1, 1, 1)
        self.grid.attach(self.buttonfpar  , 3, 1, 1, 1)
        self.grid.attach(self.buttonback  , 4, 1, 1, 1)
        self.grid.attach(self.button1     , 1, 2, 1, 1)
        self.grid.attach(self.button2     , 2, 2, 1, 1)
        self.grid.attach(self.button3     , 3, 2, 1, 1)
        self.grid.attach(self.buttonplus  , 4, 2, 1, 1)
        self.grid.attach(self.button4     , 1, 3, 1, 1)
        self.grid.attach(self.button5     , 2, 3, 1, 1)
        self.grid.attach(self.button6     , 3, 3, 1, 1)
        self.grid.attach(self.buttonmulti , 4, 3, 1, 1)
        self.grid.attach(self.buttonback  , 5, 3, 1, 1)
        self.grid.attach(self.button7     , 1, 4, 1, 1)
        self.grid.attach(self.button8     , 2, 4, 1, 1)
        self.grid.attach(self.button9     , 3, 4, 1, 1)
        self.grid.attach(self.buttonminus , 4, 4, 1, 1)
        self.grid.attach(self.buttondot   , 1, 5, 1, 1)
        self.grid.attach(self.button0     , 2, 5, 1, 1)
        self.grid.attach(self.buttonpower , 3, 5, 1, 1)
        self.grid.attach(self.buttondivide, 4, 5, 1, 1)
        
        self.entry_box.pack_end(self.buttonequal, False, False, box_padding)
        self.popover.add(self.box)
        self.box.show_all()
        self.grid.show_all()
        self.panel_box.show_all()
        self.show_all()
        self.panel_box.connect("button-press-event", self.on_press)
        

    def go(self, widget):
        _ = self.formatted_text()
        exec(f'self.entry.set_text(str({_}))')
    
    def backspace_func(self, widget):
        self.entry.set_text(self.entry.get_text()[:-1])
        
    def clear(self, button):
        self.entry.set_text('')
        
    def formatted_text(self):
        return self.entry.get_text().replace(' ','').replace('[','(').replace(']',')')\
            .replace('×','*').replace('^','**').replace('÷','/')
                   
   # Now here are the functions for normal buttons
   
    def fnc_button1(self, button): self.entry.set_text(self.entry.get_text() + '1') 

    def fnc_button2(self, button): self.entry.set_text(self.entry.get_text() + '2') 
       
    def fnc_button3(self, button): self.entry.set_text(self.entry.get_text() + '3') 
     
    def fnc_button4(self, button): self.entry.set_text(self.entry.get_text() + '4') 
        
    def fnc_button5(self, button): self.entry.set_text(self.entry.get_text() + '5') 
         
    def fnc_button6(self, button): self.entry.set_text(self.entry.get_text() + '6') 
         
    def fnc_button7(self, button): self.entry.set_text(self.entry.get_text() + '7')      
    
    def fnc_button8(self, button): self.entry.set_text(self.entry.get_text() + '8') 
     
    def fnc_button9(self, button): self.entry.set_text(self.entry.get_text() + '9') 
     
    def fnc_button0(self, button): self.entry.set_text(self.entry.get_text() + '0') 
         
    def fnc_buttonplus(self, button): self.entry.set_text(self.entry.get_text() + '+') 
    
    def fnc_buttonfpar(self, button): self.entry.set_text(self.entry.get_text() + ')') 
         
    def fnc_buttonbpar(self, button): self.entry.set_text(self.entry.get_text() + '(')      
    
    def fnc_buttonminus(self, button): self.entry.set_text(self.entry.get_text() + '-')      
    
    def fnc_buttondivide(self, button): self.entry.set_text(self.entry.get_text() + '÷')      
    
    def fnc_buttonmulti(self, button): self.entry.set_text(self.entry.get_text() + '×')      
    
    def fnc_buttondot(self, button): self.entry.set_text(self.entry.get_text() + '.')      
    
    def fnc_buttonrem(self, button): self.entry.set_text(self.entry.get_text() + '%')
    
    def fnc_buttonpower(self, button): self.entry.set_text(self.entry.get_text() + '^') 


    def on_press(self, panel_box, arg):
        self.manager.show_popover(self.panel_box)

    def do_update_popovers(self, manager):
        self.manager = manager
        self.manager.register_popover(self.panel_box, self.popover)

    def do_supports_settings(self):
        """Return True if support setting through Budgie Setting,
        False otherwise.
        """
        return False
