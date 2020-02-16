#
#### Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Feb 16th, 2020
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


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from . import commands


class Plugin():

	def __init__(self, app):
		self.name = "search_in_file"
		self.app = app
		self.handlers = app.handler.handlers
		self.commands = []
		self.highlight = None
		
		# commands.set_commands(self)
		self.set_handlers()
	

	def activate(self):
		pass
	

	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		pass
	
	
	# setting handlers, see SignalHandler
	def set_handlers(self):
		self.handlers.on_search_field_changed = self.on_search_field_changed
		self.handlers.on_search_key_press_event = self.on_search_key_press_event
	
	
	
	def get_plugins_refs(self):
		# get highlight
		if not self.highlight:
			self.highlight = self.app.plugins_manager.get_plugin("highlight")
			
		
	
	# (see https://developer.gnome.org/gtk3/stable/GtkSearchEntry.html)
	# (https://developer.gnome.org/gtk3/stable/GtkEntry.html)
	def on_search_field_changed(self, widget):
		self.get_plugins_refs()
		search = widget.get_text()
		self.highlight.highlight(search)
		
		
	def on_search_key_press_event(self, widget, event):
		keyval_name = Gdk.keyval_name(event.keyval)
		if keyval_name == "Escape":
			self.clear_search(widget)
		
	
	
	def clear_search(self, widget):
		self.get_plugins_refs()
		widget.set_text("")
		# self.highlight.highlight("")
