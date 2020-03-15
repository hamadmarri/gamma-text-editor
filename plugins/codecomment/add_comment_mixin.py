
class AddCommentMixin(object):
	def add_comment_characters(self, document, start_tag, end_tag, start, end, deselect, oldPos):
		smark = document.create_mark("start", start, False)
		imark = document.create_mark("iter", start, False)
		emark = document.create_mark("end", end, False)
		number_lines = end.get_line() - start.get_line() + 1
		comment_pos_iter = None
		count = 0
		
		document.begin_user_action()

		for i in range(0, number_lines):
			iter = document.get_iter_at_mark(imark)
				
			if not comment_pos_iter:
				(comment_pos_iter, count) = self.discard_white_spaces(iter)
								
				# check if already commented
				if self.is_commented(comment_pos_iter, start_tag):
					new_code = self.remove_comment_characters(document, start_tag, end_tag, start, end)
					return
					
			else:
				comment_pos_iter = iter
				# move iter to match first alignment
				for i in range(count):
					# get char where the current iter pointing to
					c = iter.get_char()
					if not c in (" ", "\t"):
						break
					iter.forward_char()
					
			document.insert(comment_pos_iter, start_tag)
			
			# also insert a space
			document.insert(comment_pos_iter, " ")
			
			# if block tag (/*    */) style
			if end_tag:
				# if not the last selected line
				if i != number_lines -1:
					# place the end block tag (*/) to end of line
					iter = document.get_iter_at_mark(imark)
					iter.forward_to_line_end()
					document.insert(iter, end_tag)
				else:
					# place the end block tag to end of selection
					iter = document.get_iter_at_mark(emark)
					document.insert(iter, end_tag)
					
						
			iter = document.get_iter_at_mark(imark)
			iter.forward_line()
			document.delete_mark(imark)
			imark = document.create_mark("iter", iter, True)
		# end for

		document.end_user_action()

		document.delete_mark(imark)
		new_start = document.get_iter_at_mark(smark)
		new_end = document.get_iter_at_mark(emark)
		# if not new_start.ends_line():
		#	self.backward_tag(new_start, start_tag)
		document.select_range(new_start, new_end)
		document.delete_mark(smark)
		document.delete_mark(emark)
		
		# place the cursor to its old position
		if deselect:
			oldPosIter = document.get_iter_at_offset(oldPos + 2)
			document.place_cursor(oldPosIter)
