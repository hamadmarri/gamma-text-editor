# each openned file is set in File object and
# appended to "files" array
class File():
	def __init__(self, filename, source_view, ui_ref=None,
					need_save=False, new_file=False):
		self.filename = filename
		self.source_view = source_view
		self.ui_ref = ui_ref
		self.need_save = need_save
		self.new_file = new_file
