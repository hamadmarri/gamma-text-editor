
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class CopyLine(object):
	
	def copy_line(self):
		
		# get current viewing file' buffer
		self.buffer = self.plugins["files_manager.files_manager"].current_file.source_view.get_buffer()
		
		# get selection bound
		selection = self.buffer.get_selection_bounds()
		
		# if user selected text, then exit
		# no need for fast copy a line
		if selection != ():
			return
			
		
		# if selection is empty
		# get current insert position mark (insert = cursor)
		currentPosMark = self.buffer.get_insert()
		start = self.buffer.get_iter_at_mark(currentPosMark)
		start.set_line_offset(0)
		end = start.copy()
		if not end.ends_line():
			end.forward_to_line_end()
		
		# if empty line (i.e. start == end), the exit
		if start.get_offset() == end.get_offset():
			return
		
		# copy text only without white spaces/indentations
		start = self.discard_white_spaces(start)
		
		# get line text
		line = self.buffer.get_text(start, end, False)
		
		# copy line in clipboard
		self.copy_to_clipboard(line)
		
		
		
		
	def discard_white_spaces(self, iter):
		while not iter.ends_line():
			# get char where the current iter pointing to
			c = iter.get_char()
			
			# check if c is not white space
			if c != " " and c != "\t":
				return iter
			
			iter.forward_char()
		
		return iter
		
		
		
	def copy_to_clipboard(self, line):
		clipboard = Gtk.Clipboard.get_default(Gdk.Display.get_default())
		clipboard.set_text(line, -1)
		
		
		
		