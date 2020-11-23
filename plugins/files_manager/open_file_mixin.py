
from .file import File


# TODO: scroll up the file when opened
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
			self.switch_to_file(self.files_len() - 1)
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

		try:
			# open the file in reading mode
			f = open(filename, "r", encoding="utf-8", errors="replace")
			#f = open(filename, "r")
			# actual reading from the file and populate the new sourceview buffer
			# with file data
			text = f.read()
			# DEBUG: print(bytes(text, "ascii"))
		except PermissionError as err:
			self.signal_handler.emit("log-error", self, f'Could not open {filename}: {err}')
			return
		except OSError as err:
			self.signal_handler.emit("log-error", self, f'Could not open {filename}: {err}')
			return


		# when successfully opened and read the file
		else:
			# get new sourceview from sourceview_manager
			newsource = self.THE("sourceview_manager", "get_new_sourceview", {})

			# begin_not_undoable_action to prevent ctrl+z to empty the file
			newsource.get_buffer().begin_not_undoable_action()
			newsource.get_buffer().set_text(text)
			newsource.get_buffer().end_not_undoable_action()

			# place cursor at the begining
			newsource.get_buffer().place_cursor(newsource.get_buffer().get_start_iter())

			# close file object
			f.close()
		# end of try block


		# new File object
		newfile = File(self, filename, newsource)

		# add newfile object to "files" array
		self.add_file_to_list(newfile)

		# set the language of just openned file
		# see sourceview_manager
		buffer = newsource.get_buffer()
		self.THE("sourceview_manager", "set_language", {
					"filename": filename,
					"buffer": buffer
				})

		self.THE("ui_manager", "add_filename_to_ui", {"newfile": newfile})

		self.signal_handler.emit("log", self, f"open {filename}")







