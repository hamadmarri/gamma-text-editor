import gi
gi.require_version('GtkSource', '4')
from gi.repository import GtkSource


class Plugin():
	
	def __init__(self, app):
		self.name = "source_style"
		self.app = app
		self.builder = app.builder
		self.commands = []
	
	def activate(self):
		source_view = self.builder.get_object("view")
		buffer = source_view.get_buffer()
		manager = GtkSource.StyleSchemeManager.get_default()
		style = manager.get_scheme(self.app.config["style-scheme"])
		buffer.set_style_scheme(style)
		
		
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		pass
