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
gi.require_version('GtkSource', '4')
from gi.repository import Gtk, Gdk, GtkSource


# TODO: only save when buffer is changed
class Plugin():
	
	def __init__(self, app):
		self.name = "savefile"
		self.app = app
		self.builder = app.builder
		self.commands = []
		self.files_manager = None
		
		
	def activate(self):
		pass
		
	
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if ctrl and keyval_name == "s":
			
			# get current_file
			if not self.files_manager:
				self.files_manager = self.app.plugins_manager.get_plugin("files_manager")
			
			current_file = self.files_manager.current_file
			
			# get current buffer
			buffer = current_file.source_view.get_buffer()
			
			text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
			try:
				open(current_file.filename, 'w').write(text)
			except SomeError as err:
				print('Could not save %s: %s' % (filename, err))
			

