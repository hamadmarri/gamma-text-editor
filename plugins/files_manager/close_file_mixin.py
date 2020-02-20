
class CloseFileMixin(object):
	
	def close_all(self):
		# empty file will keep adding
		# if > 0, then infinite loop
		while len(self.files) > 1:
			self.close_current_file()

		# close the last file
		self.close_current_file()
			
		
			
			
	
	# TODO: check if need saving before close
	def close_current_file(self):
		
		# if current file is new file created by user, and not saved
		# then ask to save it first
		# TODO: prompt do you want save window
		if self.current_file.filename == "New File" and self.current_file.new_file:
			self.plugins["files_manager.savefile"].save_current_file()
		
	
		# if length > 2, then close current and switch to previouse file 
		# in "files" array
		if len(self.files) > 1:
			# first switch to previouse openned file
			self.switch_to_file(len(self.files) - 2)
			
			# destroy file, after switching, the current file 
			# become second last in the "files" array
			self.destroy_file(len(self.files) - 2)
			
			# update ui, set selected
			self.plugins["ui_manager.ui_manager"].set_currently_displayed(self.current_file.ui_ref)
		
		
		# if empty file only there, do nothing
		elif len(self.files) == 1 and self.files[0].filename == "empty":
			return
			
			
		# if signle file openned, close and make empty file to stay 
		# in the view
		else:
			# new sourceview for the empty file
			newsource = self.sourceview_manager.get_new_sourceview()
			
			# remove current sourceview and put the new empty sourceview
			self.plugins["ui_manager.ui_manager"].replace_sourceview_widget(newsource)
			
			# current file is now empty
			self.current_file = File("empty", newsource, new_file=True)
			
			# destroy opened file 
			self.destroy_file(0)
			
			# append empty file to "files" array
			self.files.append(self.current_file)
			
			# since it is an empty file, set the headerbar to "Gamma"
			self.plugins["ui_manager.ui_manager"].set_header("Gamma")
			
			# cancel and clear message 
			# why? sometimes user save a file and close it right after,
			# so no need to keep showing that file is saved
			self.plugins["message_notify.message_notify"].cancel()
		
			
	
	

	def destroy_file(self, file_index):
		# destroy the sourceview attached to file 
		self.files[file_index].source_view.destroy()
		
		# destroy the ui_ref btn attached to file TODO: move to ui manager
		self.files[file_index].ui_ref.destroy()
		
		# remove from "files" array
		del self.files[file_index]
	
	
