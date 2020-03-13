#
#### Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Mar 10th, 2020
#
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
#
# 	plugin info: Toggle (hides/shows) the files list to make the text editing area wider
# 
# 
# 

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from . import commands

class Plugin():
	
	def __init__(self, app):
		self.name = "toggle_files_list"
		self.app = app
		self.builder = app.builder
		self.plugins = app.plugins_manager.plugins
		self.signal_handler = app.signal_handler
		self.commands = []
		
		# the state of current visibility
		self.removed = False
		
		# previous size of the left side file list size
		self.old_size = 0
		
		# the far left side size where menu is.
		self.min_size = 0
		
		
		
	def activate(self):
		self.signal_handler.key_bindings_to_plugins.append(self)
		commands.set_commands(self)
		
		# get widgets references from builder
		toolbar_ctrls = self.builder.get_object("toolbar_ctrls")
		self.bodyPaned = self.builder.get_object("bodyPaned")
		self.toolbar_side = self.builder.get_object("toolbar_side")
		self.headerPaned = self.builder.get_object("headerPaned")
		self.header_left_side = self.builder.get_object("header_left_side")
		self.scrolled_toolbar_files = self.builder.get_object("scrolled_toolbar_files")

		# get the menu current size which is default 34px
		self.min_size = toolbar_ctrls.get_allocated_width()

		self.setup_event_boxes()
		
				
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if alt and keyval_name == "f":
			self.toggle_files_list()
		
		
	
	# wrap logo_box and headerbarSide with eventboxs each
	# to get events such as mouse click and hover
	def setup_event_boxes(self):
		self.headerbarSide = self.builder.get_object("headerbarSide")
		self.logo_box = self.builder.get_object("logo_box")

		self.header_left_side.remove(self.logo_box)
		self.header_left_side.remove(self.headerbarSide)
		self.eventBox = Gtk.EventBox.new()
		self.eventBox.add(self.headerbarSide)
		
		self.eventBox.set_tooltip_text("Hide Files")
		self.eventBox.connect("button-press-event", self.on_headerbarSide_button_press_event)
		self.eventBox.connect("enter-notify-event", self.on_headerbarSide_enter_notify_event)
		self.eventBox.connect("leave-notify-event", self.on_headerbarSide_leave_notify_event)
		
		self.logoEventBox = Gtk.EventBox.new()
		self.logoEventBox.add(self.logo_box)
		self.logoEventBox.set_tooltip_text("Hide Files")
		self.logoEventBox.connect("button-press-event", self.on_headerbarSide_button_press_event)
		self.logoEventBox.connect("enter-notify-event", self.on_headerbarSide_enter_notify_event)
		self.logoEventBox.connect("leave-notify-event", self.on_headerbarSide_leave_notify_event)
		
		self.header_left_side.pack_start(self.logoEventBox, False, True, 0)
		self.header_left_side.pack_start(self.eventBox, True, True, 0)
		
		
		
	
	# on hover, show hand cursor
	def on_headerbarSide_enter_notify_event(self, widget, event):
		cursor = Gdk.Cursor(Gdk.CursorType.HAND2)
		self.app.window.get_window().set_cursor(cursor)
		
	# on leave hover, show back the default cursor
	def on_headerbarSide_leave_notify_event(self, widget, event):
		cursor = Gdk.Cursor(Gdk.CursorType.ARROW)
		self.app.window.get_window().set_cursor(cursor)
		
	
	# when click on "Files" or "Γ" logo, toggle files visibility
	def on_headerbarSide_button_press_event(self, widget, event):
		self.toggle_files_list()
	
	
	
	
	def toggle_files_list(self):
		if not self.removed:
			self.hide_files()
		else:
			self.show_files()
	
		
	def hide_files(self):
		self.old_size = self.bodyPaned.get_position()
		
		# to avoid auto resizing when hiding files list
		self.plugins["window_ctrl.window_ctrl"].auto_resize = False
		self.toolbar_side.remove(self.scrolled_toolbar_files)
		self.bodyPaned.set_position(0)
		
		self.header_left_side.remove(self.eventBox)
		self.headerPaned.set_position(self.min_size)
		
		self.logoEventBox.set_tooltip_text("Show Files")
		self.removed = True
		
		
		
	def show_files(self):
		self.plugins["window_ctrl.window_ctrl"].auto_resize = True
		self.header_left_side.pack_start(self.eventBox, True, True, 0)
		self.toolbar_side.pack_start(self.scrolled_toolbar_files, True, True, 0)
		
		self.bodyPaned.set_position(self.old_size)
		self.headerPaned.set_position(self.old_size)

		self.logoEventBox.set_tooltip_text("Hide Files")
		self.removed = False