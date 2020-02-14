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
		
	
	def get_new_sourceview(self):
		# get source_style
		if not self.source_style:
			self.source_style = self.app.plugins_manager.get_plugin("source_style")
			
		# get simple_completion
		if not self.simple_completion:
			self.simple_completion = self.app.plugins_manager.get_plugin("simple_completion")
			
		newsource = GtkSource.View.new()
		
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
				    
		self.source_style.set_source_style(newsource.get_buffer())
		newsource.get_style_context().add_class("sourceviewclass")
		
		newsource.show()
		
		
		self.simple_completion.update_completion(newsource)
		
		return newsource
		
		
	def set_language(self, filename, buffer):
		lm = GtkSource.LanguageManager.get_default()
		lan = lm.guess_language(filename)
		if lan:
			buffer.set_highlight_syntax(True)
			buffer.set_language(lan)
		else:
			print('No language found for file "cen"')
			buffer.set_highlight_syntax(False)
			
	def update_sourcemap(self, source_view):
		self.sourcemap.set_view(source_view)

