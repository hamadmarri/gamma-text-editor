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
		self.THE = app.plugins_manager.THE
		self.signal_handler = app.signal_handler
		self.commands = []
		
		# the far left side size where menu is.
		self.min_size = 0
		
		self.signal_handler.key_bindings_to_plugins.append(self)
		commands.set_commands(self)
		
		
		
	def activate(self):
		# the state of current visibility
		self.app.window.toggle_files_removed = False
		
		# previous size of the left side file list size
		self.app.window.toggle_files_old_size = 0
		
		# get widgets references from builder
		toolbar_ctrls = self.app.builder.get_object("toolbar_ctrls")

		# get the menu current size which is default 34px
		self.min_size = toolbar_ctrls.get_allocated_width()

		self.setup_event_boxes()
		
				
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if alt and keyval_name == "f":
			self.toggle_files_list()
		
		
	
	# wrap logo_box and headerbarSide with eventboxs each
	# to get events such as mouse click and hover
	def setup_event_boxes(self):
		header_left_side = self.app.builder.get_object("header_left_side")
		headerbarSide = self.app.builder.get_object("headerbarSide")
		logo_box = self.app.builder.get_object("logo_box")
		
		header_left_side.remove(logo_box)
		header_left_side.remove(headerbarSide)
		
		self.app.window.toggle_files_eventBox = Gtk.EventBox.new()
		self.app.window.toggle_files_eventBox.add(headerbarSide)
		
		self.app.window.toggle_files_eventBox.set_tooltip_text("Hide Files")
		self.app.window.toggle_files_eventBox.connect("button-press-event", self.on_headerbarSide_button_press_event)
		self.app.window.toggle_files_eventBox.connect("enter-notify-event", self.on_headerbarSide_enter_notify_event)
		self.app.window.toggle_files_eventBox.connect("leave-notify-event", self.on_headerbarSide_leave_notify_event)
		
		self.app.window.toggle_files_logoEventBox = Gtk.EventBox.new()
		self.app.window.toggle_files_logoEventBox.add(logo_box)
		self.app.window.toggle_files_logoEventBox.set_tooltip_text("Hide Files")
		self.app.window.toggle_files_logoEventBox.connect("button-press-event", self.on_headerbarSide_button_press_event)
		self.app.window.toggle_files_logoEventBox.connect("enter-notify-event", self.on_headerbarSide_enter_notify_event)
		self.app.window.toggle_files_logoEventBox.connect("leave-notify-event", self.on_headerbarSide_leave_notify_event)
		
		header_left_side.pack_start(self.app.window.toggle_files_logoEventBox, False, True, 0)
		header_left_side.pack_start(self.app.window.toggle_files_eventBox, True, True, 0)
		
		
		
	
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
		if not self.app.window.toggle_files_removed:
			self.hide_files()
		else:
			self.show_files()
	
		
	def hide_files(self):
		bodyPaned = self.app.builder.get_object("bodyPaned")
		toolbar_side = self.app.builder.get_object("toolbar_side")
		headerPaned = self.app.builder.get_object("headerPaned")
		header_left_side = self.app.builder.get_object("header_left_side")
		scrolled_toolbar_files = self.app.builder.get_object("scrolled_toolbar_files")
		
		self.app.window.toggle_files_old_size = bodyPaned.get_position()
		
		# to avoid auto resizing when hiding files list
		self.THE("window_controller", "set_auto_resize", {"auto_resize": False})
		toolbar_side.remove(scrolled_toolbar_files)
		bodyPaned.set_position(0)
		
		header_left_side.remove(self.app.window.toggle_files_eventBox)
		headerPaned.set_position(self.min_size)
		
		self.app.window.toggle_files_logoEventBox.set_tooltip_text("Show Files")
		self.app.window.toggle_files_removed = True
		
		
		
	def show_files(self):
		bodyPaned = self.app.builder.get_object("bodyPaned")
		toolbar_side = self.app.builder.get_object("toolbar_side")
		headerPaned = self.app.builder.get_object("headerPaned")
		header_left_side = self.app.builder.get_object("header_left_side")
		scrolled_toolbar_files = self.app.builder.get_object("scrolled_toolbar_files")
		
		self.THE("window_controller", "set_auto_resize", {"auto_resize": True})
		header_left_side.pack_start(self.app.window.toggle_files_eventBox, True, True, 0)
		toolbar_side.pack_start(scrolled_toolbar_files, True, True, 0)
		
		bodyPaned.set_position(self.app.window.toggle_files_old_size)
		headerPaned.set_position(self.app.window.toggle_files_old_size)

		self.app.window.toggle_files_logoEventBox.set_tooltip_text("Hide Files")
		self.app.window.toggle_files_removed = False
