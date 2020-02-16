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
#	TODO:	toolbar_files must be handled by a ui manager
#			which show opened files in many forms (list, tree, ..)
#
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from . import commands


# each openned file is set in File object and
# appended to "files" array
class File():
	def __init__(self, filename, source_view, toolbar_file = None):
		self.filename = filename
		self.source_view = source_view
		self.toolbar_file = toolbar_file
	

class Plugin():
	
	def __init__(self, app):
		self.name = "files_manager"
		self.app = app
		self.builder = app.builder
		self.sourceview_manager = app.sourceview_manager
		self.scrolledwindow = None
		self.commands = []
		commands.set_commands(self)
		self.files = []
		self.current_file = None
		self.headerbar = None
		self.message_notify = None

		
	
	def activate(self):
		# scrolledwindow is object that contains sourceviews
		# basically, a new opened file has its own sourceview 
		# and got added to scrolledwindow
		# previouse sourceview got removed from scrolledwindow
		self.scrolledwindow = self.builder.get_object("source_scrolledwindow")
		
		# default empty file when open editor with no opened files
		self.current_file = File("empty", self.sourceview_manager.source_view)
		
		# add empty/current_file to files array
		self.files.append(self.current_file)
		
		# get headerbar widget reference, to show current filename
		# in headerbar label
		self.headerbar = self.builder.get_object("headerbarMain")
		
	
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
			self.replace_sourceview_widget(self.current_file.source_view, newsource)
			
			# current file is now empty
			self.current_file = File("empty", newsource)
			
			# destroy opened file 
			self.destroy_file(0)
			
			# append empty file to "files" array
			self.files.append(self.current_file)
			
			# since it is an empty file, set the headerbar to "Gamma"
			self.headerbar.set_title("Gamma")
			
			# cancel and clear message 
			# why? sometimes user save a file and close it right after,
			# so no need to keep showing that file is saved
			self.message_notify.cancel()
			
	
	

	def destroy_file(self, file_index):
		# destroy the sourceview attached to file 
		self.files[file_index].source_view.destroy()
		
		# destroy the toolbar_file btn attached to file TODO: move to ui manager
		self.files[file_index].toolbar_file.destroy()
		
		# remove from "files" array
		del self.files[file_index]
	
	
	
	
	# open_files is called by openfile plugin 
	# it loops through all filenames and open each one
	# by calling open_file method
	def open_files(self, filenames):
		for f in filenames:
			self.open_file(f)
			
	
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
		self.replace_sourceview_widget(self.current_file.source_view, newsource)
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
		
		# close file object
		f.close()
		# DEBUG: print(f"{filename} closed")
		
		
		# set the language of just openned file 
		# see sourceview_manager
		buffer = newsource.get_buffer()
		self.sourceview_manager.set_language(filename, buffer)
		# DEBUG: print("set_language")
		
		# adds ui button with filename label in toolbar_file
		# (the left side panel)
		# TODO: move to ui manager plugin
		
		# get toolbar_files Gtk widget from ui file
		toolbar_files = self.builder.get_object("toolbar_files")
		
		# create new button
		btn = Gtk.Button()
		
		# associate btn widget to File object
		newfile.toolbar_file = btn
		
		# set the text of button to filename
		basename = os.path.basename(filename)
		btn.set_label(basename)

		# connect clicked signal to side_file_clicked method		
		btn.connect("clicked", self.side_file_clicked, filename)
		
		# set the ui/css class to the button (.openned_file)
		btn.get_style_context().add_class("openned_file")
		
		# get the label of the button, and set left padding to 0
		lbl = btn.get_children()[0]
		lbl.set_xalign(0)
		
		# add button to toolbar_files
		# (read: https://developer.gnome.org/gtk3/stable/GtkBox.html#gtk-box-pack-start)
		toolbar_files.pack_start(btn, False, False, 0)
		
		# position new opened file's button to top of toolbar_files
		# (read: https://developer.gnome.org/gtk3/unstable/GtkBox.html#gtk-box-reorder-child)
		toolbar_files.reorder_child(btn, 0)
		
		# show the widget
		btn.show()
		
		
		# set headerbar text to the filename
		self.update_header(filename)
		# DEBUG: print("update_header")
		
		# set current file to this file
		self.current_file = newfile
		
		
		
	
	# handler of "clicked" event
	# it switch the view to the filename in clicked button
	def side_file_clicked(self, btn, filename):
	
		# is_already_openned gets the index of the file in "files" array
		file_index = self.is_already_openned(filename)
		
		# if found, which should!, switch to it
		if file_index >= 0:
			self.switch_to_file(file_index)
	
	
		
	# TODO: must handled by ui manager
	# TODO: there is a bug here
	# (gamma.py:12008): Gtk-CRITICAL **: 19:46:38.608: gtk_bin_remove: assertion 'priv->child == child' failed
	def replace_sourceview_widget(self, previouse_source, newsource):
	
		# remove previously displayed sourceview
		# DEBUG: print("scrolledwindow.remove before")
		prev_child = self.scrolledwindow.get_child()
		# DEBUG: print(prev_child)
		if prev_child:
			self.scrolledwindow.remove(prev_child)
		# DEBUG: print("scrolledwindow.remove")
		
		# add the newsource view
		self.scrolledwindow.add(newsource)
		# DEBUG: print("scrolledwindow.add")
		
		# need to update the mini map too
		self.sourceview_manager.update_sourcemap(newsource)
		# DEBUG: print("sourceview_manager.update_sourcemap")

		
	
	def switch_to_file(self, file_index):
		# check if it is the current_file, then exit method 
		if self.current_file == self.files[file_index]:
			return
				
		# get file object
		f = self.files[file_index]
		
		# replace the source view 
		self.replace_sourceview_widget(self.current_file.source_view, f.source_view)
				
		# reposition file in files list
		del self.files[file_index]
		self.files.append(f)
		self.current_file = f
				
		# update headerbar to filename
		self.update_header(f.filename)
		
		
	

	# returns file index if found or -1
	def is_already_openned(self, filename):
		for i, f in enumerate(self.files):
			if filename == f.filename:
				return i	
		return -1
		
	
	# updates the headerbar by filename
	def update_header(self, filename):
		# get message_notify
		if not self.message_notify:
			self.message_notify = self.app.plugins_manager.get_plugin("message_notify")
		
		# gets basename of the file, not the full path
		basename = os.path.basename(filename)
		
		# set the title of headerbar
		self.headerbar.set_title(basename)
		
		# show message of the full path of the file 
		# it is useful to avoid confusion when having 
		# different files with similar names in different paths
		self.message_notify.show_message(filename)
	
