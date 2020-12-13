
import os


class CommandsCtrl(object):

	def update_commanders_remove(self, commander_ref):
		self.THE("commander", "remove_command", {"node": commander_ref})


	def update_commanders_add(self, symbol_data):

		# print(symbol, symbol_data)

		symbol		= symbol_data[0]
		line_number	= symbol_data[1]
		filename	= symbol_data[2]
		ref		= symbol_data[3]

		basename = os.path.basename(filename)
		c = {
			"plugin-name": self.name,
			"name": f"$: {symbol}",
			"ref": self._goto_symbol,
			"parameters": {"word": symbol, "filename": filename, "line_number": line_number},
			"shortcut": f"{basename}/{line_number}",
		}

		commander_ref = self.THE("commander", "add_command", {"c": c})
		ref.commander_ref = commander_ref

