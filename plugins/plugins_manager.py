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
		for p in self.plugins:
			if p.name == plugin_name:
				return p
