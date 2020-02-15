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
# #
# SourceViewManager is responsible for sourceview related functions
# - get new source view
# - detect the language of the just openned file and set the langauge (i.e. C,Python,C++ ..)
# - update source map (mini map) to connect to a sourceview
#

import gi
gi.require_version('GtkSource', '4')
from gi.repository import GtkSource

class SourceViewManager():
	def __init__(self, app):
		self.app = app
		self.source_view = self.app.builder.get_object("view")
		self.sourcemap = self.app.builder.get_object("sourcemap")
		self.sourcemap.set_view(self.source_view)
		self.source_style = None
		self.simple_completion = None
		self.highlight = None
		
	
	
	def get_plugins_refs(self):
		# get source_style
		if not self.source_style:
			self.source_style = self.app.plugins_manager.get_plugin("source_style")
			
		# get simple_completion
		if not self.simple_completion:
			self.simple_completion = self.app.plugins_manager.get_plugin("simple_completion")
			
		# get highlight
		if not self.highlight:
			self.highlight = self.app.plugins_manager.get_plugin("highlight")
			
	
	
	# opening new file needs new sourceview object
	#  here where the new sourceview object is created
	# - it copies the default sourceview properties
	# - sets the source style
	# - connects signal mark-set event which is when user select text
	# - updates the world completion to include new source buffer
	def get_new_sourceview(self):
		self.get_plugins_refs()
			
		# get new sourceview object
		newsource = GtkSource.View.new()
		
		# copy the default sourceview properties
		newsource.set_visible(self.source_view.get_visible())
		newsource.set_can_focus(self.source_view.get_can_focus())
		newsource.set_pixels_above_lines(self.source_view.get_pixels_above_lines())
		newsource.set_pixels_below_lines(self.source_view.get_pixels_below_lines())
		newsource.set_left_margin(self.source_view.get_left_margin())
		newsource.set_right_margin(self.source_view.get_right_margin())
		newsource.set_bottom_margin(self.source_view.get_bottom_margin())
		newsource.set_top_margin(self.source_view.get_top_margin())
		newsource.set_monospace(self.source_view.get_monospace())
		newsource.set_show_line_numbers(self.source_view.get_show_line_numbers())
		newsource.set_show_line_marks(self.source_view.get_show_line_marks())
		newsource.set_tab_width(self.source_view.get_tab_width())
		newsource.set_auto_indent(self.source_view.get_auto_indent())
		newsource.set_highlight_current_line(self.source_view.get_highlight_current_line())
		newsource.set_background_pattern(self.source_view.get_background_pattern())
		newsource.set_smart_home_end(self.source_view.get_smart_home_end())

		# set the source style
		self.source_style.set_source_style(newsource.get_buffer())
		
		# add "sourceviewclass" css class
		newsource.get_style_context().add_class("sourceviewclass")
		
		# connect signal mark-set event which is when user select text
		# user clicks to unselect text is also connected
		# see highlight.highlight_signal function for handling 
		# mark-set event
		newsource.get_buffer().connect("mark-set", self.highlight.highlight_signal)
		
		# show the gtk widget
		newsource.show()
		
		# update the world completion to include new source buffer
		self.simple_completion.update_completion(newsource)
		
		return newsource
		
	
	# detect the language of the just openned file 
	# and set the langauge (i.e. C,Python,C++ ..)
	def set_language(self, filename, buffer):
		lm = GtkSource.LanguageManager.get_default()
		
		# guess the language of the filename
		lan = lm.guess_language(filename)
		if lan:
			# set the highlight of buffer
			buffer.set_highlight_syntax(True)
			buffer.set_language(lan)
		else:
			print('No language found for file "cen"')
			buffer.set_highlight_syntax(False)
			
			
	# update source map (mini map) to connect to a sourceview
	def update_sourcemap(self, source_view):
		self.sourcemap.set_view(source_view)

