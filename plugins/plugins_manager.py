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
# PluginsManager:	is responsible for initating plugins.
#
# - load_plugins:	by using "importlib" the plugins loaded and included
# 					to Gamma. It goes through "plugin_list" to get exact name
#					of the plugin package. For each plugin, plugin module is
#					included, the app reference is passed to plugin, and the
#					"activate" method of a plugin is called. "activate" is plugin init,
#					so do not use plugins' __init__ for complex operation. The
#					plugins' __init__ must only include direct references assignments
#					(i.e. self.builder = app.builder). Other than these assignments,
#					plugins activate must be your method for initializing you plugin.
#					The reason for this design is to know which plugin must be eager
#					and which must be lazy plugin. Simply, if your activate method
#					is not implemented (i.e. def activate(self): pass), then the plugin
#					is lazy plugin.
#
# - get_plugin:		Used from plugins which need to get reference of other plugins.
#					It is expensive process "O(n)", so better use it once and cache
#					the reference.
#


# list of active plugins
# deactivate plugin by removing or commenting out the plugin name
# formate "[folder name].[python file]"
plugin_list = [
	{"name": "sourceview_manager.sourceview_manager","category": "sourceview_manager"},
	{"name": "styles.style","category": ""},
	{"name": "styles.source_style", "category": "source_styler"},
	{"name": "window_ctrl.window_ctrl", "category": "window_controller"},
	{"name": "files_manager.files_manager", "category": "files_manager"},
	{"name": "files_manager.openfile", "category": "files_opener"},
	{"name": "files_manager.savefile", "category": "files_saver"},
	{"name": "files_manager.opendir", "category": "directory_opener"},
	{"name": "simple_completion.simple_completion", "category": "code_completer"},
	{"name": "highlight.highlight", "category": "highlighter"},
	{"name": "message_notify.message_notify", "category": "message_notifier"},
	{"name": "search.search_in_file", "category": "file_searcher"},
	{"name": "ui_manager.ui_manager", "category": "ui_manager"},
	{"name": "codecomment.codecomment", "category": "codecommenter"},
	{"name": "find_and_replace.find_and_replace", "category": "find_and_replace"},
	{"name": "terminal.terminal", "category": "terminal"},

	{"name": "bottom_panel.bottom_panel", "category": "bottom_panel"},
	{"name": "welcome.welcome", "category": "welcomer"},
	{"name": "help.help", "category": "helper"},
	{"name": "about.about", "category": "about"},
	{"name": "fast_copy_cut_duplicate.fast_copy_cut_duplicate", "category": ""},
	{"name": "typing_assistant.typing_assistant", "category": ""},
	{"name": "logger.logger", "category": "logger"},
	{"name": "toggle_files_list.toggle_files_list", "category": "files_toggler"},
	{"name": "key_scroller.key_scroller", "category": ""},
	{"name": "output.output", "category": "output"},
	{"name": "remember_recent_files.remember_recent_files", "category": "recent_files_rememberer"},


	# special case for commander
	# must be last because the activate method
	# of commands need to cache other plugins commands
	{"name": "commander.commander", "category": "commander"},
]


import importlib

class PluginsManager():

	def __init__(self, app):
		self.name = "plugins_manager"
		self.app = app
		self.plugins_array = []
		self.categories = {}


	# importing all plugins in "plugin_list"
	# notice that activate method is called
	# these plugins are eagerly loaded
	# the more plugins, and process in activate
	# method, the heavier startup time
	def load_plugins(self):
		for p in plugin_list:
			# plugins are in "plugins" folder/package
			plugin = importlib.import_module('.' + p["name"], package='plugins')

			# initializing plugin and passing the
			# reference of app
			module = plugin.Plugin(self.app)

			# add a reference of the plugin
			# to plugins categories and array
			if p["category"]:
				self.categories[p["category"]] = module

			self.plugins_array.append(module)


		# activate plugins
		for p in self.plugins_array:
			p.activate()

		self.app.signal_handler.emit("log", self, f"loaded {len(self.plugins_array)} plugins")

		# emitting startup where any plugin could connect to
		# startup signal. It is save to reach other plugins
		# from startup signals since all have been activated
		self.app.signal_handler.emit("startup")



	def activate_plugins(self):
		# activate plugins
		for p in self.plugins_array:
			p.activate()




	# get plugin from categories dictionary that match same name
	# if existed, find the method, if existed, do the call
	def THE(self, plugin_category, method, args):
		# DEBUG: print(plugin_category, method, args)

		p = self.categories.get(plugin_category)
		if p:
			if hasattr(p, method):
				callable_method = getattr(p, method)
				# DEBUG: print(callable_method)
				# DEBUG: print(args)
				if args != None:
					# DEBUG: print("args")
					return callable_method(**args)
				else:
					# DEBUG: print("property")
					return callable_method
			else:
				self.app.signal_handler.emit("log-warning", self, f'THE: ({plugin_category}): No method/property: {method}')
				return None
		else:
			self.app.signal_handler.emit("log-warning", self, f'THE: No plugin/category: {plugin_category}')
			return None


