#
#### Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Feb 11th, 2020
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
from . import commander_window as cw

class Plugin():
	
	def __init__(self, app):
		self.name = "commander"
		self.app = app
		self.builder = app.builder
		self.plugins_manager = app.plugins_manager
		self.signal_handler = app.signal_handler
		self.handlers = app.signal_handler.handlers
		self.commands = None
		self.only_alt = False
		self.commander_window = cw.CommanderWindow(app, self)
		
		
	def activate(self):
		self.signal_handler.key_bindings_to_plugins.append(self)
		self.signal_handler.any_key_press_to_plugins.append(self)
		self.set_handlers()
	
		
	def set_handlers(self):
		self.handlers.on_window_key_release_event = self.on_window_key_release_event
		self.handlers.on_commanderWindow_key_press_event = self.commander_window.on_commanderWindow_key_press_event
		self.handlers.on_commanderWindow_key_release_event = self.commander_window.on_commanderWindow_key_release_event
		self.handlers.on_commanderWindow_focus_out_event = self.commander_window.on_commanderWindow_focus_out_event
		self.handlers.on_commanderSearchEntry_changed = self.commander_window.on_commanderSearchEntry_changed
		self.handlers.on_commanderList_row_activated = self.commander_window.on_commanderList_row_activated
		self.handlers.on_commanderSearchEntry_key_press_event = self.commander_window.on_commanderSearchEntry_key_press_event
		self.handlers.on_commanderList_key_press_event = self.commander_window.on_commanderList_key_press_event

				
	
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if not alt:
			self.only_alt = True
		else:
			self.only_alt = False
			

	def on_window_key_release_event(self, window, event):
		keyval_name = Gdk.keyval_name(event.keyval)
		ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
		alt = (event.state & Gdk.ModifierType.MOD1_MASK)
		shift = (event.state & Gdk.ModifierType.SHIFT_MASK)
		
		if alt and self.only_alt and keyval_name == "Alt_L":
			self.run()

	
	def run(self):
		# check if commands have been loaded
		if not self.commands:
			# load commands
			self.load_commands()
			
		self.commander_window.show_commander_window()
	
	
	
	def load_commands(self):
		self.commands = []
				
		for plugin in self.plugins_manager.plugins_array:
			if plugin.name != self.name and plugin.commands:
				for c in plugin.commands:
					self.commands.append(c)
		
		# add self commands!
		commands.set_commands(self)				
		print(len(self.commands))

	
	
