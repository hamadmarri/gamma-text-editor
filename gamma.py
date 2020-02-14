import sys

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')
from gi.repository import GLib, Gio, Gtk, Gdk, GtkSource, GObject

import config
import sourceview_manager
from plugins.plugins_manager import PluginsManager
from plugins.signal_handler.signal_handler import SignalHandler

class Application(Gtk.Application):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, application_id="com.editor.gamma", flags=Gio.ApplicationFlags.FLAGS_NONE, **kwargs)
		GObject.type_register(GtkSource.View)
		self.window = None
		self.config = config.config_paths_and_settings
		
		self.load_builder()
		self.sourceview_manager = sourceview_manager.SourceViewManager(self)
		self.plugins_manager = PluginsManager(self)
		self.handler = SignalHandler(self)
		

	def load_builder(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file(self.config["ui-path"])



	def set_handlers(self):	
		self.builder.connect_signals(self.handler.handlers)
		

	def do_startup(self):
		Gtk.Application.do_startup(self)

	def do_activate(self):
		if not self.window:
			self.window = self.builder.get_object("window")
			self.window.props.application = self
		
		
		self.plugins_manager.load_plugins()
		self.set_handlers()
		self.window.show_all()



if __name__ == "__main__":
	app = Application()
	app.run()
