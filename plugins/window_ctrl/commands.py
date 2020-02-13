

def set_commands(plugin):
	plugin.commands.append( 
		{
			"name": "toggle maximize",
			"ref": plugin.toggle_maximize,
			"shortcut": "<Alt>+m",
		}
	)
	
	plugin.commands.append( 
		{
			"name": "minimize",
			"ref": plugin.minimize,
			"shortcut": "<Ctrl><Alt>+m",
		}
	)
	
	plugin.commands.append( 
		{
			"name": "quit",
			"ref": plugin.quit,
			"shortcut": "<Ctrl>+q",
		}
	)
	
