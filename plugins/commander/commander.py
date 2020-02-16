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

class Plugin():
	
	def __init__(self, app):
		self.name = "commander"
		self.app = app
		self.plugins = app.plugins_manager.plugins
		self.handlers = app.handler.handlers
		self.commands = []
		self.only_alt = False
		self.set_handlers()
		
		
	def activate(self):
		pass
	
		
	def set_handlers(self):
		self.handlers.on_window_key_release_event = self.on_window_key_release_event
		
	
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
			for p in self.plugins:
				if p.commands:
					print(p.name)
					for c in p.commands:
						print(c["name"], c["shortcut"])
