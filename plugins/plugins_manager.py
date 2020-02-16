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
#					"activate" of a plugin is called. "activate" is plugin init,
#					so do not use plugins' __init__ for complex operation. The
#					plugins' __init__ must only include direct references assignments
#					(i.e. self.builder = app.builder). Other than these assignments,
#					plugins activate must be your method for initializing you plugin.
#					The reason for this design is to know which plugin must be eager
#					and which must be lazy plugin. Simply, if your activate method 
#					is not implemented (i.e. def activate(self): pass), then the
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
	"styles.style",
	"styles.source_style", 
	"window_ctrl.window_ctrl",
	"files_manager.openfile",
	"files_manager.savefile",
	"files_manager.files_manager",
	"commander.commander",
	"simple_completion.simple_completion",
	"highlight.highlight",
	"message_notify.message_notify",
	"search.search_in_file",
]


import importlib


class PluginsManager():

	def __init__(self, app):
		self.app = app
		self.plugins = []


	# importing all plugins in "plugin_list"
	# notice that activate method is called
	# these plugins are eagerly loaded
	# the more plugins, and process in activate 
	# method, the heavier startup time
	def load_plugins(self):
		for p in plugin_list:
			# plugins are in "plugins" folder/package
			plugin = importlib.import_module('.' + p, package='plugins')
			
			# initializing plugin and passing the
			# reference of app
			module = plugin.Plugin(self.app)
			module.activate()
			
			# add a reference of the plugin 
			# to plugins array
			self.plugins.append(module)
			
			
	# loop through plugins array and
	# find plugin matching same name
	# TODO: implement dictionary for faster access
	def get_plugin(self, plugin_name):
		for p in self.plugins:
			if p.name == plugin_name:
				return p
