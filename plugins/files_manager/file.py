# each openned file is set in File object and
# appended to "files" array
class File():
	def __init__(self, filename, source_view, ui_ref=None,
					need_save=False, new_file=False, init_file=False):
		self.filename = filename
		self.source_view = source_view
		self.ui_ref = ui_ref
		self.init_file = init_file
		self.need_save = need_save
		self.new_file = new_file
		self.editted = False
		
		# if source_view is not empty,
		# then connect buffer changed signal
		# to detect if file has been editted
		if self.source_view:
			buffer = self.source_view.get_buffer()
			buffer.connect("changed", self.buffer_changed)
			
		
		
	
	def buffer_changed(self, buffer):
		self.set_editted()



	def set_editted(self):
		print(f"editted {self.filename}")
		self.editted = True