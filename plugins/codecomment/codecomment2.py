#
#### Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Feb 19th, 2020
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


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from . import commands

class Plugin():
	

	def __init__(self, app):
		self.name = "codecomment.codecomment2"
		self.app = app
		self.plugins = app.plugins_manager.plugins
		self.signal_handler = app.signal_handler
		self.commands = []
	
	# do not remove 
	def activate(self):
		self.signal_handler.key_bindings_to_plugins.append(self)
#		commands.set_commands(self)

	

	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		print(keyval_name, event.keyval)
		if shift and ctrl and keyval_name == "question":
			self.do_comment()
			
			
			
			

	def do_comment(self):
		sourceview = self.plugins["files_manager.files_manager"].current_file.source_view
		buffer = sourceview.get_buffer()
		
		
		
		sel = buffer.get_selection_bounds()
		currentPosMark = buffer.get_insert()
		deselect = False
		if sel != ():
			(start, end) = sel
			if start.ends_line():
				start.forward_line()
			elif not start.starts_line():
				start.set_line_offset(0)
			if end.starts_line():
				end.backward_char()
			elif not end.ends_line():
				end.forward_to_line_end()
		else:
			deselect = True
			start = buffer.get_iter_at_mark(currentPosMark)
			start.set_line_offset(0)
			end = start.copy()
			end.forward_to_line_end()

		lang = buffer.get_language()
		if lang is None:
			return

		(start_tag, end_tag) = self.get_comment_tags(lang)

		if not start_tag and not end_tag:
			return

		new_code = self.add_comment_characters(buffer,
                                                   start_tag,
                                                   end_tag,
                                                   start,
                                                   end)

		if deselect:
			oldPosIter = buffer.get_iter_at_mark(currentPosMark)
			buffer.select_range(oldPosIter,oldPosIter)
			buffer.place_cursor(oldPosIter)


	
	
	
	
	
	def get_comment_tags(self, lang):
		(s, e) = self.get_line_comment_tags(lang)
		if (s, e) == (None, None):
			(s, e) = self.get_block_comment_tags(lang)
		return (s, e)


	def get_block_comment_tags(self, lang):
		start_tag = lang.get_metadata('block-comment-start')
		end_tag = lang.get_metadata('block-comment-end')
		if start_tag and end_tag:
			return (start_tag, end_tag)
		return (None, None)
		
		
	def get_line_comment_tags(self, lang):
		start_tag = lang.get_metadata('line-comment-start')
		if start_tag:
			return (start_tag, None)
		return (None, None)


	def add_comment_characters(self, document, start_tag, end_tag, start, end):
		smark = document.create_mark("start", start, False)
		imark = document.create_mark("iter", start, False)
		emark = document.create_mark("end", end, False)
		number_lines = end.get_line() - start.get_line() + 1
		
		document.begin_user_action()

		for i in range(0, number_lines):
			iter = document.get_iter_at_mark(imark)
			if not iter.ends_line():
				document.insert(iter, start_tag)
				if end_tag is not None:
					if i != number_lines -1:
						iter = document.get_iter_at_mark(imark)
						iter.forward_to_line_end()
						document.insert(iter, end_tag)
					else:
						iter = document.get_iter_at_mark(emark)
						document.insert(iter, end_tag)
			iter = document.get_iter_at_mark(imark)
			iter.forward_line()
			document.delete_mark(imark)
			imark = document.create_mark("iter", iter, True)

		document.end_user_action()

		document.delete_mark(imark)
		new_start = document.get_iter_at_mark(smark)
		new_end = document.get_iter_at_mark(emark)
		if not new_start.ends_line():
			self.backward_tag(new_start, start_tag)
		document.select_range(new_start, new_end)
		document.delete_mark(smark)
		document.delete_mark(emark)
		
	
	
	def backward_tag(self, iter, tag):
		iter.backward_chars(len(tag))
		
		
		
		
#		new_code = self.remove_comment_characters(document,
#                                                      start_tag,
#                                                      end_tag,
#                                                      start,
#                                                      end)



#def remove_comment_characters(self, document, start_tag, end_tag, start, end):
#        smark = document.create_mark("start", start, False)
#        emark = document.create_mark("end", end, False)
#        number_lines = end.get_line() - start.get_line() + 1
#        iter = start.copy()
#        head_iter = iter.copy()
#        self.forward_tag(head_iter, start_tag)

#        document.begin_user_action()

#        for i in range(0, number_lines):
#            if self.get_tag_position_in_line(start_tag, head_iter, iter):
#                dmark = document.create_mark("delete", iter, False)
#                document.delete(iter, head_iter)
#                if end_tag is not None:
#                    iter = document.get_iter_at_mark(dmark)
#                    head_iter = iter.copy()
#                    self.forward_tag(head_iter, end_tag)
#                    if self.get_tag_position_in_line(end_tag, head_iter, iter):
#                        document.delete(iter, head_iter)
#                document.delete_mark(dmark)
#            iter = document.get_iter_at_mark(smark)
#            iter.forward_line()
#            document.delete_mark(smark)
#            head_iter = iter.copy()
#            self.forward_tag(head_iter, start_tag)
#            smark = document.create_mark("iter", iter, True)

#        document.end_user_action()

#        document.delete_mark(smark)
#        document.delete_mark(emark)
        
        