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

			print("new search")
			search.refresh_sources()
			search.do_highlight(text, self.buffer)
		elif not previous:
			search.scroll_next()
		else:
			search.scroll_prev()
		




	# TODO: remove 
		# buffer = self.sourceview.get_buffer()
		# # after_end_iter = match_end.copy()
		# # after_end_iter.forward_char()
		# pos_mark = buffer.create_mark("find-replace", match_end, True)
		# # pos_mark.set_visible(True)
		# buffer.delete(match_start, match_end)
		# p = buffer.get_iter_at_mark(pos_mark)
		# buffer.insert(p, "~!@~!@~!@")
		# match_end = buffer.get_iter_at_mark(pos_mark)
		
		
		