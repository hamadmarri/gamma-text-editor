import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')
from gi.repository import Gtk, Gdk, GtkSource

from . import commands


class File():
	def __init__(self, filename, buffer_text):
		self.filename = filename
		self.buffer_text = buffer_text
	

class Plugin():
	
	def __init__(self, app):
		self.name = "files_manager"
		self.app = app
		self.builder = app.builder
		self.source_view = self.builder.get_object("view")
		self.commands = []
		commands.set_commands(self)
		self.files = []
		self.current_file = None
		
	
	def activate(self):
		pass
		
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if ctrl and keyval_name == "f":
			for f in self.files:
				print(f.filename)
		
		
	
	def save_current_file_state(self):
		if self.current_file:
			buffer = self.source_view.get_buffer()
			self.current_file.buffer_text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
		
	
	
	def open_file(self, filename):
		# check if file is already opened
		file_index = self.is_already_openned(filename)
		if file_index >= 0:
			print("is_already_openned")			
			self.switch_to_file(file_index)
			return
		
		# save the state of current file buffer
		self.save_current_file_state()
		
#		print("start load file")
		f = open(filename, "r")
		source_view = self.builder.get_object("view")
		source_view.get_buffer().set_text(f.read())
		f.close()
#		print("end load file")

		# get current buffer
		buffer = self.source_view.get_buffer()
		self.set_language(filename, buffer)
		
		f = File(filename, buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False))
		self.files.append(f)
		self.current_file = f
		print("file_opened")
		
		
		
	def switch_to_file(self, file_index):
		# check if it is the current_file
		if self.current_file == self.files[file_index]:
			return
		
		# save the state of current file buffer
		self.save_current_file_state()
				
		f = self.files[file_index]
		self.source_view.get_buffer().set_text(f.buffer_text)
		self.set_language(f.filename, self.source_view.get_buffer())
		
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
		
	
	def set_language(self, filename, buffer):
		lm = GtkSource.LanguageManager.get_default()
		lan = lm.guess_language(filename)
		if lan:
			buffer.set_highlight_syntax(True)
			buffer.set_language(lan)
		else:
			print('No language found for file "cen"')
			buffer.set_highlight_syntax(False)
