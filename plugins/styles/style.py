import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class Plugin():
	
	def __init__(self, app):
		self.name = "style"
		self.app = app
		self.handlers = app.handler.handlers
		self.commands = []
		
		
	def activate(self):
		style_provider = Gtk.CssProvider()
		style_provider.load_from_path(self.app.config["style-path"])
		Gtk.StyleContext.add_provider_for_screen(
			Gdk.Screen.get_default(), style_provider,
			Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
		)
		
		
	
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		pass
