from pathlib import Path

home_path = str(Path.home())
gamma_path = home_path + "/dev/pygtk/gamma"
ui_file = "builder.ui"
style_file = "default.css"

config_paths_and_settings = {
	"ui-path":		gamma_path + "/ui/"		+ ui_file,
	"style-path":	gamma_path + "/style/"	+ style_file,
	"style-scheme":	"icecream",
}
