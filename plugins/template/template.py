import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from . import commands


class Plugin():
	
	def __init__(self, app):
		self.name = "template"
		self.app = app
		self.commands = []
		commands.set_commands(self)
		
	def activate(self):
		pass
		
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		pass
		
	def method1(self):
		pass
		
	def method2(self):
		pass
	
	def method3(self):
		pass
