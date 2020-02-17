
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
#	savefile: saves the current_file openned 
#	it gets current_file from files_manager plugin 
#	and saves it. Message notify is sent to tell the user
#	that the file is saved successfully
#  

import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# TODO: only save when buffer is changed
# TODO: empty file is saved at home!
class Plugin():
	
	def __init__(self, app):
		self.name = "savefile"
		self.app = app
		self.signal_handler = app.signal_handler
		self.plugins = app.plugins_manager.plugins
		self.commands = []

		
	def activate(self):
		self.signal_handler.key_bindings_to_plugins.append(self)
		
	
	# key_bindings is called by SignalHandler
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		
		# save is bound to "<Ctrl>+s"
		if ctrl and keyval_name == "s":
			
			# get the current displayed file
			current_file = self.plugins["files_manager.files_manager"].current_file
			
			# get current buffer
			buffer = current_file.source_view.get_buffer()

			# get all buffer text without the hidden markups
			# (read: https://developer.gnome.org/gtk3/stable/GtkTextBuffer.html#gtk-text-buffer-get-text) 	
			text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
			
			# check if file is new
			if current_file.new_file:
				new_filename = self.show_save_dialog()
				if new_filename:
					self.save_file(new_filename, text)
					self.plugins["files_manager.files_manager"].convert_new_empty_file(current_file, new_filename)
			else:
				self.save_file(current_file.filename, text)
	
	
	
	
	def show_save_dialog(self):		
		# initialize file chooser 
		dialog = Gtk.FileChooserDialog("Save File", None,
										Gtk.FileChooserAction.SAVE,
										(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
										Gtk.STOCK_SAVE, Gtk.ResponseType.ACCEPT))
		
		# TODO: current folder must be dynamicly change
		dialog.set_current_folder("/home/hamad/dev/pygtk/gamma")
		
		dialog.set_do_overwrite_confirmation(True);
		
		# show the dialog		
		response = dialog.run()
		
		filename = ""
		if response == Gtk.ResponseType.ACCEPT:
			filename = dialog.get_filename()

		# close and destroy dialog object
		dialog.destroy()
		return filename
		
		
		
			
	def save_file(self, filename, text):
		try:
			# save the file, in other words, copy text 
			# from buffer and write the file "current_file.filename"
			# in permenant storage (disk)
			f = open(filename, 'w')
			f.write(text)
		except SomeError as err:
			print('Could not save %s: %s' % (filename, err))
		else:
			# when successfully wrote the file, show successful message
			basename = os.path.basename(filename)
			self.plugins["message_notify.message_notify"].show_message(basename + " | Saved")
		finally:
			f.close()
			print(f"{basename} saved and closed")
			
