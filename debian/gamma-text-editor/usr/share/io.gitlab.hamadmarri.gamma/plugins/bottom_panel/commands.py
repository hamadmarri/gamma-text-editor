
def set_commands(plugin):
	plugin.commands.append( 
		{
			"plugin-name": plugin.name,
			"name": "Toggle Show/Hide Bottom Panel",
			"ref": plugin.toggle_bottom_panel,
			"shortcut": "F9",
		}
	)
