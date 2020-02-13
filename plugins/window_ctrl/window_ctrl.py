import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')
from gi.repository import Gtk, Gdk, GtkSource

from . import commands

class Plugin():
	
	def __init__(self, app):
		self.name = "window_ctrl"
		self.app = app
		self.window = app.window
		self.handlers = app.handler.handlers
		self.is_maximized = self.window.is_maximized()
		self.commands = []
		commands.set_commands(self)
		self.set_handlers()
		
	def activate(self):
		pass
	
	def set_handlers(self):
		self.handlers.on_closeBtn_release_event = self.on_closeBtn_release_event
		self.handlers.on_maximizeBtn_release_event = self.on_maximizeBtn_release_event
		self.handlers.on_minimizeBtn_release_event = self.on_minimizeBtn_release_event
		self.handlers.on_closeBtn_hover_event = self.on_closeBtn_hover_event
	
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if alt and ctrl and keyval_name == "m":
			self.minimize()
		elif alt and keyval_name == "m":
			self.toggle_maximize()
		elif ctrl and keyval_name == "q":
			self.quit()
			

	
	
	def minimize(self):
		self.window.iconify()
		
		
	def toggle_maximize(self):
		if self.is_maximized:
			self.window.unmaximize()
		else:
			self.window.maximize()
			
		self.is_maximized = not self.is_maximized

		
	def quit(self):
		self.app.quit()
		
		
	
	def on_closeBtn_hover_event(self, widget, event):
		print("on_closeBtn_hover_event")
		
	def on_closeBtn_release_event(self, widget, event):
		self.quit()
	
	def on_maximizeBtn_release_event(self, widget, event):
		self.toggle_maximize()
	
	def on_minimizeBtn_release_event(self, widget, event):
		self.minimize()
		
