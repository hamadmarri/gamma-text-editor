import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class Plugin():
	
	def __init__(self, app):
		self.name = "commander"
		self.app = app
		self.plugins = app.plugins_manager.plugins
		self.handlers = app.handler.handlers
		self.commands = []
		self.only_alt = False
		self.set_handlers()
		
		
	def activate(self):
		pass
	
		
	def set_handlers(self):
		self.handlers.on_window_key_release_event = self.on_window_key_release_event
		
	
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if not alt:
			self.only_alt = True
		else:
			self.only_alt = False
			

	def on_window_key_release_event(self, window, event):
		keyval_name = Gdk.keyval_name(event.keyval)
		ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
		alt = (event.state & Gdk.ModifierType.MOD1_MASK)
		shift = (event.state & Gdk.ModifierType.SHIFT_MASK)
		
		if alt and self.only_alt and keyval_name == "Alt_L":
			for p in self.plugins:
				if p.commands:
					print(p.name)
					for c in p.commands:
						print(c["name"], c["shortcut"])
