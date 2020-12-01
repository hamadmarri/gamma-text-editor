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
from pathlib import Path

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from . import commands

class Plugin():
	
	def __init__(self, app):
		self.name = "welcome"
		self.app = app
		self.THE = app.plugins_manager.THE
		self.signal_handler = app.signal_handler
		self.commands = []

		self.signal_handler.key_bindings_to_plugins.append(self)
		commands.set_commands(self)

		self.dir_path = os.path.dirname(os.path.realpath(__file__))
		self.location = str(Path.home()) + "/.config/gamma-text-editor/"

		self.signal_handler.connect("startup", self.open_for_first_time)


	def activate(self):
		pass

		
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if alt and keyval_name == "w":
			self.show_welcome()
	

			
	def show_welcome(self):
		welcome_file = f"{self.dir_path}/welcome"
		
		self.THE("files_manager", "open_files", {"filenames": (welcome_file, )})
		current_file = self.THE("files_manager", "get_current_file", {})
		
		if not current_file:
			return
			
		source_view = current_file.source_view
		if source_view:
			source_view.set_editable(False)


	def open_for_first_time(self):
		Path(self.location).mkdir(parents=True, exist_ok=True)

		not_first_time_file = f"{self.location}/not_first_time"
		if not os.path.isfile(not_first_time_file):
			f = open(not_first_time_file, "w")
			f.close()
			self.show_welcome()





