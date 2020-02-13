plugin_list = [
	"styles.style",
	"styles.source_style", 
	"window_ctrl.window_ctrl",
	"files_manager.openfile",
	"commander.commander",
	"simple_completion.simple_completion",
]


import importlib


class PluginsManager():

	def __init__(self, app):
		self.app = app
		self.plugins = []


	def load_plugins(self):
		for p in plugin_list:
			plugin = importlib.import_module('.' + p, package='plugins')
			module = plugin.Plugin(self.app)
			module.activate()
			self.plugins.append(module)
			
			
			
	def get_plugin(self, plugin_name):
		for p in plugin_list:
			print(p)
