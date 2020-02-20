from .file import File

class CloseFileMixin(object):
	
	
	def close_file(self, filename):
		# check if the current file is being closed
		if self.current_file.filename == filename:
			self.close_current_file()
			
		else:
			# get  file index
			to_close_index = self.get_file_index(filename)
					
			# destroy file
			self.destroy_file(to_close_index)				

		
	
	def close_all(self):
		# > 1 to not delete empty init file
		while len(self.files) > 1:
			self.close_current_file()
		
		
		
	
	# TODO: check if need saving before close
	def close_current_file(self):
		# if current file is new file created by user, and not saved
		# then ask to save it first
		# TODO: prompt do you want save window
			
		# if length > 2, then close current and switch to previouse file 
		# in "files" array
		if len(self.files) > 2:
			# get current file index
			to_close_index = self.get_file_index(self.current_file.filename)
					
			# destroy file
			self.destroy_file(to_close_index)
			
			# switch to last file
			self.switch_to_file(len(self.files) - 1)

		
		# if empty file only there, do nothing
		elif len(self.files) == 1 and self.files[0].init_file:
			return
			
			
		# if 2 files (a signle file, and empty in array), close and make empty file to stay 
		# in the view
		else:			
			# remove current sourceview and put the new empty sourceview
			self.plugins["ui_manager.ui_manager"].replace_sourceview_widget(self.files[0].source_view)
			
			# current file is now empty
			self.current_file = self.files[0]
			
			# destroy opened file 
			self.destroy_file(1)
						
			# since it is an empty file, set the headerbar to "Gamma"
			self.plugins["ui_manager.ui_manager"].set_header("Gamma")
			
			# cancel and clear message 
			# why? sometimes user save a file and close it right after,
			# so no need to keep showing that file is saved
			self.plugins["message_notify.message_notify"].cancel()
		
			
	
	

	def destroy_file(self, file_index):		
		# destroy the ui_ref btn attached to file TODO: move to ui manager
		self.files[file_index].ui_ref.destroy()
		
		# remove from "files" array
		del self.files[file_index]
	
	
