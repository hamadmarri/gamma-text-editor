#
#### Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Mar 4th, 2020
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
#

import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from . import commands

class Plugin():
	
	def __init__(self, app):
		self.name = "logger"
		self.app = app
		self.builder = app.builder
		self.signal_handler = app.signal_handler
		self.THE = app.plugins_manager.THE
		self.set_handlers()
		self.commands = []
		self.signal_handler.connect("log", self.log)
		self.signal_handler.connect("log-warning", self.log_warning)
		self.signal_handler.connect("log-error", self.log_error)
		self.signal_handler.connect("append-to-log", self.append_to_log)
		self.log_array = []
		self.log_scrolled = None
		self.need_reload = True

	
	

	def activate(self):
		self.signal_handler.key_bindings_to_plugins.append(self)
		commands.set_commands(self)
		
	
	
	def set_handlers(self):
		self.signals = {
			"on_log_window_destroy": self.on_log_window_destroy,
		}
		


	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if shift and ctrl and keyval_name == "L":
			self.show_log()
	
	
	def on_log_window_destroy(self, w):
		self.need_reload = True
	
	
	def show_log(self, log_type=0):
		text = ""
		print("\nlog:")
		
		if log_type == 0:
			for l in self.log_array:
				text += l + '\n'
		elif log_type == 1:
			for l in self.log_array:
				if l.find("WARNING:") == 0:
					text += l + '\n'
		elif log_type == 2:
			for l in self.log_array:
				if l.find("ERROR:") == 0:
					text += l + '\n'
		
		print(text)
		
		self.load_from_builder()
		self.textview.get_buffer().set_text(text)
		self.show_log_in_bottom_panel()

		
		
	def load_from_builder(self):
		if not self.need_reload:
			return
				
		dir_path = os.path.dirname(os.path.realpath(__file__))
		builder = Gtk.Builder()
		builder.add_from_file(f"{dir_path}/logger.glade")
		builder.connect_signals(self.signals)
		
		self.window = builder.get_object("log_window")
		self.log_scrolled = builder.get_object("log_scrolled_window")
		self.textview = builder.get_object("log_textview")
		
		style_provider = Gtk.CssProvider()
		style_provider.load_from_path(f"{dir_path}/logger.css")
		self.log_scrolled.get_style_context().add_provider(
			style_provider,
			Gtk.STYLE_PROVIDER_PRIORITY_USER
		)
		
		self.textview.get_style_context().add_provider(
			style_provider,
			Gtk.STYLE_PROVIDER_PRIORITY_USER
		)
		
		
	
	
	def show_log_window(self):
		self.window.set_transient_for(self.app.window)
		
		if not self.window.get_visible():
			self.need_reload = False
			self.window.show_all()
		
		
	def show_log_in_bottom_panel(self):
		if self.window.get_child():
			self.window.remove(self.log_scrolled)
			
		self.log_scrolled.show_all()
		args = {
			"plugin": self,
			"label": "Log",
			"widget": self.log_scrolled
		}
		
		added = self.THE("bottom_panel", "add", args)
		
		if not added:
			self.window.add(self.log_scrolled)
			self.show_log_window()
				
		
	
	def log(self, message):
		print(message)
		self.log_array.append(message)
		self.signal_handler.emit("append-to-log", message)
		
		
		
	def log_warning(self, message):
		message = f'WARNING: {message}' 
		print(message)
		self.log_array.append(message)
		self.signal_handler.emit("append-to-log", message)
		
		
	def log_error(self, message):
		message = f'ERROR: {message}' 
		print(message)
		self.log_array.append(message)
		self.signal_handler.emit("append-to-log", message)
		
		self.THE("message_notifier", "show_message", {"m": message, "state": 3})
		
		
	
	def append_to_log(self, text):
		if self.log_scrolled:
			buffer = self.textview.get_buffer()
			text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False) \
						 + text + '\n' 
			self.textview.get_buffer().set_text(text)
		

		
		
