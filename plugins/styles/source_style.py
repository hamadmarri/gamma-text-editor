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
#	source_style: sets the style for the sourceview (text editting area)
#	"style_scheme" is set in config.py
#	style scheme for srource view style, usually sourceview style xml files are in 
#	~/.local/share/gtksourceview-4/styles (see config.py)
#	

import gi
gi.require_version('GtkSource', '4')
from gi.repository import GtkSource


class Plugin():
	
	def __init__(self, app):
		self.name = "source_style"
		self.app = app
		self.commands = []
	
	
	def activate(self):
		# the style is applied on the buffer
		source_view = self.app.sourceview_manager.source_view
		buffer = source_view.get_buffer()
		self.set_source_style(buffer)
		
		
	def set_source_style(self, buffer):
		manager = GtkSource.StyleSchemeManager.get_default()
		style = manager.get_scheme(self.app.config["style-scheme"])
		
		# the style is applied on the buffer
		buffer.set_style_scheme(style)
		