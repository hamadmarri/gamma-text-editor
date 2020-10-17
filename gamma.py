#
#### Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Feb 11th, 2020
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
# This is the entry point to Gamma editor. The gamma.py will load
# config parameters and load the builder (UI structure of the main window).
# This Application instance is the main root of gamma. It holds
# references to everything needed for other plugins such as config, 
# window, builder, and plugins_manager.
# Also it loads the eager plugins in self.plugins_manager.load_plugins()
# which call activate for each plugin and store plugins references in
# plugins_manager.plugins

import sys
import os

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', "4")
from gi.repository import Gio, Gtk, Gdk, GtkSource, GObject

# While packaging this application, set packaged to True
# If packaged is False, it means gamma was installed using setup.sh
packaged = False
if packaged == True:
	if os.path.isfile(os.path.expanduser('~/.config/gamma-text-editor/config.py')) == False:
		# If initial config is not present then execute
		# script to copy it to user's .config directory
		install_path = os.path.dirname(os.path.realpath(__file__))
		import subprocess
		subprocess.run([install_path + "/home_dir_init.sh", install_path])
	# Allow gamma to read config/plugins from user's .config directory
	sys.path.append(os.path.expanduser('~/.config/gamma-text-editor'))

import config
import signal_handler
from plugins.plugins_manager import PluginsManager


class Application(Gtk.Application):

	def __init__(self, *args, **kwargs):
				
		# make the package name as "io.gitlab.hamadmarri.gamma"
		# FLAGS_NONE means no passing arguments from command line, this
		# might be changed later to support new window, new file, or open a file
		super().__init__(*args, application_id=f"io.gitlab.hamadmarri.gamma", 
						flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE, **kwargs)
		
		
		# this line is important to mak gtk object(newer version of pygtk) to
		# include gtk sourceview.
		GObject.type_register(GtkSource.View)
		
		self.name = "GammaApplication"
		self.window = None
		self.builder = None
		self.is_debugging = False
		
		# config contains important paths and settings for ui, styles, plugins
		self.config = config.config_paths_and_settings

		# builder is the object responsible of
		# translating .ui xml files (widgets design/layout. see glade) to
		# be in the gtk objects form 
		self.load_builder()
		
		# plugins_manager for anything related to plugins (eager plugins)
		self.plugins_manager = PluginsManager(self)
				
		# signal_handler is for handling general signals such as
		# key press, and basic window resizing paned
		# SignalHandler also makes it easier for other plugins to
		# process key bindings. It loop through all plugins and 
		# call key_bindings function passing (event, keyval_name, ctrl, alt, shift)
		# which is an easy design for plugins to set there key bindings
		self.signal_handler = signal_handler.SignalHandler(self)
		


	def load_builder(self):
		self.builder = Gtk.Builder()
		
		# load .ui file, its path is in config file
		self.builder.add_from_file(self.config["ui-path"])



	def set_handlers(self):
		# this line connects signals in handlers object to 
		# some functions. "handlers" is set by SignalHandler and
		# plugins that need to bind signals to functions
		self.builder.connect_signals(self.signal_handler.handlers)
		

	def do_startup(self):
		Gtk.Application.do_startup(self)

	
	def do_command_line(self, command_line):
		args = command_line.get_arguments()
		self.signal_handler.emit("log", self, "do_command_line:" + str(args))
		
		if len(args) == 1:
			self.do_activate()
		elif args[1] == "--new-window":
			self.do_activate(new_window=True)
		elif args[1] == "--verbose":
			self.is_debugging = True
			
			# make sure at least the main window is open
			self.do_activate()
			
			if len(args) > 2:
				# open files
				self.open_files(args[2:])
		else:
			# make sure at least the main window is open
			self.do_activate()
			
			# open files
			self.open_files(args[1:])
			
		return 0
	
			
		
	def do_activate(self, new_window=False):
	 	if not self.window:
	 		self.show_first_window()
	 	elif new_window:
	 		self.show_new_window()
		
	
	def show_first_window(self):
		# get id=window (ui element in .ui) from builder
		self.window = self.builder.get_object("window")
		
		# bind this builder to this window
		self.window.builder = self.builder
		
		# loading plugins calls their activate functions.
		# in plugins_manager.py, you can comment out plugins in
		# plugin_list array
		self.plugins_manager.load_plugins()
		self.set_handlers()
		
		# must set the parent application of 
		# window to this app(self)
		self.window.props.application = self
		self.window.set_icon_name("io.gitlab.hamadmarri.gamma")
		self.window.show_all()
		self.window.connect("focus_in_event", self.window_event)
		

	def show_new_window(self):
		self.load_builder()
		
		# get id=window (ui element in .ui) from builder
		self.window = self.builder.get_object("window")
		
		# bind this builder to this window
		self.window.builder = self.builder

		self.plugins_manager.activate_plugins()
		self.set_handlers()
				
		# must set the parent application of 
		# window to this app(self)
		self.window.props.application = self
		self.window.set_icon_name("io.gitlab.hamadmarri.gamma")
		self.window.show_all()
		self.window.connect("focus_in_event", self.window_event)
		

	
	def window_event(self, w, e=None):
		self.window = w
		self.builder = w.builder
		self.signal_handler.emit("windo-focus-in", w)



	def open_files(self, filenames):	
		self.signal_handler.emit("log", self, "do_open:" + str(filenames))
		self.plugins_manager.THE("files_manager", "open_files", {"filenames": filenames})


if __name__ == "__main__":
	app = Application()
	app.run(sys.argv)
	
