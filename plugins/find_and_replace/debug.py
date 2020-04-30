
class Debug(object):

	def debug_do_find(self, previous):
		msg = \
f"""<do_find> previous:{previous}, new_search:{self.new_search}, \
buffer:{self.find_text_view.get_buffer()}"""
		
		self.signal_handler.emit("debug", self, msg)