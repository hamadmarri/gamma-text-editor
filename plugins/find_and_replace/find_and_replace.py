#
#### Author: first lastname <email>
#### Date: MMM ddth, yyyy
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


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from . import commands
from .find_and_replace_window import FindReplaceWindow


class Plugin(FindReplaceWindow):
	
	def __init__(self, app):
		self.name = "find_and_replace"
		self.app = app
		self.window = None
		self.sourceview = None
		self.buffer = None
		self.signal_handler = app.signal_handler
		self.handlers = app.signal_handler.handlers
		self.plugins = app.plugins_manager.plugins
		self.commands = []
		self.show_replace = False
		self.find_text_view = None
		self.replace_text_view = None
		self.new_search = True
		self.match_case = True
		self.whole_word = False
		
	
 
	def activate(self):
		self.signal_handler.key_bindings_to_plugins.append(self)
		commands.set_commands(self)
		self.set_handlers()


	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if ctrl and keyval_name == "h":
			self.show_window(show_replace=False)


	def clear_highlights(self):
		# to clear highlights
		self.plugins["search.search_in_file"].do_highlight("", self.buffer)
		self.plugins["search.search_in_file"].quit_search()
		
	
	def do_find(self, previous=False):
		search = self.plugins["search.search_in_file"]
		if self.new_search:
			if self.match_case:
				search.search_flags = 0
			else:
				search.search_flags = Gtk.TextSearchFlags.CASE_INSENSITIVE
			
			search.whole_word = self.whole_word
			
			self.new_search = False
			buffer = self.find_text_view.get_buffer()
			text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)

			search.refresh_sources()
			search.do_highlight(text, self.buffer)
		elif not previous:
			search.scroll_next()
		else:
			search.scroll_prev()
		



	def do_replace(self):
		if self.new_search:
			self.do_find()
			return
		
		search = self.plugins["search.search_in_file"]
		
		# if no current selection (end of replace)
		if not search.current_selection:
			return
		
		# get replace text 
		replace_buffer = self.replace_text_view.get_buffer()
		text = replace_buffer.get_text(replace_buffer.get_start_iter(), replace_buffer.get_end_iter(), False)
		
		# get current selected 
		(s_iter, e_iter) = search.current_selection
	  
		self.replace_in_buffer(self.buffer, s_iter, e_iter, text)
		
		search.delete_current_marks()
		# reset iters after buffer manipulation
		search.set_selected_iters(None, None)
		
		self.do_find()
		
		
		
		
	def replace_in_buffer(self, buffer, s_iter, e_iter, text):
		pos_mark = buffer.create_mark("find-replace", e_iter, True)
		# pos_mark.set_visible(True)
		buffer.delete(s_iter, e_iter)
		replace_iter = buffer.get_iter_at_mark(pos_mark)
		buffer.insert(replace_iter, text)
		
		
		
	def do_replace_all(self):
		if self.new_search:
			self.do_find()
			return
	
		highlight = self.plugins["highlight.highlight"]
		search = self.plugins["search.search_in_file"]
		marks = highlight.marks
		
		# if no current selection (end of replace)
		if not search.current_selection:
			return
			
		# get replace text 
		replace_buffer = self.replace_text_view.get_buffer()
		text = replace_buffer.get_text(replace_buffer.get_start_iter(), replace_buffer.get_end_iter(), False)
		
		
		i = len(marks) - 1
		while marks:
			s_mark = marks[i - 1]
			e_mark = marks[i]
			s_iter = self.buffer.get_iter_at_mark(s_mark)
			e_iter = self.buffer.get_iter_at_mark(e_mark)
			
			self.replace_in_buffer(self.buffer, s_iter, e_iter, text)
			
			self.buffer.delete_mark(s_mark)
			self.buffer.delete_mark(e_mark)
			
			del marks[i]
			del marks[i - 1]
			i -= 2
		# end while
			
		# reset iters after buffer manipulation
		search.set_selected_iters(None, None)
		
		
		
