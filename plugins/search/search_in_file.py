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
#    


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
#from . import commands

class Plugin(): 

	def __init__(self, app):
		self.name = "search_in_file"
		self.app = app
		self.signal_handler = app.signal_handler
		self.builder = app.builder
		self.handlers = app.signal_handler.handlers
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
		
		# commands.set_commands(self)
		self.set_handlers()
			

	def activate(self):
		self.signal_handler.key_bindings_to_plugins.append(self)
		
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
				self.do_highlight(self.searchEntry)
			self.scroll_prev()	
			
		elif keyval_name == "Return" or keyval_name == "KP_Enter" or keyval_name == "Down":
			if not self.is_highlight_done:
				self.do_highlight(self.searchEntry)
			else:
				self.scroll_next()
				
		
	
	def on_search_focus_out_event(self, widget, data):
		self.is_highlight_done = False
		self.plugins["highlight.highlight"].remove_highlight(self.tag_name)
		
			
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
				
	
	# (see https://developer.gnome.org/gtk3/stable/GtkSearchEntry.html)
	# (https://developer.gnome.org/gtk3/stable/GtkEntry.html)
	def on_search_field_changed(self, widget):
		self.do_highlight(widget)
		
	
	# (see https://developer.gnome.org/gtk3/stable/GtkSearchEntry.html)
	# (https://developer.gnome.org/gtk3/stable/GtkEntry.html)
	def do_highlight(self, searchEntry):
		self.plugins["highlight"].remove_highlight(self.tag_name)
		self.search = searchEntry.get_text()
		self.count = self.plugins["highlight.highlight"].highlight(self.search)
		self.is_highlight_done = True
		
		# if no results
		if self.count == 0:
			self.plugins["message_notify.message_notify"].show_message("Search Results | 0")
			return
			
		
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
			self.plugins["message_notify.message_notify"].show_message("Search Results | " + str(self.match_number) + "/" + str(self.count))
			self.highlight_scrolled()
		
			
	
	def scroll_next(self):
		if not self.next_match:
			return
		
		(match_start, match_end) = self.next_match
		self.next_match = match_end.forward_search(self.search, 0, None)
				
		if self.next_match != None:
			(match_start, match_end) = self.next_match
			self.sourceview.scroll_to_iter(match_end, 0, True, 0.5, 0.5)
			
			self.match_number += 1
			self.plugins["message_notify.message_notify"].show_message("Search Results | " + str(self.match_number) + "/" + str(self.count))
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
			self.plugins["message_notify.message_notify"].show_message("Search Results | " 
											+ str(self.match_number) + "/" + str(self.count))
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
	
