#
#### Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Feb 27th, 2020
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



from . import commands
from .copy_line import CopyLine

class Plugin(CopyLine):
	
	def __init__(self, app):
		self.name = "fast_copy_cut_duplicate"
		self.app = app
		self.plugins = app.plugins_manager.plugins
		self.signal_handler = app.signal_handler 
		self.commands = []
	
	def activate(self):
		self.signal_handler.key_bindings_to_plugins.append(self)
		commands.set_commands(self)

	
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if ctrl and keyval_name == "c":
			self.copy_line()
	

	def cut_line(self):
		pass
	
	def duplicate_line(self):
		pass
		
