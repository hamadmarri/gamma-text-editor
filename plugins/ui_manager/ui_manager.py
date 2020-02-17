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

import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk	


# class name must be "Plugin". Do not change the name 
class Plugin():
	
	# the plugins_manager will pass "app" reference 
	# to your plugin. "app" object is defined in gamma.py
	# from "app" reference you can access pretty much 
	# everything related to Gamma (i.e. window, builder, 
	# sourceview, and other plugins)
	def __init__(self, app):
		self.name = "ui_manager"
		self.app = app
		self.builder = app.builder
		self.handlers = app.handler.handlers
		self.sourceview_manager = app.sourceview_manager
		self.commands = []
		self.set_handlers()
		self.files_manager = None
		self.message_notify = None
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
	
	
	
	def get_plugins_refs(self):
		# get files_manager
		if not self.files_manager:
			self.files_manager = self.app.plugins_manager.get_plugin("files_manager")
		
		# get message_notify
		if not self.message_notify:
			self.message_notify = self.app.plugins_manager.get_plugin("message_notify")
				
	
	
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		pass
	
	
	
	def set_handlers(self):
		self.handlers.on_closeBtn_hover_event = self.on_closeBtn_hover_event
		self.handlers.on_menue_enter_notify_event = self.on_menue_enter_notify_event
		self.handlers.on_menue_leave_notify_event = self.on_menue_leave_notify_event
		
		

	def on_closeBtn_hover_event(self, widget, event):
		print("on_closeBtn_hover_event")
		
		

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



	# adds ui button with filename label in toolbar_file
	# (the left side panel)
	def add_filename_to_ui(self, newfile):		
		
		# create new button
		btn = Gtk.Button()
		
		# associate btn widget to File object
		newfile.ui_ref = btn
		
		# set the text of button to filename
		basename = os.path.basename(newfile.filename)
		btn.set_label(basename)

		# connect clicked signal to side_file_clicked method		
		btn.connect("clicked", self.side_file_clicked, newfile.filename)
		
		# set the ui/css class to the button (.openned_file)
		btn.get_style_context().add_class("openned_file")
		
		# get the label of the button, and set left padding to 0
		lbl = btn.get_children()[0]
		lbl.set_xalign(0)
		
		# add button to toolbar_files
		# (read: https://developer.gnome.org/gtk3/stable/GtkBox.html#gtk-box-pack-start)
		self.toolbar_files.pack_start(btn, False, False, 0)
		
		# position new opened file's button to top of toolbar_files
		# (read: https://developer.gnome.org/gtk3/unstable/GtkBox.html#gtk-box-reorder-child)
		self.toolbar_files.reorder_child(btn, 0)
		
		# show the widget
		btn.show()
		
		
		
	# handler of "clicked" event
	# it switch the view to the filename in clicked button
	def side_file_clicked(self, btn, filename):
		self.get_plugins_refs()
		self.set_currently_displayed(btn)	
		self.files_manager.side_file_clicked(filename)
		
		
		
	def set_currently_displayed(self, file_ui_ref):
		# remove current displayed class
		btns = self.toolbar_files.get_children()
		for b in btns:
			b.get_style_context().remove_class("openned_file_current_displayed")
		
		file_ui_ref.get_style_context().add_class("openned_file_current_displayed")
	
	
	# updates the headerbar by filename
	def update_header(self, filename):
		self.get_plugins_refs()
		
		# gets basename of the file, not the full path
		basename = os.path.basename(filename)
		
		# set the title of headerbar
		self.headerbar.set_title(basename)
		
		# show message of the full path of the file 
		# it is useful to avoid confusion when having 
		# different files with similar names in different paths
		self.message_notify.show_message(filename)
		
	
	
	# updates the headerbar by filename
	def set_header(self, text):
		# set the title of headerbar
		self.headerbar.set_title(text)





	def replace_sourceview_widget(self, newsource):
		# remove previously displayed sourceview
		# DEBUG: print("scrolledwindow.remove before")
		prev_child = self.scrolledwindow.get_child()
		# DEBUG: print(prev_child)
		if prev_child:
			self.scrolledwindow.remove(prev_child)
		# DEBUG: print("scrolledwindow.remove")
		
		# add the newsource view
		self.scrolledwindow.add(newsource)
		# DEBUG: print("scrolledwindow.add")
		
		# place the cursor in it
		newsource.grab_focus()
		
		# need to update the mini map too
		self.sourceview_manager.update_sourcemap(newsource)
		# DEBUG: print("sourceview_manager.update_sourcemap")
