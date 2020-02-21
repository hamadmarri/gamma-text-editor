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
#	openfile: opens file(s) by showing open dialog and send filenames array
#	to files_manager.open_files method
#

import os
from urllib.parse import urlparse

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from . import opendir_commands as commands

class Plugin():
	
	def __init__(self, app):
		self.name = "opendir"
		self.app = app
		self.signal_handler = app.signal_handler
		self.plugins = app.plugins_manager.plugins
		self.commands = []
		
		
	def activate(self):
		self.signal_handler.key_bindings_to_plugins.append(self)
		commands.set_commands(self)
		
			
	
	# key_bindings is called by SignalHandler
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		
		if ctrl and shift and keyval_name == "O":
			self.opendir()
			
			
			
	def opendir(self):
		filenames = []
		
		# choosefile will display the open dialog
		dir_path = self.chooseDir()
		# print(dir_path)
		
		# if cancel button is pressed
		if not dir_path:
			return
		
		# otherwise, let files_manager controll open, read files, and
		# set new sourceviews to each file.
		for root, dirs, files in os.walk(dir_path, topdown=False):
			for filename in files:
				(name, ext) = os.path.splitext(filename)
				if name[0] != '.' and ext != ".pyc":
					#print(os.path.join(root, filename))
					filenames.append(os.path.join(root, filename))
		    	
		    
		
		
		if filenames:
			self.plugins["files_manager.files_manager"].open_files(filenames)
		    

	
	
	
	# show open dialog
	# (see: https://developer.gnome.org/gtk3/stable/GtkFileChooserDialog.html)
	# (see: https://developer.gnome.org/gtk3/stable/GtkFileChooser.html#GtkFileChooserAction)
	def chooseDir(self):
		final_path = None
		
		# initialize file chooser 
		dialog = Gtk.FileChooserDialog("Open Project", None,
										Gtk.FileChooserAction.SELECT_FOLDER,
										(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
										Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		
		# TODO: current folder must be dynamicly change
		dialog.set_current_folder("/home/hamad/dev/pygtk/gamma")
		
		# can select and open multiple files
		# dialog.set_select_multiple(True)

		# show the dialog		
		response = dialog.run()
		
		if response == Gtk.ResponseType.OK:
			dir_path = dialog.get_uri()
			p = urlparse(dir_path)
			final_path = os.path.abspath(os.path.join(p.netloc, p.path))
		# elif response == Gtk.ResponseType.CANCEL:
		#	print("Cancel clicked")

		# close and destroy dialog object
		dialog.destroy()
		return final_path



	# add files types filters
	# when user select "Python files" for example,
	# only python files are displyed
	# TODO: add more filters
	def add_filters(self, dialog):
		filter_text = Gtk.FileFilter()
		filter_text.set_name("Text files")
		filter_text.add_mime_type("text/plain")
		dialog.add_filter(filter_text)

		filter_py = Gtk.FileFilter()
		filter_py.set_name("Python files")
		filter_py.add_mime_type("text/x-python")
		dialog.add_filter(filter_py)

		filter_any = Gtk.FileFilter()
		filter_any.set_name("Any files")
		filter_any.add_pattern("*")
		dialog.add_filter(filter_any)
		
