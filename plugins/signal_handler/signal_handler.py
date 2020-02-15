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
#

import sys

import gi
from gi.repository import Gdk


class Handlers(object):
	pass
	

class SignalHandler:
	def __init__(self, app):
		self.app = app
		self.builder = app.builder
		self.plugins = app.plugins_manager.plugins
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
		
		# for performance reason:
		# - pass only key bindings (i.e. when ctrl, alt)
		# - or when "F" function keys pressed such F1, F2 ..
		# this if is to condition the exit
		if not ctrl and not alt:
			if len(keyval_name) != 2: # not F1, ..
				return
		
		for p in self.plugins:
			p.key_bindings(event, keyval_name, ctrl, alt, shift)


	
	def resizeBodySide(self, bodyPaned, param):
		headerPaned = self.builder.get_object("headerPaned")
		headerPaned.set_position(bodyPaned.get_position())
		
		
	def resizeHeaderSide(self, headerPaned, param):
		bodyPaned = self.builder.get_object("bodyPaned")
		bodyPaned.set_position(headerPaned.get_position())
			
