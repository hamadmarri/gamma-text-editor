
import os


class CommandsCtrl(object):

	def update_commanders_remove(self, newfile):
		commander_ref = newfile.commander_ref
		self.THE("commander", "remove_command", {"node": commander_ref})



	def update_commanders_add(self, newfile):
		basename = os.path.basename(newfile.filename)
		c = {
			"plugin-name": self.name,
			"name": f"Switch to -- {basename}",
			"ref": self.switch_command,
			"parameters": newfile.filename,
			"shortcut": "",
		}

		commander_ref = self.THE("commander", "add_command", {"c": c})
		newfile.commander_ref = commander_ref




	def switch_command(self, filename):
		 index = self.get_file_index(filename)
		 self.switch_to_file(index)
