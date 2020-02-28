#
#### Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Feb 17th, 2020
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
# template: is not used plugin, but it is an example or template for you to 
#			start your plugin. It is good starting point to your plugin.
#			Copy this file, rename it, change self.name to your plugin name.
#			If the plugin needs to export its commands to commander, copy
#			commands.py too. If not, delete lines:
#									from . import commands
#									commands.set_commands(self)
# 			
#			Currently, activate and key_bindings methods must be implemented.
#			If no implemention needed for activate and key_bindings then keep
#			the "pass"
#
#			The usual imports are:
#			import gi
#			gi.require_version('Gtk', '3.0')
#			gi.require_version('GtkSource', '4')
#			from gi.repository import GLib, Gio, Gtk, Gdk, GtkSource, GObject
#			
#			But your plugin may not need all of these modules
#
#


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk	

from .files_ui import  FilesUI

# class name must be "Plugin". Do not change the name 
class Plugin(FilesUI):
	
	# the plugins_manager will pass "app" reference 
	# to your plugin. "app" object is defined in gamma.py
	# from "app" reference you can access pretty much 
	# everything related to Gamma (i.e. window, builder, 
	# sourceview, and other plugins)
	def __init__(self, app):
		self.name = "ui_manager"
		self.app = app
		self.builder = app.builder
		self.handlers = app.signal_handler.handlers
		self.plugins = app.plugins_manager.plugins
		self.sourceview_manager = app.sourceview_manager
		self.commands = []
		self.set_handlers()
		
		self.toolbar_files = None
		self.headerbar = None
		self.scrolledwindow = None		
		

	def activate(self):
		# scrolledwindow is object that contains sourceviews
		# basically, a new opened file has its own sourceview 
		# and got added to scrolledwindow
		# previouse sourceview got removed from scrolledwindow
		self.scrolledwindow = self.builder.get_object("source_scrolledwindow")
		
		# get toolbar_files Gtk widget from ui file
		self.toolbar_files = self.builder.get_object("toolbar_files")

		# get headerbar widget reference, to show current filename
		# in headerbar label
		self.headerbar = self.builder.get_object("headerbarMain")
		
		self.scroll_and_source_and_map_box = self.builder.get_object("scroll_and_source_and_map_box") 
	
	
	
	
	def set_handlers(self):
		self.handlers.on_closeBtn_hover_event = self.on_closeBtn_hover_event
		self.handlers.on_menue_enter_notify_event = self.on_menue_enter_notify_event
		self.handlers.on_menue_leave_notify_event = self.on_menue_leave_notify_event
		
		

	def on_closeBtn_hover_event(self, widget, event):
		# print("on_closeBtn_hover_event")
		pass
		
		

	def on_menue_enter_notify_event(self, widget, event):
		lbl = widget.get_child()
		lbl.get_style_context().add_class("menu_hover")
		cursor = Gdk.Cursor(Gdk.CursorType.HAND2)
		self.app.window.get_window().set_cursor(cursor)
		
	
	def on_menue_leave_notify_event(self, widget, event):
		lbl = widget.get_child()
		lbl.get_style_context().remove_class("menu_hover")
		cursor = Gdk.Cursor(Gdk.CursorType.ARROW)
		self.app.window.get_window().set_cursor(cursor)

	
