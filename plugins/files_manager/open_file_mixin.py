
from .file import File


class OpenFileMixin(object):
	# open_files is called by openfile plugin 
	# it loops through all filenames and open each one
	# by calling open_file method
	def open_files(self, filenames):
		for f in filenames:
			self.open_file(f)
				
		self.current_file = self.files[-1]
		self.plugins["ui_manager.ui_manager"].replace_sourceview_widget(self.current_file.source_view)
		
		# set headerbar text to the filename
		self.plugins["ui_manager.ui_manager"].update_header(self.current_file.filename)
		
		# update ui, set selected
		self.plugins["ui_manager.ui_manager"].set_currently_displayed(self.current_file.ui_ref)
			
	
	
	
	# TODO: this method is doing too much, must get seperated
	def open_file(self, filename):
		# check if file is already opened
		file_index = self.is_already_openned(filename)
		if file_index >= 0:
			# if already open then just switch to it and exit method
			self.switch_to_file(file_index)
			return
		
		
		# open the file in reading mode
		f = open(filename, "r", encoding="utf-8", errors="replace")
		# DEBUG: print(f"{filename} opened")
		
		# actual reading from the file and populate the new sourceview buffer
		# with file data
		text = f.read()
		
		
		# get new sourceview from sourceview_manager
		# TODO: must handled by ui manager
		newsource = self.sourceview_manager.get_new_sourceview()
		# DEBUG: print("newsource")
				
		# new File object
		newfile = File(filename, newsource)
		# DEBUG: print("newfile")
		
		# if empty file only is currently opened, replace it
		if len(self.files) == 1 and self.files[0].filename == "empty":
			self.files[0].source_view.destroy()
			del self.files[0]
		
		# add newfile object to "files" array
		self.files.append(newfile)
		# DEBUG: print("files.append")
					
			
		# DEBUG: print("text is read")
				
		newsource.get_buffer().set_text(text)
				
		# place cursor at the begining
		newsource.get_buffer().place_cursor(newsource.get_buffer().get_start_iter())
		
		# close file object
		f.close()
		# DEBUG: print(f"{filename} closed")
		
		# set the language of just openned file 
		# see sourceview_manager
		buffer = newsource.get_buffer()
		self.sourceview_manager.set_language(filename, buffer)
		# DEBUG: print("set_language")
		
		self.plugins["ui_manager.ui_manager"].add_filename_to_ui(newfile)
				
		# set current file to this file
		# self.current_file = newfile
		
