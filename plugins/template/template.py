#
#### Author: first lastname <email>
#### Date: MMM ddth, yyyy
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
# template: is not used plugin, but it is an example or template for you to 
#			start your plugin. It is good starting point to your plugin.
#			Copy this file, rename it, change self.name to your plugin name.
#			If the plugin needs to export its commands to commander, copy
#			commands.py too. If not, delete lines:
#									from . import commands
#									commands.set_commands(self)
# 			
#			Currently, activate and key_bindings methods must be implemented.
#			If no implemention needed for activate and key_bindings then keep
#			the "pass"
#
#			The usual imports are:
#			import gi
#			gi.require_version('Gtk', '3.0')
#			gi.require_version('GtkSource', '4')
#			from gi.repository import GLib, Gio, Gtk, Gdk, GtkSource, GObject
#			
#			But your plugin may not need all of these modules
#
#

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from . import commands

# class name must be "Plugin". Do not change the name 
class Plugin():
	
	# the plugins_manager will pass "app" reference 
	# to your plugin. "app" object is defined in gamma.py
	# from "app" reference you can access pretty much 
	# everything related to Gamma (i.e. window, builder, 
	# sourceview, and other plugins)
	def __init__(self, app):
		self.name = "template"
		self.app = app
		self.commands = []
		commands.set_commands(self)
	
	# do not remove 
	def activate(self):
		pass
	
	# do not remove 
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		# you should not map "on_window_key_press_event" to your plugin.
		# this function will help you by getting the keyval_name("e", "space", ..)
		# and other modifiers like ctrl, alt, and shift 
		# your plugin must have the "key_bindings" method. If your
		# plugin does not need key bindings, then just "pass"
		# if yes, then simply just check what key binding you need such as
		# if alt and ctrl and keyval_name == "m":
		# 	...
		# the above "if" is checking whether alt and ctrl are hold when
		# pressed the "m" key (i.e. <Ctrl><Alt>+m)
		# see SignalHandler
		pass
	
	# optional	
	def method1(self):
		pass
		
	# optional
	def method2(self):
		pass
	
	# optional
	def method3(self):
		pass
