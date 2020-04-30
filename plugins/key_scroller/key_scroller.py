#
#### Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Mar 17th, 2020
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
from gi.repository import Gtk

from . import commands

class Plugin():

	def __init__(self, app):
		self.name = "key_scroller"
		self.app = app
		self.signal_handler = app.signal_handler
		self.THE = app.plugins_manager.THE
		self.commands = []
		self.signal_handler.key_bindings_to_plugins.append(self)
	
	
	def activate(self):
		pass


	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if ctrl and keyval_name == "Down":
			return self.scroll(1) # scroll down  
		elif ctrl and keyval_name == "Up":
			return self.scroll(-1) # scroll up

	
	def scroll(self, direction):
		current_file = self.THE("files_manager", "get_current_file", {})
		
		if not current_file:
			return
		
		sourceview = current_file.source_view
		v_adjustment = sourceview.get_vadjustment()
		
		scroll_value = v_adjustment.get_value()
		scroll_step = v_adjustment.get_step_increment()
		
		v_adjustment.set_value(scroll_value + (scroll_step * direction))
		sourceview.set_vadjustment(v_adjustment)
		
		return True
		
		
