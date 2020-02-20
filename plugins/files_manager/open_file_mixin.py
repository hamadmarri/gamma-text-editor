
from .file import File


class OpenFileMixin(object):
	# open_files is called by openfile plugin 
	# it loops through all filenames and open each one
	# by calling open_file method
	def open_files(self, filenames):
		if not filenames:
			return
			
		for f in filenames:
			self.open_file(f)
	
		# if many files are opened, then switch to last open	
		if len(filenames) > 1:
			self.switch_to_file(len(self.files) - 1)
		else:
			# find the file (maybe it is in the list already)
			index = self.get_file_index(filenames[0])
			self.switch_to_file(index)



	
	# TODO: this method is doing too much, must get seperated
	def open_file(self, filename):
		# check if file is already opened
		file_index = self.is_already_openned(filename)
		if file_index >= 0:
			# if already open then just exit method
			#self.switch_to_file(file_index)
			return
		
		
		# open the file in reading mode
		f = open(filename, "r", encoding="utf-8", errors="replace")
		
		# actual reading from the file and populate the new sourceview buffer
		# with file data
		text = f.read()
				
		# get new sourceview from sourceview_manager
		# TODO: must handled by ui manager
		newsource = self.sourceview_manager.get_new_sourceview()
		newsource.get_buffer().set_text(text)

		# place cursor at the begining
		newsource.get_buffer().place_cursor(newsource.get_buffer().get_start_iter())
		
		# close file object
		f.close()
				
		# new File object
		newfile = File(self, filename, newsource)
				
		# add newfile object to "files" array
		self.files.append(newfile)
				
		# set the language of just openned file 
		# see sourceview_manager
		buffer = newsource.get_buffer()
		self.sourceview_manager.set_language(filename, buffer)

		self.plugins["ui_manager.ui_manager"].add_filename_to_ui(newfile)
		
		
