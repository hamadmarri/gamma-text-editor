#
#### Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Feb 11th, 2020
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
#	savefile: saves the current_file openned 
#	it gets current_file from files_manager plugin 
#	and saves it. Message notify is sent to tell the user
#	that the file is saved successfully
#

import os


# TODO: only save when buffer is changed
# TODO: empty file is saved at home!
class Plugin():
	
	def __init__(self, app):
		self.name = "savefile"
		self.app = app
		self.commands = []
		self.files_manager = None
		self.message_notify = None
		
		
	def activate(self):
		pass
	
	
	
	def get_plugins_refs(self):
		# get current_file
		if not self.files_manager:
			self.files_manager = self.app.plugins_manager.get_plugin("files_manager")
		
		# get message_notify
		if not self.message_notify:
			self.message_notify = self.app.plugins_manager.get_plugin("message_notify")
	
	
	
	# key_bindings is called by SignalHandler
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		
		# save is bound to "<Ctrl>+s"
		if ctrl and keyval_name == "s":
			
			self.get_plugins_refs()
			
			# get the current displayed file
			current_file = self.files_manager.current_file
			
			# get current buffer
			buffer = current_file.source_view.get_buffer()

			# get all buffer text without the hidden markups
			# (read: https://developer.gnome.org/gtk3/stable/GtkTextBuffer.html#gtk-text-buffer-get-text) 	
			text = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
			try:
				# save the file, in other words, copy text 
				# from buffer and write the file "current_file.filename"
				# in permenant storage (disk)
				open(current_file.filename, 'w').write(text)
			except SomeError as err:
				print('Could not save %s: %s' % (filename, err))
			else:
				# when successfully wrote the file, show successful message
				basename = os.path.basename(current_file.filename)
				self.message_notify.show_message(basename + " | Saved")
			

