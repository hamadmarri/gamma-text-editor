import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')
from gi.repository import Gtk, Gdk, GtkSource

from . import commands


class File():
	def __init__(self, filename, source_view):
		self.filename = filename
		self.source_view = source_view
	

class Plugin():
	
	def __init__(self, app):
		self.name = "files_manager"
		self.app = app
		self.builder = app.builder
		self.sourceview_manager = self.app.sourceview_manager
		self.scrolledwindow = app.builder.get_object("scrolledwindow")
		self.commands = []
		commands.set_commands(self)
		self.files = []
		self.current_file = File("empty", app.sourceview_manager.source_view)
		self.files.append(self.current_file)
		
	
	def activate(self):
		pass
		
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if ctrl and keyval_name == "f":
			for f in self.files:
				print(f.filename)
		elif ctrl and keyval_name == "w":
			# close current_file
			
			# if length > 2
			if len(self.files) > 1:
				self.switch_to_file(len(self.files) - 2)
				self.files[len(self.files) - 2].source_view.destroy()
				del self.files[len(self.files) - 2]
			else:
				# if signle file openned
				newsource = self.sourceview_manager.get_new_sourceview()
				self.replace_sourceview_widget(newsource)
				self.current_file = File("empty", newsource)
				self.files[0].source_view.destroy()
				del self.files[0]
				self.files.append(self.current_file)
				
			
			
		
			
	
	def open_file(self, filename):
		# check if file is already opened
		file_index = self.is_already_openned(filename)
		if file_index >= 0:
			print("is_already_openned")			
			self.switch_to_file(file_index)
			return
		
		
#		print("start load file")
		f = open(filename, "r")
		
		newsource = self.sourceview_manager.get_new_sourceview()
		self.replace_sourceview_widget(newsource)

		newfile = File(filename, newsource)
		
		# if empty file only there, replace it
		if len(self.files) == 1 and self.files[0].filename == "empty":
			self.files[0].source_view.destroy()
			del self.files[0]
		
		
		self.files.append(newfile)
		self.current_file = newfile
		self.current_file.source_view.get_buffer().set_text(f.read())
		f.close()
#		print("end load file")

		# get current buffer
		buffer = self.current_file.source_view.get_buffer()
		self.sourceview_manager.set_language(filename, buffer)
		
		print("file_opened")
		
		
	
	def replace_sourceview_widget(self, newsource):
		self.scrolledwindow.remove(self.current_file.source_view)
		self.scrolledwindow.add(newsource)
		self.sourceview_manager.update_sourcemap(newsource)
		
		
	def switch_to_file(self, file_index):
		# check if it is the current_file
		if self.current_file == self.files[file_index]:
			return
				
		f = self.files[file_index]
		
		self.scrolledwindow.remove(self.current_file.source_view)
		self.scrolledwindow.add(f.source_view)
		self.sourceview_manager.update_sourcemap(f.source_view)
		
		# reposition file in files list
		del self.files[file_index]
		self.files.append(f)
		self.current_file = f
		print(f"switch_to_file {f.filename}")
	
		
		
	def is_already_openned(self, filename):
		for i, f in enumerate(self.files):
			if filename == f.filename:
				return i	
		return -1
		
