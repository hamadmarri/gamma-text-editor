#
#### Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Feb 16th, 2020
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
#     TODO: when Escape search keep cursor at last found
#

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from . import commands

class Plugin(): 
	
	def __init__(self, app):
		self.name = "search_in_file"
		self.app = app
		self.signal_handler = app.signal_handler
		self.handlers = app.signal_handler.handlers
		self.builder = app.builder
		self.plugins = app.plugins_manager.plugins
		self.sourceview = None
		self.buffer = None
		self.commands = []
		self.searchEntry = None
		self.search = None
		self.first_match = None
		self.next_match = None
		self.is_highlight_done = False
		self.count = 0
		self.match_number = 0
		
		# for highlight current match
		self.props = {
			"weight": 1700,
		}
		self.tag = None
		self.tag_name = "selected_search"
		
		
	
	def activate(self):
		self.signal_handler.key_bindings_to_plugins.append(self)
		self.set_handlers()
		commands.set_commands(self)
		self.searchEntry = self.builder.get_object("searchEntry")
	

	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if ctrl and keyval_name == "f":
			self.get_focus()
			
	
	# setting handlers, see SignalHandler
	def set_handlers(self):
		self.handlers.on_search_field_changed = self.on_search_field_changed
		self.handlers.on_search_key_press_event = self.on_search_key_press_event
		self.handlers.on_search_focus_out_event = self.on_search_focus_out_event
		
		
	
	def on_search_key_press_event(self, widget, event):
		keyval_name = Gdk.keyval_name(event.keyval)
		shift = (event.state & Gdk.ModifierType.SHIFT_MASK)
				
		if keyval_name == "Escape":
			self.clear_search(widget)
			
			# set focus back to sourceview
			self.plugins["files_manager.files_manager"].current_file.source_view.grab_focus()
			
		elif (shift and keyval_name == "Return") or keyval_name == "Up":
			if not self.is_highlight_done:
				self.do_highlight(self.searchEntry.get_text())
			self.scroll_prev()	
			
		elif keyval_name == "Return" or keyval_name == "KP_Enter" or keyval_name == "Down":
			if not self.is_highlight_done:
				self.do_highlight(self.searchEntry.get_text())
			else:
				self.scroll_next()
				
		
	
	def on_search_focus_out_event(self, widget, data):
		self.quit_search()
		
			
	def quit_search(self):
		self.is_highlight_done = False
		self.plugins["highlight.highlight"].remove_highlight(self.tag_name)
		self.update_style(-1)
	
	
	def get_focus(self):	
		self.sourceview = self.plugins["files_manager.files_manager"].current_file.source_view
		self.buffer = self.sourceview.get_buffer()
		
		# gets (start, end) iterators of 
		# the selected text
		iters = self.buffer.get_selection_bounds()
		if iters:
			# when user selected some text
			# get the start and end iters
			(iter_start, iter_end) = iters
			
			# get the text is being selected, False means without tags
			# i.e. only appearing text without hidden tags set by sourceview
			# (read: https://developer.gnome.org/gtk3/stable/GtkTextBuffer.html#gtk-text-buffer-get-text)
			text = self.buffer.get_text(iter_start, iter_end, False)
			
			self.searchEntry.set_text(text)

		# set cursor to searchEntry
		self.searchEntry.grab_focus()
		self.update_style(0)
				
	
	
	
	def update_style(self, state):
		self.searchEntry.get_style_context().remove_class("searching")
		self.searchEntry.get_style_context().remove_class("searchSuccess")
		self.searchEntry.get_style_context().remove_class("searchFail")
		
		if state == 0:
			# searching in blue
			self.searchEntry.get_style_context().add_class("searching")
		elif state == 1:
			# search success in green
			self.searchEntry.get_style_context().add_class("searchSuccess")
		elif state == 2:
			# no results in red 
			self.searchEntry.get_style_context().add_class("searchFail")
			
			
	
	# (see https://developer.gnome.org/gtk3/stable/GtkSearchEntry.html)
	# (https://developer.gnome.org/gtk3/stable/GtkEntry.html)
	def on_search_field_changed(self, widget):
		self.do_highlight(widget.get_text())
		
	
	# (see https://developer.gnome.org/gtk3/stable/GtkSearchEntry.html)
	# (https://developer.gnome.org/gtk3/stable/GtkEntry.html)
	def do_highlight(self, search):
		self.plugins["highlight.highlight"].remove_highlight(self.tag_name)
		self.search = search
		self.count = self.plugins["highlight.highlight"].highlight(self.search)
		
		# if no results while search is not empty
		if self.count == 0 and self.search:
			self.plugins["message_notify.message_notify"].show_message("Search Results | 0")
			self.update_style(2)
			return
			
		if not self.search:
			self.update_style(0)
		else:
			self.update_style(1)
			
		self.is_highlight_done = True
		
		# scroll to first occurrence of search if not empty
		if self.search:
			self.scroll()
		
		
	# gets start,end iters or None if no match
	# first search start from the beggining of the buffer
	# i.e. start_iter
	def scroll(self):
		self.sourceview = self.plugins["files_manager.files_manager"].current_file.source_view
		self.buffer = self.sourceview.get_buffer()
		start_iter = self.buffer.get_start_iter()
		
		# TODO: start scroll after cursor location
		#mark = self.buffer.get_insert()
		#start_iter = self.buffer.get_iter_at_mark(mark)
		matches = start_iter.forward_search(self.search, 0, None)
		
		self.first_match = matches
		self.next_match = matches
		if matches != None:
			(match_start, match_end) = matches
			self.sourceview.scroll_to_iter(match_start, 0, True, 0.5, 0.5)
			
			self.match_number = 1
			self.plugins["message_notify.message_notify"].show_message( \
						"Search Results | " + str(self.match_number) + "/" + str(self.count))
			self.highlight_scrolled()
		
			
	
	def scroll_next(self):
		if not self.next_match:
			return
		
		(match_start, match_end) = self.next_match
		
		
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
		
		self.next_match = match_end.forward_search(self.search, 0, None)
				
		if self.next_match != None:
			(match_start, match_end) = self.next_match
			self.sourceview.scroll_to_iter(match_end, 0, True, 0.5, 0.5)
			
			self.match_number += 1
			self.plugins["message_notify.message_notify"].show_message( \
						"Search Results | " + str(self.match_number) + "/" + str(self.count))
			self.highlight_scrolled()
		else:
			# call again scroll to go up
			self.scroll()
			# self.next_match = (self.buffer.get_start_iter(), self.buffer.get_start_iter())
			# self.match_number = 0
			# self.scroll_next()
			
			
			
			
	def scroll_prev(self):
		if not self.next_match:
			return
		
		(match_start, match_end) = self.next_match
		self.next_match = match_start.backward_search(self.search, 0, None)
		
		if self.next_match != None:
			(match_start, match_end) = self.next_match
			self.sourceview.scroll_to_iter(match_end, 0, True, 0.5, 0.5)
			
			self.match_number -= 1
			self.plugins["message_notify.message_notify"].show_message( \
							"Search Results | "	+ str(self.match_number) + "/" + str(self.count))
			self.highlight_scrolled()
		else:
			# scroll from the end
			self.next_match = (self.buffer.get_end_iter(), self.buffer.get_end_iter())
			self.match_number = self.count + 1
			self.scroll_prev()
			
	
	
	def highlight_scrolled(self):
		(start_iter, end_iter) = self.next_match
		self.tag = self.plugins["highlight.highlight"].setup_custom_tag(self.buffer, self.tag_name, self.props)
		self.plugins["highlight.highlight"].highlight_custom_tag(self.buffer, start_iter, end_iter, self.tag, self.tag_name)
		
		
		

	def clear_search(self, widget):
		self.search = ""
		widget.set_text(self.search)
		self.plugins["highlight.highlight"].remove_highlight(self.tag_name)
	
