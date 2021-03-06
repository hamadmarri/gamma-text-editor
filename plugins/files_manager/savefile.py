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
#	savefile: saves the current_file openned or all editted files 
#	it gets current_file from files_manager plugin 
#	and saves it. Message notify is sent to tell the user
#	that the file is saved successfully
#  

import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from . import savefile_commands as commands

class Plugin():
	
	def __init__(self, app):
		self.name = "savefile"
		self.app = app
		self.signal_handler = app.signal_handler
		self.THE = app.plugins_manager.THE
		self.commands = []

		self.signal_handler.key_bindings_to_plugins.append(self)
		commands.set_commands(self)
		

	def activate(self):
		pass

	
	# key_bindings is called by SignalHandler
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):

		# save as is bound to "<Shift><Alt>+s"
		if shift and ctrl and keyval_name == "S":
			self.save_as()

		# save all is bound to "<Ctrl><Alt>+s"
		elif ctrl and alt and (keyval_name == "s" or keyval_name == "S"):
			self.save_all()

		# save is bound to "<Ctrl>+s"
		elif ctrl and (keyval_name == "s" or keyval_name == "S"):
			self.save_current_file()
		
	
	
	def save_as(self):
		# show save dialog
		new_filename = self.show_save_dialog()
		
		# if hit cancel, quit
		if not new_filename:
			return
		
		# get the current displayed file
		current_file = self.THE("files_manager", "get_current_file", {})
		
		buffer = current_file.source_view.get_buffer()

		# get all buffer text without the hidden markups
		text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
		
		# write file
		self.write_file(new_filename, text)
		
		# open the new saved as file
		self.THE("files_manager", "open_files", {"filenames": (new_filename,)})
		
		
		
		
	
	
	def save_all(self):
		editted_counter = self.THE("files_manager", "current_window_editted_counter", {})
		
		if editted_counter > 0:
			files = self.THE("files_manager", "current_window_files", {})
			
			# loop through all files objects
			# reversed so from user prespective "from top to bottom"
			for f in reversed(files):
				if f.editted:
					self.save_file(f)
					
					
					
	def save_current_file(self):
		# get the current displayed file
		current_file = self.THE("files_manager", "get_current_file", {})
		self.save_file(current_file)
		
	
	
	def save_file(self, file_object):
		# check if not editted then exit
		if not file_object.editted:
			return
		
		# get current buffer
		buffer = file_object.source_view.get_buffer()

		# get all buffer text without the hidden markups
		# (read: https://developer.gnome.org/gtk3/stable/GtkTextBuffer.html#gtk-text-buffer-get-text) 	
		text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
		
		# check if file is new
		if file_object.new_file:
			# switch to file to let the user 
			# know which file is it
			file_index = self.THE("files_manager", "get_file_index", {"filename": file_object.filename})
			self.THE("files_manager", "switch_to_file", {"file_index": file_index})
			new_filename = self.show_save_dialog()
			if new_filename:
				self.write_file(new_filename, text)
				self.THE("files_manager", "rename_file", {"file_object": file_object, "filename": new_filename})
				file_object.reset_editted()
				
				# set the language of new created file 
				# see sourceview_manager
				buffer = file_object.source_view.get_buffer()
				self.THE("sourceview_manager", "set_language", {
							"filename": new_filename,
							"buffer": buffer
						})
				
					
				# TODO: if saved(overwrite) a file in Hard Drive, but that file 
				# is already is open here! need to close old file 
		else:
			self.write_file(file_object.filename, text)
			file_object.reset_editted()
		
	
	
	
	
	def show_save_dialog(self):		
		# initialize file chooser 
		dialog = Gtk.FileChooserDialog("Save File", None,
										Gtk.FileChooserAction.SAVE,
				 						(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
										Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))
		
		dialog.set_current_folder(self.THE("files_manager", "get_directory" , {}))
		
		dialog.set_do_overwrite_confirmation(True);
		
		# show the dialog		
		response = dialog.run()
		
		filename = ""
		if response == Gtk.ResponseType.ACCEPT:
			filename = dialog.get_filename()

		# close and destroy dialog object
		dialog.destroy()
		return filename
		
		
		
			
	def write_file(self, filename, text):
		try:
			# save the file, in other words, copy text 
			# from buffer and write the file "current_file.filename"
			# in permenant storage (disk)
			f = open(filename, 'w', encoding='utf-8')
			f.write(text)
		
		except PermissionError as err:
			self.signal_handler.emit("log-error", self, f'Could not save {filename}: {err}')
		except OSError as err:
			self.signal_handler.emit("log-error", self, f'Could not save {filename}: {err}')
		else:
			# when successfully wrote the file, show successful message
			basename = os.path.basename(filename)
			self.THE("message_notifier", "show_message", {"m": f"{basename} | Saved", "state": 2})
			f.close()

			self.signal_handler.emit("file-saved", filename)

			


