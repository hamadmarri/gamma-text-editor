

def set_commands(plugin):
	plugin.commands.append( 
		{
			"plugin-name": plugin.name,
			"name": "Save File",
			"ref": plugin.save_current_file,
			"shortcut": "<Ctrl> + s",
		}
	)
	
	plugin.commands.append( 
		{
			"plugin-name": plugin.name,
			"name": "Save All",
			"ref": plugin.save_all,
			"shortcut": "<Ctrl><Alt> + s",
		}
	)
	
	plugin.commands.append( 
		{
			"plugin-name": plugin.name,
			"name": "Save As",
			"ref": plugin.save_as,
			"shortcut": "<Shift><Ctrl> + S",
		}
	)
	