#
#### Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Feb 26th, 2020
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


import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from . import commands

class Plugin():
	
	def __init__(self, app):
		self.name = "welcome"
		self.app = app
		self.plugins = app.plugins_manager.plugins
		self.signal_handler = app.signal_handler
		self.commands = []
		self.signal_handler.connect("startup", self.open_for_first_time)
		

	def activate(self):
		self.signal_handler.key_bindings_to_plugins.append(self)
		commands.set_commands(self)
		self.dir_path = os.path.dirname(os.path.realpath(__file__))

		
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if alt and keyval_name == "w":
			self.show_welcome()
	

			
	def show_welcome(self):
		files_mngr = self.plugins["files_manager.files_manager"]
		welcome_file = f"{self.dir_path}/welcome"
		
		files_mngr.open_files((welcome_file, ))
		sourceview = files_mngr.current_file.source_view
		sourceview.set_editable(False)
		

	def open_for_first_time(self):
		first_time_file = f"{self.dir_path}/first_time"
		not_first_time_file = f"{self.dir_path}/not_first_time"
		if os.path.isfile(first_time_file):
			os.rename(first_time_file, not_first_time_file)
			self.show_welcome()
