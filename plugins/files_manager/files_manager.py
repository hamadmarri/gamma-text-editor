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
#	files_manager: is responsible to manage all opened documents.
#
#
#

import os
from pathlib import Path

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from . import files_manager_commands as commands

from .file import File
from .create_file_mixin import CreateFileMixin
from .close_file_mixin import CloseFileMixin
from .open_file_mixin import OpenFileMixin
from .commands_ctrl import CommandsCtrl


class Plugin(CommandsCtrl, CreateFileMixin, CloseFileMixin, OpenFileMixin):

	def __init__(self, app):
		self.name = "files_manager"
		self.app = app
		self.signal_handler = app.signal_handler
		self.THE = app.plugins_manager.THE
		self.commands = []
		self.current_directory = str(Path.home())
		self.counter = 1

		self.signal_handler.key_bindings_to_plugins.append(self)
		commands.set_commands(self)


	def activate(self):
		# default empty file when open editor with no opened files
		self.app.window.current_file = File(self, "empty",
											self.app.builder.get_object("view"),
											new_file=True, init_file=True)

		# initialize files array and bind it to current window
		self.app.window.files = []

		# initialize files editted counter and bind it to current window
		self.app.window.editted_counter = 0

		# add empty/current_file to files array
		self.app.window.files.append(self.app.window.current_file)

		self.signal_handler.emit("file-switched", self.app.window.current_file.source_view)



	# key_bindings is called by SignalHandler
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		# close current file is bound to "<Ctrl>+w"
		if ctrl and keyval_name == "w":
			# close current_file
			self.close_current_file()
		elif shift and ctrl and keyval_name == "W":
			self.close_all()
		elif ctrl and keyval_name == "n":
			self.create_new_file()



	def current_window_files(self):
		return self.app.window.files


	def files_len(self):
		return len(self.app.window.files)


	def current_window_editted_counter(self):
		return self.app.window.editted_counter


	def current_window_editted_counter_add(self, value):
		self.app.window.editted_counter += value

	def get_current_file(self):
		return self.app.window.current_file

	def set_current_file(self, file_object):
		self.app.window.current_file = file_object


	def rename_file(self, file_object, filename):
		# check if it is the new init file, need to make new sourceview and be added to ui
		if file_object.init_file:
			self.duplicate_init_file(file_object, filename)

		# if new file added by the user
		else:
			# rename in array

			# remove old command in commander
			self.update_commanders_remove(file_object)

			# rename file
			file_object.filename = filename

			# attach parent directory to file
			self.set_parent_dir(file_object)

			# add new commander for the file
			self.update_commanders_add(file_object)

			file_object.new_file = False	# not new anymore
			self.THE("ui_manager", "rename_file", {"file_object": file_object})





	def duplicate_init_file(self, file_object, filename):
		newsource = self.THE("sourceview_manager", "get_new_sourceview", {})

		# default empty file when open editor with no opened files
		newfile = File(self, filename, newsource)

		# copy text from init file to newfile
		buffer = file_object.source_view.get_buffer()
		text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True)
		newsource.get_buffer().set_text(text)
		file_object.source_view.get_buffer().set_text("")

		# add newfile to files array
		self.add_file_to_list(newfile)

		self.THE("ui_manager", "add_filename_to_ui", {"newfile", newfile})
		self.switch_to_file(self.files_len() - 1)



	# handler of "clicked" event
	# it switch the view to the filename in clicked button
	def side_file_clicked(self, filename):
		self.switch_to_file_by_filename(filename)


	def switch_to_file_by_filename(self, filename):
		# is_already_openned gets the index of the file in "files" array
		file_index = self.is_already_openned(filename)

		# if found, which should!, switch to it
		if file_index >= 0:
			self.switch_to_file(file_index)


	def switch_to_file(self, file_index):

		if file_index < 0:
			return

		# check if it is the current_file, then exit method
		if self.app.window.current_file == self.app.window.files[file_index]:
			return

		buffer = self.app.window.current_file.source_view.get_buffer()
		self.THE("highlighter", "remove_highlight", {"buffer": buffer})

		# get file object
		f = self.app.window.files[file_index]

		# replace the source view
		self.THE("ui_manager", "replace_sourceview_widget", {"newsource": f.source_view})

		self.app.window.current_file = f

		# update ui, set selected
		self.THE("ui_manager", "set_currently_displayed", {"box": self.app.window.current_file.ui_ref})

		# update headerbar to filename
		self.THE("ui_manager", "update_header", {"filename": f.filename, "editted": f.editted})

		# show message of the full path of the file
		# it is useful to avoid confusion when having
		# different files with similar names in different paths
		self.THE("message_notifier", "show_message", {"m": f.filename})

		self.signal_handler.emit("file-switched", self.app.window.current_file.source_view)

		f.loaded = True


	def is_file_loaded(self, file_index):
		if file_index < 0:
			return False

		return self.app.window.files[file_index].loaded == True


	# returns file index if found or -1
	def is_already_openned(self, filename):
		return self.get_file_index(filename)




	def get_file_index(self, filename):
		for i, f in enumerate(self.app.window.files):
			if filename == f.filename:
				return i
		return -1



	def set_parent_dir(self, aFile):
		# attach parent directory to file
		parent_dir = os.path.dirname(aFile.filename)
		aFile.parent_dir = parent_dir


	def add_file_to_list(self, newfile):
		self.set_parent_dir(newfile)
		self.app.window.files.append(newfile)
		self.update_commanders_add(newfile)


	def remove_file_from_list(self, file_object, file_index):
		self.update_commanders_remove(file_object)
		del self.app.window.files[file_index]


	def get_directory(self):
		if self.app.window.current_file.parent_dir:
			return self.app.window.current_file.parent_dir

		return self.current_directory

