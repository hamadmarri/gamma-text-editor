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

from datetime import datetime

from . import commands
from .colors_mixin import ColorsMixin
from .log_entry import LogEntry
from .logger_gui import LoggerGUI

class Plugin(ColorsMixin, LoggerGUI):
	
	def __init__(self, app):
		self.name = "logger"
		self.app = app
		self.signal_handler = app.signal_handler
		self.THE = app.plugins_manager.THE
		self.commands = []
		self.signal_handler.connect("log", self.log)
		self.signal_handler.connect("log-warning", self.log_warning)
		self.signal_handler.connect("log-error", self.log_error)
		
		if app.is_debugging:
			self.signal_handler.connect("debug", self.log_debug)
		
		self.window = None
		self.log_array = []
		self.warning_color = None
		self.error_color = None

		self.signal_handler.key_bindings_to_plugins.append(self)
		commands.set_commands(self)
		
	

	def activate(self):
		self.app.window.logger_log_body = None
		self.app.window.logger_need_reload = True
		self.app.window.logger_log_type = 0
		self.app.window.logger_original_results = ""
		self.set_handlers()
	
	
	def set_handlers(self):
		self.signals = {
			"on_log_window_destroy": self.on_log_window_destroy,
			"on_log_search_search_changed": self.on_log_search_search_changed,
		}
		


	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if shift and ctrl and keyval_name == "L":
			self.show_log()
	
	
	
	def show_log(self, log_type=0):
		self.app.window.logger_log_type = log_type
	
		text = ""
		print("\nlog:")
		
		if log_type == 0:
			for l in self.log_array:
				text += str(l) + '\n'
		elif log_type == 1:
			for l in self.log_array:
				if l.level == "WARNING":
					text += str(l) + '\n'
		elif log_type == 2:
			for l in self.log_array:
				if l.level == "ERROR":
					text += str(l) + '\n'
		
		print(self.colorize_terminal(text))
		
		self.show_log_gui(text)


		
	def log(self, plugin, message):
		_time = datetime.now().strftime('%c').strip()
		_level = "INFO"
		message = LogEntry(f'<{_time}> <{plugin.name}> <{_level}>: {message.strip()}', _level)
		print(message)
		self.log_array.append(message)
		self.append_to_log(message)
	
	
	def log_debug(self, plugin, message):
		_time = datetime.now().strftime('%c').strip()
		_level = "DEBUG"
		message = LogEntry(f'<{_time}> <{plugin.name}> <{_level}>: {message.strip()}', _level)
		print(message)
		self.log_array.append(message)
		self.append_to_log(message)
		
		
	def log_warning(self, plugin, message):
		_time = datetime.now().strftime('%c').strip()
		_level = "WARNING"
		message = LogEntry(f'<{_time}> <{plugin.name}> <{_level}>: {message.strip()}', _level)
		print(self.colorize_terminal(message))
		self.log_array.append(message)
		self.append_to_log(message)
		
		
	def log_error(self, plugin, message):
		_time = datetime.now().strftime('%c').strip()
		_level = "ERROR"
		message = LogEntry(f'<{_time}> <{plugin.name}> <{_level}>: {message.strip()}', _level)
		print(self.colorize_terminal(message))
		self.log_array.append(message)
		self.append_to_log(message)
		self.THE("message_notifier", "show_message", {"m": str(message), "state": 3})
		
		
					
		
