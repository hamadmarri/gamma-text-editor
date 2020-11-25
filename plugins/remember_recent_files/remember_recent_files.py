#
#### Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Nov 23th, 2020
#
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

import os

class Plugin():
	def __init__(self, app):
		self.name = "remember_recent_files"
		self.app = app
		self.THE = app.plugins_manager.THE
		self.window = self.app.window
		self.commands = []

		self.location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


	def activate(self):
		filenames = self.get_stored_file_names()
		self.THE("files_manager", "open_files", {"filenames": filenames})



	def store_file_names(self):
		f = open(os.path.join(self.location, 'recent_files.txt'), 'w', encoding='utf-8')

		for file_obj in self.window.files:
			if file_obj.filename != "empty":
				f.write(file_obj.filename + "\n")

		f.close()



	def get_stored_file_names(self):
		filenames = []

		try:
			f = open(os.path.join(self.location, 'recent_files.txt'), 'r', encoding='utf-8')

			lines = f.readlines()

			for l in lines:
				filenames.append(l.strip())

			f.close()

		except:
			pass

		return filenames
