import sys

import gi
from gi.repository import Gdk


class Handlers(object):
	pass
	

class SignalHandler:
	def __init__(self, app):
		self.app = app
		self.builder = app.builder
		self.plugins = app.plugins
		self.handlers = Handlers()
		self.set_handlers()
		
		
	def set_handlers(self):
		self.handlers.on_window_key_press_event = self.on_window_key_press_event
		self.handlers.resizeBodySide = self.resizeBodySide
		self.handlers.resizeHeaderSide = self.resizeHeaderSide

		
		
	def on_window_key_press_event(self, window, event):
		keyval_name = Gdk.keyval_name(event.keyval)
		ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
		alt = (event.state & Gdk.ModifierType.MOD1_MASK)
		shift = (event.state & Gdk.ModifierType.SHIFT_MASK)		
			
		for p in self.plugins:
			p.key_bindings(event, keyval_name, ctrl, alt, shift)


	
	def resizeBodySide(self, bodyPaned, param):
		headerPaned = self.builder.get_object("headerPaned")
		headerPaned.set_position(bodyPaned.get_position())
		
		
	def resizeHeaderSide(self, headerPaned, param):
		bodyPaned = self.builder.get_object("bodyPaned")
		bodyPaned.set_position(headerPaned.get_position())
			
