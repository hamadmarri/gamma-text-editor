

class DuplicateLine(object):
	
	def duplicate_line(self):
		# get current viewing file's buffer		
		current_file = self.THE("files_manager", "current_file", None)
		if not current_file:
			return
		
		buffer = current_file.source_view.get_buffer()
		
		# get selection bound
		selection = buffer.get_selection_bounds()
		
		# if user selected text, then exit
		if selection != ():
			return None
			
		# if selection is empty
		# get current insert position mark (insert = cursor)
		currentPosMark = buffer.get_insert()
		start = buffer.get_iter_at_mark(currentPosMark)
		start.set_line_offset(0)
		end = start.copy()
		if not end.ends_line():
			end.forward_to_line_end()
		
		# if empty line (i.e. start == end), the exit
		if start.get_offset() == end.get_offset():
			return
		
		# get line text
		line = buffer.get_text(start, end, False)
		buffer.insert(end, f"\n{line}")
		
		# get end iters position to re-place the cursor
		current_cursor = buffer.get_insert()
		c_iter = buffer.get_iter_at_mark(current_cursor)
		
		# if at the end of the line, no need to move 
		# the cursos, it moves automatically
		if not c_iter.ends_line():
			# count offset from start of line to current cursor
			offset = c_iter.get_line_offset()
			
			# move to next line
			c_iter.forward_line()
			
			# move same offsets
			c_iter.forward_chars(offset)
			
			buffer.place_cursor(c_iter)
		
		
		
		
		
