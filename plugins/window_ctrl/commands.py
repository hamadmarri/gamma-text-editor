

def set_commands(plugin):
	plugin.commands.append( 
		{
			"plugin-name": plugin.name,
			"name": "toggle maximize",
			"ref": plugin.toggle_maximize,
			"shortcut": "<Alt>+m",
		}
	)
	
	plugin.commands.append( 
		{
			"plugin-name": plugin.name,
			"name": "minimize",
			"ref": plugin.minimize,
			"shortcut": "<Ctrl><Alt>+m",
		}
	)
	
	plugin.commands.append( 
		{
			"plugin-name": plugin.name,
			"name": "quit",
			"ref": plugin.quit,
			"shortcut": "<Ctrl>+q",
		}
	)
	
