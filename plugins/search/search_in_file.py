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
#
#	Quick search on current opened file. It is located at
#	the top of the editor. It auto scroll to first found
#	match and moving to the next/previous one by UP/DOWN keywords or Enter/Shift+Enter.
#	It is case sensitive. For case insensitive, see find_and_replace plugin.
#

import threading
import time

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
from . import commands

class Plugin():

	def __init__(self, app):
		self.name = "search_in_file"
		self.app = app
		self.signal_handler = app.signal_handler
		self.handlers = app.signal_handler.handlers
		self.THE = app.plugins_manager.THE
		self.commands = []
		self.search = None
		self.search_flags = 0
		self.whole_word = False
		self.is_highlight_done = False
		self.count = 0
		self.match_number = 0
		self.deleted_marks = 0
		self.old_start_iter = None
		self.old_end_iter = None
		self.current_selection = None
		self.timer = None
		self.search_time = 0.35 # seconds
		self.search_text = ""
		self.signal_handler.connect("file-switched", self.refresh_source)


		# for highlight current match
		self.props = {
			"weight": 1700,
			"background": "#dddd77",
		}
		self.app.window.search_tag = None
		self.tag_name = "selected_search"

		self.signal_handler.key_bindings_to_plugins.append(self)
		self.set_handlers()
		commands.set_commands(self)


	def activate(self):
		pass


	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if ctrl and keyval_name == "f":
			self.get_focus()


	# setting handlers, see SignalHandler
	def set_handlers(self):
		self.handlers.on_search_field_changed = self.on_search_field_changed
		self.handlers.on_search_key_press_event = self.on_search_key_press_event
		self.handlers.on_search_focus_out_event = self.on_search_focus_out_event


	def set_search_flags(self, search_flags):
		self.search_flags = search_flags


	def set_whole_word(self, whole_word):
		self.whole_word = whole_word


	def refresh_source(self, new_source):
		self.quit_search()
		self.app.window.search_sourceview = new_source
		self.app.window.search_buffer = self.app.window.search_sourceview.get_buffer()

		args = {
			"buffer": self.app.window.search_buffer,
			"tag_name": self.tag_name,
			"props": self.props
		}
		self.app.window.search_tag = self.THE("highlighter", "get_custom_tag", args)



	def on_search_key_press_event(self, widget, event):
		keyval_name = Gdk.keyval_name(event.keyval)
		shift = (event.state & Gdk.ModifierType.SHIFT_MASK)

		if keyval_name == "Escape":

			# before self.clear_search(before loosing search marks)
			# try to place the cursor on current selected text in sourceview
			self.place_cursor_to_selection()

			self.clear_search(widget)

			# set focus back to sourceview
			current_file = self.THE("files_manager", "get_current_file", {})
			if current_file:
				current_file.source_view.grab_focus()

		elif (shift and keyval_name == "Return") or keyval_name == "Up":
			self.search_flags = 0
			self.whole_word = False
			if not self.is_highlight_done:
				searchEntry = self.app.builder.get_object("searchEntry")
				self.search_text = searchEntry.get_text()
				self._do_highlight()
			self.scroll_prev()

		elif keyval_name == "Return" or keyval_name == "KP_Enter" or keyval_name == "Down":
			self.search_flags = 0
			self.whole_word = False
			if not self.is_highlight_done:
				searchEntry = self.app.builder.get_object("searchEntry")
				self.search_text = searchEntry.get_text()
				self._do_highlight()
			else:
				self.scroll_next()



	def on_search_focus_out_event(self, widget, data):
		self.quit_search()


	def place_cursor_to_selection(self):
		if self.old_start_iter:
			self.app.window.search_buffer.place_cursor(self.old_start_iter)


	def quit_search(self):
		self.is_highlight_done = False
		if hasattr(self.app.window, "search_buffer"):
			self.THE("highlighter", "remove_highlight", {"buffer": self.app.window.search_buffer, "tag": self.app.window.search_tag})
		self.set_selected_iters(None, None)
		if hasattr(self.app.window, "search_buffer"):
			self.THE("highlighter", "remove_highlight", {"buffer": self.app.window.search_buffer})
		self.update_style(-1)


	def get_focus(self):
		searchEntry = self.app.builder.get_object("searchEntry")

		# gets (start, end) iterators of
		# the selected text
		iters = self.app.window.search_buffer.get_selection_bounds()
		if iters:
			# when user selected some text
			# get the start and end iters
			(iter_start, iter_end) = iters

			# get the text is being selected, False means without tags
			# i.e. only appearing text without hidden tags set by sourceview
			# (read: https://developer.gnome.org/gtk3/stable/GtkTextBuffer.html#gtk-text-buffer-get-text)
			text = self.app.window.search_buffer.get_text(iter_start, iter_end, False)

			searchEntry.set_text(text)

		# set cursor to searchEntry
		searchEntry.grab_focus()
		self.update_style(0)




	def update_style(self, state):
		searchEntry = self.app.builder.get_object("searchEntry")

		searchEntry.get_style_context().remove_class("searching")
		searchEntry.get_style_context().remove_class("searchSuccess")
		searchEntry.get_style_context().remove_class("searchFail")

		if state == 0:
			# searching in blue
			searchEntry.get_style_context().add_class("searching")
		elif state == 1:
			# search success in green
			searchEntry.get_style_context().add_class("searchSuccess")
		elif state == 2:
			# no results in red
			searchEntry.get_style_context().add_class("searchFail")



	def cancel_timer(self):
		if self.timer:
			self.timer.cancel()
			GLib.idle_remove_by_data(None)

	def delay_search_Glib(self):
		GLib.idle_add(self._do_highlight)

	def delay_search(self):
		wait_time = self.search_time / len(self.search_text)
		wait_time = max(wait_time, 0.05)

		self.timer = threading.Timer(wait_time, self.delay_search_Glib)
		self.timer.daemon = True
		self.timer.start()



	# (see https://developer.gnome.org/gtk3/stable/GtkSearchEntry.html)
	# (https://developer.gnome.org/gtk3/stable/GtkEntry.html)
	def on_search_field_changed(self, widget):
		self.cancel_timer()

		self.search_flags = 0
		self.whole_word = False

		self.search_text = widget.get_text()

		# texts between 1 and 4 inclusive go delay
		if len(self.search_text) > 0 and len(self.search_text) < 5:
			self.delay_search()
		else:
			self._do_highlight()


	# (see https://developer.gnome.org/gtk3/stable/GtkSearchEntry.html)
	# (https://developer.gnome.org/gtk3/stable/GtkEntry.html)
	def do_highlight(self, search, buffer):
		self.search_text = search
		self._do_highlight()
	
	def _do_highlight(self):

		search = self.search_text
		buffer = self.app.window.search_buffer

		if buffer:
			self.app.window.search_buffer = buffer

		# remove selected tag (bold text)
		self.THE("highlighter", "remove_highlight", {"buffer": self.app.window.search_buffer, "tag": self.app.window.search_tag})
		self.set_selected_iters(None, None)

		# print(f"search.whole_word: {self.whole_word}")
		self.search = search

		args = {
			"buffer": buffer,
			"search": self.search,
			"search_flags": self.search_flags,
			"whole_word": self.whole_word
		}
		self.count = self.THE("highlighter", "highlight", args)

		# if no results while search is not empty
		if self.count == 0 and self.search:
			self.THE("message_notifier", "show_message", {"m": "Search Results | 0"})
			self.update_style(2)
			return

		if not self.search:
			self.update_style(0)
		else:
			self.update_style(1)

		self.is_highlight_done = True

		# scroll to first occurrence of search if not empty
		if self.search:
			self.match_number = -1
			self.deleted_marks = 0
			self.scroll_next()



	def scroll_next(self):
		marks = self.THE("highlighter", "marks", None)

		if not marks:
			return

		self.match_number += 1

		if self.match_number * 2 == len(marks):
			self.match_number = 0

		self.scroll(marks)



	def scroll_prev(self):
		marks = self.THE("highlighter", "marks", None)

		if not marks:
			return

		if self.match_number == 0:
			self.match_number = (len(marks) // 2)

		self.match_number -= 1
		self.scroll(marks)


	def scroll(self, marks):
		next_mark_pos = self.match_number * 2
		match_start = self.app.window.search_buffer.get_iter_at_mark(marks[next_mark_pos])
		match_end = self.app.window.search_buffer.get_iter_at_mark(marks[next_mark_pos + 1])

		self.app.window.search_sourceview.scroll_to_mark(marks[self.match_number * 2], 0.20, False, 1.0, 0.5)
		self.THE("message_notifier", "show_message", \
						{"m": "Search Results | " + str(self.match_number + self.deleted_marks + 1) + "/" + str(self.count)})

		self.highlight_scrolled(match_start, match_end)



	def highlight_scrolled(self, start_iter, end_iter):
		args = {
			"buffer": self.app.window.search_buffer,
			"tag_name": self.tag_name,
			"props": self.props
		}
		self.app.window.search_tag = self.THE("highlighter", "get_custom_tag", args)

		# remove old highlight
		if self.old_start_iter:
			args = {
				"buffer": self.app.window.search_buffer,
				"tag": self.app.window.search_tag,
				"start_iter": self.old_start_iter,
				"end_iter": self.old_end_iter
			}
			self.THE("highlighter", "remove_highlight", args)

		args = {
			"buffer": self.app.window.search_buffer,
			"start_iter": start_iter,
			"end_iter": end_iter,
			"tag": self.app.window.search_tag
		}
		self.THE("highlighter", "highlight_custom_tag", args)
		self.set_selected_iters(start_iter, end_iter)



	def clear_search(self, widget):
		self.search = ""
		widget.set_text(self.search)
		self.THE("highlighter", "remove_highlight", {"buffer": self.app.window.search_buffer, "tag": self.app.window.search_tag})


	def set_selected_iters(self, s_iter, e_iter):
		self.old_start_iter = s_iter
		self.old_end_iter = e_iter
		if s_iter:
			self.current_selection = (s_iter, e_iter)
		else:
			self.current_selection = None



	def delete_current_marks(self):
		marks = self.THE("highlighter", "marks", None)

		s_mark = marks[self.match_number * 2]
		e_mark = marks[(self.match_number * 2) + 1]

		self.app.window.search_buffer.delete_mark(s_mark)
		self.app.window.search_buffer.delete_mark(e_mark)

		del marks[(self.match_number * 2) + 1]
		del marks[self.match_number * 2]

		self.match_number -= 1
		self.deleted_marks += 1

