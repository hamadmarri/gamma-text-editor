
from .file import File


 
class CreateFileMixin(object):		
		
	def create_new_file(self):
		# get new sourceview from sourceview_manager
		newsource = self.THE("sourceview_manager", "get_new_sourceview", {})
		
		newfile = File(self, f"New File {self.counter}", newsource, new_file=True)

		# add empty/current_file to files array
		# self.files.append(newfile)
		self.add_file_to_list(newfile)
		
		self.THE("ui_manager", "add_filename_to_ui", {"newfile": newfile})
		self.switch_to_file(self.files_len() - 1)	
		
		self.counter += 1
		self.get_current_file().set_editted()
		
