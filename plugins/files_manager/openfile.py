import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class Plugin():
	
	def __init__(self, app):
		self.name = "openfile"
		self.app = app
		self.builder = app.builder
		self.commands = []
		self.files_manager = None
		
		
	def activate(self):
		pass
		
	
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if ctrl and keyval_name == "o":
			self.openfile()
			
			
			
	def openfile(self):
		# get files_manager
		if not self.files_manager:
			self.files_manager = self.app.plugins_manager.get_plugin("files_manager")
		
		filename = self.choosefile()
		if not filename:
			return
		
		self.files_manager.open_file(filename)

	
	

	def choosefile(self):
		filename = None
		dialog = Gtk.FileChooserDialog("Open File", None,
										Gtk.FileChooserAction.OPEN,
										(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
										Gtk.STOCK_OPEN, Gtk.ResponseType.OK))


		self.add_filters(dialog)
		dialog.set_current_folder("/home/hamad/dev/pygtk/gamma")
		
		response = dialog.run()
		if response == Gtk.ResponseType.OK:
			print("Open clicked")
			print("File selected: " + dialog.get_filename())
			filename = dialog.get_filename()
		elif response == Gtk.ResponseType.CANCEL:
			print("Cancel clicked")

		dialog.destroy()
		return filename


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
		
