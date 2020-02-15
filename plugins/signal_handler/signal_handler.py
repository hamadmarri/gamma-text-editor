#
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
# SignalHandler: is the class that manage signal handlers.
# "Handlers" is an object for mapping signal names with 
# callback methods references. "set_handlers" method is the convention
# way when need to map ui signals to callback functions. It is
# good to have the same method name in your plugin when need
# connect ui signals to your plugin's methods
#
#

import sys

import gi
from gi.repository import Gdk


# "Handlers" is an object for mapping signal names with 
# callback methods references. You can mapp ui signals by
# simply handlers.on_some_ui_event = some_callback_method
class Handlers(object):
	pass
	

class SignalHandler:
	def __init__(self, app):
		self.app = app
		self.builder = app.builder
		self.plugins = app.plugins_manager.plugins
		self.handlers = Handlers()
		self.set_handlers()
		
	
	# SignalHandler sets the main signals such as key press 
	def set_handlers(self):
		self.handlers.on_window_key_press_event = self.on_window_key_press_event
		self.handlers.resizeBodySide = self.resizeBodySide
		self.handlers.resizeHeaderSide = self.resizeHeaderSide

		
	
	# you should not map "on_window_key_press_event" to your plugin.
	# this function will help you by getting the keyval_name("e", "space", ..)
	# and other modifiers like ctrl, alt, and shift 
	# you plugin must have the "key_bindings" method. If your
	# plugin does not need key bindings, then just "pass"
	# if yes, then simply just check what key binding you need such as
	# if alt and ctrl and keyval_name == "m":
	# 	...
	# the above "if" is checking whether alt and ctrl are hold when
	# pressed the "m" key (i.e. <Ctrl><Alt>+m)
	def on_window_key_press_event(self, window, event):
		keyval_name = Gdk.keyval_name(event.keyval)
		ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
		alt = (event.state & Gdk.ModifierType.MOD1_MASK)
		shift = (event.state & Gdk.ModifierType.SHIFT_MASK)
		
		# for performance reason:
		# - pass only key bindings (i.e. when ctrl, alt)
		# - or when "F" function keys pressed such F1, F2 ..
		# this if is to condition the exit
		if not ctrl and not alt:
			if len(keyval_name) != 2: # not F1, ..
				return
		
		# loop through all plugins and call their key_bindings method
		for p in self.plugins:
			p.key_bindings(event, keyval_name, ctrl, alt, shift)


	
	# when resize the left panel of the files, need
	# to resize the header too "Files"
	def resizeBodySide(self, bodyPaned, param):
		headerPaned = self.builder.get_object("headerPaned")
		headerPaned.set_position(bodyPaned.get_position())
		
	# when resize the "Files" header, need
	# to resize left panel of the files too 
	def resizeHeaderSide(self, headerPaned, param):
		bodyPaned = self.builder.get_object("bodyPaned")
		bodyPaned.set_position(headerPaned.get_position())
			
