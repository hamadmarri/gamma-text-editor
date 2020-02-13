

def set_commands(plugin):
	plugin.commands.append( 
		{
			"plugin-name": plugin.name,
			"name": "A command name 1",
			"ref": plugin.a_method1,
			"shortcut": "<Alt><Ctrl>+n",
		}
	)
	
	plugin.commands.append( 
		{
			"plugin-name": plugin.name,
			"name": "A command name 2",
			"ref": plugin.a_method2,
			"shortcut": "<Alt>+t",
		}
	)
	
	plugin.commands.append( 
		{
			"plugin-name": plugin.name,
			"name": "A command name 3",
			"ref": plugin.a_method3,
			"shortcut": "<Shift><Ctrl>+a",
		}
	)
	
