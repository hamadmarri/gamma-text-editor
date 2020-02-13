import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')
from gi.repository import Gtk, Gdk, GtkSource

class Plugin():
	
	def __init__(self, app):
		self.name = "savefile"
		self.app = app
		self.builder = app.builder
		self.commands = []
		self.files_manager = None
		
		
	def activate(self):
		pass
		
	
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if ctrl and keyval_name == "s":
			
			# get current_file
			if not self.files_manager:
				self.files_manager = self.app.plugins_manager.get_plugin("files_manager")
			
			current_file = self.files_manager.current_file
			
			# get current buffer
			buffer = current_file.source_view.get_buffer()
			
			# TODO: buffer is cached in files_manager
			text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
			try:
				open(current_file.filename, 'w').write(text)
			except SomeError as err:
				print('Could not save %s: %s' % (filename, err))
			

