import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')
from gi.repository import Gtk, Gdk, GtkSource

class Plugin():
	
	def __init__(self, app):
		self.name = "openfile"
		self.app = app
		self.builder = app.builder
		self.source_view = self.builder.get_object("view")
		self.buffer = self.source_view.get_buffer()
		self.current_file = ""
		self.commands = []
		
		
	def activate(self):
		pass
		
	
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if ctrl and keyval_name == "o":
			self.openfile()
		elif ctrl and keyval_name == "s":
			text = self.buffer.get_text(self.buffer.get_start_iter(), self.buffer.get_end_iter(), True)
			try:
				open(self.current_file, 'w').write(text)
			except SomeError as err:
				print('Could not save %s: %s' % (filename, err))
			
			
			
			
	def openfile(self):
		filename = self.choosefile()
		if not filename:
			return
		
		self.current_file = filename
		
#		print("start load file")
		f = open(filename, "r")
		source_view = self.builder.get_object("view")
		source_view.get_buffer().set_text(f.read())
		f.close()
#		print("end load file")

		self.set_language(f.name)
	
	

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
			
			
			
	def set_language(self, filename):
		lm = GtkSource.LanguageManager.get_default()
		lan = lm.guess_language(filename)
		if lan:
			self.buffer.set_highlight_syntax(True)
			self.buffer.set_language(lan)
		else:
			print('No language found for file "cen"')
			self.buffer.set_highlight_syntax(False)
