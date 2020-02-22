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


#import threading
import time

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GObject


from . import commands
from . import commander_window as cw



class Plugin():
	
	def __init__(self, app):
		self.name = "commander"
		self.app = app
		self.builder = app.builder
		self.plugins_manager = app.plugins_manager
		self.plugins = app.plugins_manager.plugins
		self.signal_handler = app.signal_handler
		self.handlers = app.signal_handler.handlers
		self.commands = None
		self.dynamic_commands = []
		self.only_ctrl = False
		self.commander_window = cw.CommanderWindow(app, self)
		
		# when user hold ctrl for long time
		# but never used key bindings, then
		# no need to show commander 
		# it is annoying to show commander 
		# when user hold ctrl but then changed
		# their mind (i.e. ctrl+c to copy something 
		# but changed their mind before hit the 'c'
		# when relaeas ctrl (without timing) commander 
		# will show which is not good
		# but with timing if ctrl is helf for self.max_time
		# then open commander will fire 
		self.t0 = 0
		self.max_time = 0.2 # was 0.3 
		self.cache_thread = None
		
		
	def activate(self):
		self.signal_handler.key_bindings_to_plugins.append(self)
		self.signal_handler.any_key_press_to_plugins.append(self)
		self.set_handlers()
		self.cache_commands()
		

	def set_handlers(self):
		self.handlers.on_window_key_release_event = self.on_window_key_release_event
		self.handlers.on_commanderWindow_key_press_event = self.commander_window.on_commanderWindow_key_press_event
		self.handlers.on_commanderWindow_key_release_event = self.commander_window.on_commanderWindow_key_release_event
		self.handlers.on_commanderWindow_focus_out_event = self.commander_window.on_commanderWindow_focus_out_event
		self.handlers.on_commanderSearchEntry_changed = self.commander_window.on_commanderSearchEntry_changed
		self.handlers.on_commanderList_row_activated = self.commander_window.on_commanderList_row_activated
		self.handlers.on_commanderSearchEntry_key_press_event = self.commander_window.on_commanderSearchEntry_key_press_event
		self.handlers.on_commanderList_key_press_event = self.commander_window.on_commanderList_key_press_event
			

	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		# when user hit ctrl alone, or any key 
		# not ctrl + any 
		if not ctrl:
			# we assume that only ctrl is pressed
			# we know it is for sure not ctrl+'any key'
			# on_window_key_release_event verifies if
			# ctrl was released, but we need to know
			# if ctrl has been pressed and released (alone)
			self.only_ctrl = True
			
			# get time
			self.t0 = time.time()
		else:
			self.only_ctrl = False
			
			
	def on_window_key_release_event(self, window, event):
		keyval_name = Gdk.keyval_name(event.keyval)
		ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
		alt = (event.state & Gdk.ModifierType.MOD1_MASK)
		shift = (event.state & Gdk.ModifierType.SHIFT_MASK)
		
		# if only ctrl has been pressed and released, and 
		# time is not to long during the held!, then open commander
		if ctrl and self.only_ctrl and keyval_name == "Control_L":
			if (time.time() - self.t0) <= self.max_time:
				self.run()




	def cache_commands(self):
#		self.cache_thread = threading.Thread(target=self.cache_commands_thread_func)
#		self.cache_thread.daemon = True
#		self.cache_thread.start()
		self.cache_commands_thread_func()
		
	
	def cache_commands_thread_func(self):
		print("start caching")
		
		# load commands only once, for first time
		# check if commands have been loaded
		if not self.commands:
			# load commands
			self.load_commands()
		
		self.load_dynamic_commands()
		
		self.commander_window.cache_commander_window()
		
		print("done caching")
		
		
		
	
	def run(self):
		# show commander window	
		self.commander_window.show_commander_window()
	
	
	
	def load_commands(self):
		print("load_commands")
		temp_thread_safe = []
		
		#for i in range(0, 100):
		for plugin in self.plugins_manager.plugins_array:
			if plugin.commands:
				for c in plugin.commands:
					temp_thread_safe.append(c)

		self.commands = temp_thread_safe
	
	
	

	def load_dynamic_commands(self):
		# delete all items 
		temp_thread_safe = []
		
		temp_thread_safe.append({
			"plugin-name":		self.name,
			"name": 			"Switch to File < commander_window.py",
			"ref": 				self.plugins["files_manager.files_manager"].switch_to_file,
			"parameters": 		2,
			"shortcut": 		"",
			})
		self.dynamic_commands = temp_thread_safe
		
		
		
		
