
from .file import File



class CreateFileMixin(object):		
	def create_new_file(self):
	
		# if current file is the empty init file 
		# just rename
		if self.current_file.init_file:
			self.rename_file(self.current_file, f"New File {self.counter}")
			
			# set headerbar text to the filename
			self.plugins["ui_manager.ui_manager"].update_header(self.current_file.filename)
			
		else:
			# get new sourceview from sourceview_manager
			# TODO: must handled by ui manager
			newsource = self.sourceview_manager.get_new_sourceview()
			
			# default empty file when open editor with no opened files
			self.current_file = File(f"New File {self.counter}", newsource, new_file=True)

			# add empty/current_file to files array
			self.files.append(self.current_file)
			
			self.plugins["ui_manager.ui_manager"].add_filename_to_ui(self.current_file)
			self.plugins["ui_manager.ui_manager"].replace_sourceview_widget(self.current_file.source_view)
			# set headerbar text to the filename
			self.plugins["ui_manager.ui_manager"].update_header(self.current_file.filename)
			# update ui, set selected
			self.plugins["ui_manager.ui_manager"].set_currently_displayed(self.current_file.ui_ref)
		
		self.counter += 1
		self.current_file.set_editted()
