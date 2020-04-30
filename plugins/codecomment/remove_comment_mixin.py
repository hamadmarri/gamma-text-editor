	

class RemoveCommentMixin(object):
	def remove_comment_characters(self, document, start_tag, end_tag, start, end):
		smark = document.create_mark("start", start, False)
		emark = document.create_mark("end", end, False)
		number_lines = end.get_line() - start.get_line() + 1
		iter = start.copy()
		head_iter = iter.copy()
		self.forward_tag(head_iter, start_tag)

		document.begin_user_action()

		for i in range(0, number_lines):
			# print(f"line {i}")
			if self.get_tag_position_in_line(start_tag, head_iter, iter):
				dmark = document.create_mark("delete", iter, False)
				document.delete(iter, head_iter)
				
				# delete the extra space added
				space_iter = head_iter.copy()
				space_iter.forward_char()
				s = head_iter.get_slice(space_iter)
				if s == " ":
					# remove 
					document.delete(head_iter, space_iter)
				
				if end_tag:
					iter = document.get_iter_at_mark(dmark)
					head_iter = iter.copy()
					self.forward_tag(head_iter, end_tag)
					if self.get_tag_position_in_line(end_tag, head_iter, iter):
						document.delete(iter, head_iter)
				document.delete_mark(dmark)
				
			iter = document.get_iter_at_mark(smark)
			iter.forward_line()
			document.delete_mark(smark)
			head_iter = iter.copy()
			self.forward_tag(head_iter, start_tag)
			smark = document.create_mark("iter", iter, True)

		document.end_user_action()

		document.delete_mark(smark)
		document.delete_mark(emark)