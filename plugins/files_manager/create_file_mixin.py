
from .file import File

class CreateFileMixin(object):
	def create_new_file(self):
		# get new sourceview from sourceview_manager
		# TODO: must handled by ui manager
		newsource = self.sourceview_manager.get_new_sourceview()
		
		# default empty file when open editor with no opened files
		self.current_file = File("New File", newsource, new_file=True)

		# add empty/current_file to files array
		self.files.append(self.current_file)
		
		self.plugins["ui_manager.ui_manager"].files_ui.add_filename_to_ui(self.current_file)
		self.plugins["ui_manager.ui_manager"].files_ui.replace_sourceview_widget(self.current_file.source_view)
		# set headerbar text to the filename
		self.plugins["ui_manager.ui_manager"].files_ui.update_header(self.current_file.filename)
		# update ui, set selected
		self.plugins["ui_manager.ui_manager"].files_ui.set_currently_displayed(self.current_file.ui_ref)
		
