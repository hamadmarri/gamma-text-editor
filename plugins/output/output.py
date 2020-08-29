#
#### Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Mar 4th, 2020
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
#
#


from .output_gui import OutputGUI

class Plugin(OutputGUI):
	
	def __init__(self, app):
		self.name = "output"
		self.app = app
		self.THE = app.plugins_manager.THE
		self.commands = []
		self.copies = {}
		self.load_from_builder()


	def activate(self):
		pass
		
				
	def print(self, plugin_name, label, text):
		a_copy = self.show(plugin_name, label)
		buffer = a_copy["buffer"]
		buffer.insert(buffer.get_end_iter(), text, -1)
		
	
	def clear(self, plugin_name, label):
		# check if it is already shown
		a_copy = self.copies.get(plugin_name + label)
		
		if a_copy:
			self.clear_buffer(None, a_copy["buffer"])
	
	
	def show(self, plugin_name, label):
		# check if it is already shown
		a_copy = self.get_copy(plugin_name, label)
		
		# if no copy, create new one
		if not a_copy:
			print("not a_copy")
			
			a_copy = self.instantiate_widgets()
			a_copy["window"].set_title(label)
			a_copy["parent_window"] = self.app.window
			a_copy["plugin_name"] = plugin_name
			a_copy["label"] = label
			self.insert_copy(plugin_name, label, a_copy)
			
		self.show_output_gui(label, a_copy)
		
		return a_copy
		
		
		
	def insert_copy(self, plugin_name, label, a_copy):
		self.copies[str(self.app.window) + plugin_name + label] = a_copy


	def get_copy(self, plugin_name, label):
		return self.copies.get(str(self.app.window) + plugin_name + label)
	
	
	def delete_copy(self, a_copy):
		del self.copies[str(a_copy["parent_window"]) + a_copy["plugin_name"] + a_copy["label"]]
		
