#
#### Author: Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Feb 25th, 2020
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
#	Find and replace text with some options such as case sensitive/insensitive,
#	whole word, and replace one or replace all.
#
#


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from . import commands
from .find_and_replace_window import FindReplaceWindow
from .debug import Debug


class Plugin(Debug, FindReplaceWindow):
	
	def __init__(self, app):
		self.name = "find_and_replace"
		self.app = app
		self.window = None
		self.signal_handler = app.signal_handler
		self.handlers = app.signal_handler.handlers
		self.THE = app.plugins_manager.THE
		self.commands = []
		self.show_replace = False
		self.find_text_view = None
		self.replace_text_view = None
		self.find_status_lbl = None
		self.new_search = True
		self.match_case = True
		self.whole_word = False
		self.signal_handler.connect("file-switched", self.update_buffer)
		self.signal_handler.connect("windo-focus-in", self.window_focus_in)
		self.signal_handler.key_bindings_to_plugins.append(self)
		
		commands.set_commands(self)
		self.set_handlers()
	
 
	def activate(self):
		pass


	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if shift and ctrl and keyval_name == "F":
			self.show_window(show_replace=False)
		elif ctrl and keyval_name == "h":
			self.show_window(show_replace=True)


	def update_buffer(self, new_source):
		self.app.window.find_buffer = new_source.get_buffer()
		self.app.window.find_buffer.connect("changed", self.set_new_search)
		self.new_search = True
		
		
	def window_focus_in(self, w):
		self.new_search = True
		
	
	def set_new_search(self, buffer):
		self.new_search = True
		
	
	def clear_highlights(self):
		# to clear highlights
		self.THE("file_searcher", "do_highlight", {"search": "", "buffer": self.app.window.find_buffer})
		self.THE("file_searcher", "quit_search" , {})
		
	
	def do_find(self, previous=False):		
		self.debug_do_find(previous)
		
		if self.new_search:
			if self.match_case:
				self.THE("file_searcher", "set_search_flags", {"search_flags": 0})
			else:
				self.THE("file_searcher", "set_search_flags", {"search_flags": Gtk.TextSearchFlags.CASE_INSENSITIVE})
			
			self.THE("file_searcher", "set_whole_word", {"whole_word": self.whole_word})
			
			self.new_search = False
			buffer = self.find_text_view.get_buffer()
			text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)

			self.THE("file_searcher", "do_highlight", {"search": text, "buffer": self.app.window.find_buffer})
		elif not previous:
			self.THE("file_searcher", "scroll_next", {})
		else:
			self.THE("file_searcher", "scroll_prev", {})
		
		self.update_status()
	
	
	
	def update_status(self):
		count = self.THE("file_searcher", "count", None)
		match_number = self.THE("file_searcher", "match_number", None)
		deleted_marks = self.THE("file_searcher", "deleted_marks", None)
		
		if count == None or match_number == None or deleted_marks == None:
			return
			
		if count > 0:
			self.find_status_lbl.set_text( \
				str(match_number + deleted_marks + 1) \
				+ "/" + str(count))
		else:
			self.find_status_lbl.set_text("No results")
		



	def do_replace(self):
		if self.new_search:
			self.do_find()
			return
				
		# if no current selection (end of replace)
		if not self.THE("file_searcher", "current_selection", None):
			return
		
		# get replace text 
		replace_buffer = self.replace_text_view.get_buffer()
		text = replace_buffer.get_text(replace_buffer.get_start_iter(), replace_buffer.get_end_iter(), False)
		
		# get current selected 
		(s_iter, e_iter) = self.THE("file_searcher", "current_selection", None)
	  
		self.replace_in_buffer(self.app.window.find_buffer, s_iter, e_iter, text)
		
		self.THE("file_searcher", "delete_current_marks", {})
		
		# reset iters after buffer manipulation
		self.THE("file_searcher", "set_selected_iters", {"s_iter": None, "e_iter": None})
		
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
	
		marks = self.THE("highlighter", "marks", None)
		
		# if no current selection (end of replace)
		if not self.THE("file_searcher", "current_selection", None):
			return
			
		# get replace text 
		replace_buffer = self.replace_text_view.get_buffer()
		text = replace_buffer.get_text(replace_buffer.get_start_iter(), replace_buffer.get_end_iter(), False)
		
		
		i = len(marks) - 1
		while marks:
			s_mark = marks[i - 1]
			e_mark = marks[i]
			s_iter = self.app.window.find_buffer.get_iter_at_mark(s_mark)
			e_iter = self.app.window.find_buffer.get_iter_at_mark(e_mark)
			
			self.replace_in_buffer(self.app.window.find_buffer, s_iter, e_iter, text)
			
			self.app.window.find_buffer.delete_mark(s_mark)
			self.app.window.find_buffer.delete_mark(e_mark)
			
			del marks[i]
			del marks[i - 1]
			i -= 2
		# end while
			
		# reset iters after buffer manipulation
		self.THE("file_searcher", "set_selected_iters", {"s_iter": None, "e_iter": None})
		
		self.find_status_lbl.set_text("Done")
		
		
		
