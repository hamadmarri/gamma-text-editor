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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from . import commands


# each openned file is set in File object and
# appended to "files" array
class File():
	def __init__(self, filename, source_view, ui_ref=None,
					need_save=False, new_file=False):
		self.filename = filename
		self.source_view = source_view
		self.ui_ref = ui_ref
		self.need_save = need_save
		self.new_file = new_file
	

class Plugin():
	
	def __init__(self, app):
		self.name = "files_manager"
		self.app = app
		self.signal_handler = app.signal_handler
		self.builder = app.builder
		self.plugins = app.plugins_manager.plugins
		self.sourceview_manager = app.sourceview_manager
		self.commands = []
		commands.set_commands(self)
		self.files = []
		self.current_file = None
		
	
	def activate(self):
		self.signal_handler.key_bindings_to_plugins.append(self)
		
		# default empty file when open editor with no opened files
		self.current_file = File("empty", self.sourceview_manager.source_view, new_file=True)

		# add empty/current_file to files array
		self.files.append(self.current_file)
		
		
				
	
	# key_bindings is called by SignalHandler
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):		
		# close current file is bound to "<Ctrl>+w"
		# TODO: check if need saving before close
		if ctrl and keyval_name == "w":
			# close current_file
			self.close_current_file()
			
	
	# TODO: check if need saving before close
	def close_current_file(self):
		# if length > 2, then close current and switch to previouse file 
		# in "files" array
		if len(self.files) > 1:
			# first switch to previouse openned file
			self.switch_to_file(len(self.files) - 2)
			
			# destroy file, after switching, the current file 
			# become second last in the "files" array
			self.destroy_file(len(self.files) - 2)
		
		
		# if empty file only there, do nothing
		elif len(self.files) == 1 and self.files[0].filename == "empty":
			return
			
			
		# if signle file openned, close and make empty file to stay 
		# in the view
		else:
			# new sourceview for the empty file
			newsource = self.sourceview_manager.get_new_sourceview()
			
			# remove current sourceview and put the new empty sourceview
			self.plugins["ui_manager.ui_manager"].replace_sourceview_widget(newsource)
			
			# current file is now empty
			self.current_file = File("empty", newsource, new_file=True)
			
			# destroy opened file 
			self.destroy_file(0)
			
			# append empty file to "files" array
			self.files.append(self.current_file)
			
			# since it is an empty file, set the headerbar to "Gamma"
			self.plugins["ui_manager.ui_manager"].set_header("Gamma")
			
			# cancel and clear message 
			# why? sometimes user save a file and close it right after,
			# so no need to keep showing that file is saved
			self.plugins["message_notify.message_notify"].cancel()
			
	
	

	def destroy_file(self, file_index):
		# destroy the sourceview attached to file 
		self.files[file_index].source_view.destroy()
		
		# destroy the ui_ref btn attached to file TODO: move to ui manager
		self.files[file_index].ui_ref.destroy()
		
		# remove from "files" array
		del self.files[file_index]
	
	
	
	
	# open_files is called by openfile plugin 
	# it loops through all filenames and open each one
	# by calling open_file method
	def open_files(self, filenames):
		for f in filenames:
			self.open_file(f)
		
		# set headerbar text to the filename
		self.plugins["ui_manager.ui_manager"].update_header(self.current_file.filename)
		
		# update ui, set selected
		self.plugins["ui_manager.ui_manager"].set_currently_displayed(self.current_file.ui_ref)
			
	
	# TODO: this method is doing too much, must get seperated
	def open_file(self, filename):
		# check if file is already opened
		file_index = self.is_already_openned(filename)
		if file_index >= 0:
			# if already open then just switch to it and exit method
			self.switch_to_file(file_index)
			return
		
		
		# open the file in reading mode
		f = open(filename, "r")
		# DEBUG: print(f"{filename} opened")
		
		
		# get new sourceview from sourceview_manager
		# TODO: must handled by ui manager
		newsource = self.sourceview_manager.get_new_sourceview()
		# DEBUG: print("newsource")
		
		# replace old sourceview(previously opened) with this new one
		self.plugins["ui_manager.ui_manager"].replace_sourceview_widget(newsource)
		# DEBUG: print("replace_sourceview_widget")
		
		# new File object
		newfile = File(filename, newsource)
		# DEBUG: print("newfile")
		
		# if empty file only is currently opened, replace it
		if len(self.files) == 1 and self.files[0].filename == "empty":
			self.files[0].source_view.destroy()
			del self.files[0]
		
		# add newfile object to "files" array
		self.files.append(newfile)
		# DEBUG: print("files.append")
		
		# actual reading from the file and populate the new sourceview buffer
		# with file data
		text = f.read()
		# DEBUG: print("text is read")
				
		newsource.get_buffer().set_text(text)
				
		# place cursor at the begining
		newsource.get_buffer().place_cursor(newsource.get_buffer().get_start_iter())
		
		# close file object
		f.close()
		# DEBUG: print(f"{filename} closed")
		
		# set the language of just openned file 
		# see sourceview_manager
		buffer = newsource.get_buffer()
		self.sourceview_manager.set_language(filename, buffer)
		# DEBUG: print("set_language")
		
		self.plugins["ui_manager.ui_manager"].add_filename_to_ui(newfile)
				
		# set current file to this file
		self.current_file = newfile
		
	
	
	def convert_new_empty_file(self, newfile, filename):
		newfile.filename = filename
		newfile.new_file = False
		self.plugins["ui_manager.ui_manager"].add_filename_to_ui(newfile)
	
	
	
	# handler of "clicked" event
	# it switch the view to the filename in clicked button
	def side_file_clicked(self, filename):
	
		# is_already_openned gets the index of the file in "files" array
		file_index = self.is_already_openned(filename)
		
		# if found, which should!, switch to it
		if file_index >= 0:
			self.switch_to_file(file_index)
	
		
	
	def switch_to_file(self, file_index):
		# check if it is the current_file, then exit method 
		if self.current_file == self.files[file_index]:
			return
				
		# get file object
		f = self.files[file_index]
		
		# replace the source view 
		self.plugins["ui_manager.ui_manager"].replace_sourceview_widget(f.source_view)
				
		# reposition file in files list
		del self.files[file_index]
		self.files.append(f)
		self.current_file = f
				
		# update headerbar to filename
		self.plugins["ui_manager.ui_manager"].update_header(f.filename)
		
		

	# returns file index if found or -1
	def is_already_openned(self, filename):
		for i, f in enumerate(self.files):
			if filename == f.filename:
				return i	
		return -1
		
