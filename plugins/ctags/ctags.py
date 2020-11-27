#
#### Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Nov 24th, 2020
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

import subprocess

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

from .commands_ctrl import CommandsCtrl

class Ref(object):
	pass

class Plugin(CommandsCtrl):

	def __init__(self, app):
		self.name = "ctags"
		self.app = app
		self.THE = app.plugins_manager.THE
		self.signal_handler = app.signal_handler
		self.handlers = app.signal_handler.handlers
		self.commands = []
		self.symbols = {}

		self.signal_handler.connect("file-opened", self.file_opened)
		self.signal_handler.connect("file-closed", self.file_closed)



	def activate(self):
		self.set_handlers()

	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		pass


	def set_handlers(self):
		self.handlers.on_sourceview_button_press_event = self.goto_symbol



	def file_closed(self, filename):
		for k in self.symbols.copy():

			v = self.symbols[k]

			for d in reversed(v["duplicate"]):
				if d[1] == filename:
					# print(d[0], d[1], d[2])
					self.update_commanders_remove(d[2].commander_ref)
					v["duplicate"].remove(d)

			if v["data"][1] == filename:
				# print(k["data"][1], k["data"][2])
				self.update_commanders_remove(v["data"][2].commander_ref)

				if not v["duplicate"]:
					del self.symbols[k]
				else:
					# move last item in duplicate array to dic:value
					self.symbols[k]["data"] = self.symbols[k]["duplicate"][-1]
					self.symbols[k]["duplicate"].remove(self.symbols[k]["duplicate"][-1])




	def file_opened(self, filename):
		ctags = subprocess.Popen(["ctags", "-x", filename], stdout=subprocess.PIPE)
		output = subprocess.Popen(["awk", '{print $1 \" \" $3 \" \" $4}'], \
						stdin=ctags.stdout, stdout=subprocess.PIPE, \
						encoding='UTF-8')
		ctags.wait()

		while True:
			line = output.stdout.readline()

			if not line:
				break

			arr = line.strip().split()

			arr.append(Ref())

			if arr[0] not in self.symbols:
				self.symbols[arr[0]] = {
					"data": arr[1:],
					"duplicate": []
				}
			else:
				self.symbols[arr[0]]["duplicate"].append(arr[1:])

			self.update_commanders_add(arr)

			# print(arr[3].commander_ref)
		# end while



	def goto_symbol(self, widget, e):
		ctrl = (e.state & Gdk.ModifierType.CONTROL_MASK)

		if not (ctrl and e.state):
			return

		word = self.get_selected()

		if word in self.symbols:
			current_file = self.THE("files_manager", "get_current_file", {})
			self._goto_symbol({"word": word, "filename": current_file.filename})


	def _goto_symbol(self, args):

		word = args["word"]
		filename = args["filename"]

		symbol_data = self.symbols[word]

		_line_number	= symbol_data["data"][0]
		_filename	= symbol_data["data"][1]

		if filename and symbol_data["data"][1] != filename:
			for d in symbol_data["duplicate"]:
				if d[1] == filename:
					_line_number	= d[0]
					_filename	= d[1]
					break


		file_index = self.THE("files_manager", "get_file_index", \
					{"filename": _filename})

		is_file_loaded = self.THE("files_manager", "is_file_loaded", \
					{"file_index": file_index})

		self.THE("files_manager", "switch_to_file", \
					{"file_index": file_index})

		sourceview	= self.app.window.current_file.source_view
		buffer		= sourceview.get_buffer()

		symbol_iter = buffer.get_iter_at_line(int(_line_number) - 1)
		buffer.place_cursor(symbol_iter)

		if is_file_loaded:
			sourceview.scroll_to_mark(buffer.get_insert(), 0.20, False, 1.0, 0.5)
		else:
			GLib.idle_add(sourceview.scroll_to_mark, buffer.get_insert(), 0.20, False, 1.0, 0.5)



	def get_selected(self):
		sourceview	= self.app.window.current_file.source_view
		buffer		= sourceview.get_buffer()

		currentPosMark = buffer.get_insert()

		s_iter = buffer.get_iter_at_mark(currentPosMark)
		e_iter = s_iter.copy()

		if not self.valid_selection(s_iter):
			return

		self.move_to_word_beginning(s_iter)
		self.move_to_word_end(e_iter)

		return buffer.get_text(s_iter, e_iter, False).strip()



	def valid_selection(self, s_iter):
		if s_iter.get_char().isalpha():
			return True

		if s_iter.get_char().isnumeric():
			return True

		if s_iter.get_char() == "_":
			return True

		return False



	def move_to_word_beginning(self, s_iter):
		while not s_iter.starts_line():
			c = s_iter.get_char()
			if not (c.isalpha() or c.isnumeric() or c == "_"):
				s_iter.forward_char()
				return

			if not s_iter.backward_char():
				return
		# end while

		s_iter.forward_char()



	def move_to_word_end(self, e_iter):
		while not e_iter.ends_line():

			c = e_iter.get_char()
			if not (c.isalpha() or c.isnumeric() or c == "_"):
				return

			if not e_iter.forward_char():
				return
