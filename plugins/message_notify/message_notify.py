import threading
import time

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from . import commands


class Plugin():
	
	def __init__(self, app):
		self.name = "message_notify"
		self.app = app
		self.builder = app.builder
		self.commands = []
		self.messageLbl = None
		self.message_time = 7.5 # 7.5 seconds
		self.timer = None
		
		
	def activate(self):
		self.messageLbl = self.builder.get_object("messageLbl")
		self.clear_message()
		
		
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		pass
	
		
	def show_message(self, m):
		self.cancel()
		
		self.messageLbl.set_text(m)
		self.timer = threading.Timer(self.message_time, self.clear_message)
		self.timer.start()
	
	def clear_message(self):
		self.timer = None
		self.messageLbl.set_text("")
	
	
	def cancel(self):
		if self.timer:
			self.timer.cancel()
