#
#### Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Feb 11th, 2020
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
#
# window_ctrl: is responsible for handling basic window operations
# - Maximize, minimize, quit
#

from . import commands

class Plugin():
	
	def __init__(self, app):
		self.name = "window_ctrl"
		self.app = app
		self.builder = app.builder
		self.window = app.window
		self.handlers = app.handler.handlers
		self.is_maximized = None
		
		# commands and set_commands are important for
		# the commander plugin to know this plugin methods, key bindings, description
		self.commands = []
		commands.set_commands(self)
		
		self.set_handlers()
		self.message_notify = None
		self.openfile = None
		
	
	
	def activate(self):
		pass
	
	
	# setting handlers, see SignalHandler
	def set_handlers(self):
		self.handlers.on_closeBtn_release_event = self.on_closeBtn_release_event
		self.handlers.on_maximizeBtn_release_event = self.on_maximizeBtn_release_event
		self.handlers.on_minimizeBtn_release_event = self.on_minimizeBtn_release_event
		self.handlers.on_open_menu_button_press_event = self.on_open_menu_button_press_event
		
	
	
	# to use other plugins, need to get
	# the reference of the plugin by its name
	# need to cache the reference 
	def get_plugins_refs(self):
		# get message_notify
		if not self.message_notify:
			self.message_notify = self.app.plugins_manager.get_plugin("message_notify")
		
		# get message_notify
		if not self.openfile:
			self.openfile = self.app.plugins_manager.get_plugin("openfile")
			
	
	# this method got called by SignalHandler. Use it wisely
	# if your plugin spend much time in this method it will delay
	# other plugins when calling their key_bindings method
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if alt and ctrl and keyval_name == "m":
			self.minimize()
		elif alt and keyval_name == "m":
			self.toggle_maximize()
		elif ctrl and keyval_name == "q":
			self.quit()
			

	
	# iconify is the gtk method to minimize window
	def minimize(self):
		self.window.iconify()
		
		
		
	def toggle_maximize(self):
		if self.window.is_maximized():
			self.window.unmaximize()
		else:
			self.window.maximize()
			
			
	# before quit, need to stop any notify message
	# because of the thread sleep in message_notify
	# must cancel the thread		
	def quit(self):
		self.get_plugins_refs()
		self.message_notify.cancel()
		self.app.quit()
		
		
	def on_closeBtn_release_event(self, widget, event):
		self.quit()
	
	def on_maximizeBtn_release_event(self, widget, event):
		self.toggle_maximize()
	
	def on_minimizeBtn_release_event(self, widget, event):
		self.minimize()
	
	def on_open_menu_button_press_event(self, widget, event):
		self.get_plugins_refs()
		self.openfile.openfile()
		