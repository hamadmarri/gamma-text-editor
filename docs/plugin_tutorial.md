# Plugin Tutorial
In this tutorial you will be able to accomplish the following tasks:
*	Getting input or information from Gamma editor
*	Getting input or information from other plugins
*	Designing UI layout using Glade
*	Writing css for plugin widgets
*	Output back to the editor
*	Changing the main layout of Gamma (example, inserting a bottom panel)
*	Using other plugins features
*	Listening to GTK signals
*	Creating signals to your plugin 
*	Listening to plugins signals
*	The idea of the plugin would be a logger which logs every action\
	and outputs the log in bottom panel
*	Write help pages for your plugin


## Copy form the template
First step to start your plugin is to copy the `./plugins/template` folder and paste it with
your plugin name. Copy `./plugins/template` and rename the copy folder to `logger`. Your plugin
should be in the `./plugins/` folder alongside with other plugins.

The `./plugins/template` folder initially contains three python files:
-	`template.py`: is the template of your plugin main file.
-	`commands.py`: is the template of your plugin's commands (for the commander use)
-	`__init__.py`: a python file to tell that this folder is a python package.

Rename `template.py` to your plugin name, in our case it is `logger.py`.


## Author, Name of the plugin, and Remove unwanted comments and methods
Open `./logger/logger.py`, at top, write your name, email, and the date.
Change the name in `self.name = "template"` to the plugin name `self.name = "logger"`.
Remove any comments you do not need. Remove `method1`, `method2`, and `method3`.


## Add logger to plugins_array in plugins_manager
We need to add our plugin to be loaded to Gamma. Open `./plugins/plugins_manager.py`.
Add `"logger.logger",` to `plugin_list` (add it before this line `"commander.commander",`). 
 

## Test our plugin
Before we test our plugin, we need to do some clean up, and make sure we add our plugin to 
the `key_bindings_to_plugins` array. Remove the following code:
```
self.handlers = app.signal_handler.handlers
```
Since no need to handle signals from Gtk widgets in the main window other than keypress,
we do not need a reference to `signal_handler.handlers`. Also, remove the following:
```
def set_handlers(self):
	pass
```
Usually in `set_handlers` method, we have to bind Gtk signals to local methods, but for this tutorial
we need only key bindings. Instead of connecting to key press signals, the `signal_handler` does this job
for us, and it will call our `key_bindings` method. We do not want to handle every key press from the user.
To let `signal_handler` calls our `key_bindings` method only when user applay a shortcut such as `Ctrl+f`,
we need to uncomment this line: 
```
self.signal_handler.key_bindings_to_plugins.append(self)
```
Here we added our plugin to the `key_bindings_to_plugins` array. For any shortcuts entered by the user,
our `key_bindings` method will be called. Add the following code to `key_bindings`:
``` 
def key_bindings(self, event, keyval_name, ctrl, alt, shift):
	if shift and ctrl and keyval_name == "L":
		print("logger") 
```
The condition checks if the user held shift and ctrl when pressed `L`. If so, for testing purpose, print logger
to the console.

Before we test our plugin, comment or remove all code in `commands.py`, and
comment `commands.set_commands(self)` for now. We are going to use `set_commands` later
to export our commands/functionalities to commander plugin.

Close Gamma and run from command line `$ gamma`. Hold shift and ctrl and press `L`.
if `logger` is printed out in the terminal, then everything works as expected.


## Export our commands to the commander
To make it easier for us, instead of opening our plugin files every time,
close and reopen gamma again with the following: 
```
gamma plugins/logger/logger.py plugins/logger/commands.py
```

Uncomment `commands.set_commands(self)`. Change
``` 
def key_bindings(self, event, keyval_name, ctrl, alt, shift):
	if shift and ctrl and keyval_name == "L":
		print("logger") 
```
to 
``` 
def key_bindings(self, event, keyval_name, ctrl, alt, shift):
	if shift and ctrl and keyval_name == "L":
		self.show_log()
```

Create `show_log` method 
```
def show_log(self):
	print("logger")
```

Open `./plugins/logger/commands` (if it is not opened), delete any previous contents, and
write the following:
``` 
def set_commands(plugin):
	plugin.commands.append( 
		{
			"plugin-name": plugin.name,
 			"name": "Show Log",
 			"ref": plugin.show_log,
 			"shortcut": "<Shift><Ctrl> + L",
 		}
 	)
```
Basically, we just separated filling the `self.commands = []` array into another file. A better
way to do this is to use mixin instead of having a reference to `commands` as `commands.set_commands(self)`.
This will be edited in the future.

The commander expects and array called `commands` in your plugin. Each entry in the `commands` array is
expected to be a dictionary with the following attributes:
-	plugin-name: our plugin name
-	name: is the name/description of the command
-	ref: is method reference that gets called when run the command 
-	parameters: (optional) parameters to pass to the ref method
-	shortcut: the key binding/combination to call our command 


Restart Gamma, press `Alt` to open the commander. Then type `show log` in the search field,
you will see `Show Log` in the list with the shortcut `<Shift><Ctrl> + L`. Click on `Show Log`,
or hit enter if it is the first result. The method `show_log` gets called and `logger` is printed
out in the terminal.




## Design our plugin programming interface


# need other plugins to say something like
# self.signal_handler.emit("log", some_message) for normal log
# self.signal_handler.emit("log-warning", some_message) for warning log
# self.signal_handler.emit("log-error", some_message) for error log


# add
# self.signal_handler.connect("log", self.log)
# self.signal_handler.connect("log-warning", self.log_warning)
# self.signal_handler.connect("log-error", self.log_error)

# def log(self, message):
# 	print(message)
# 	
# 	
# def log_warning(self, message):
# 	print(f'WARNING: {message}')
# 	
# 	
# def log_error(self, message):
# 	print(f'ERROR: {message}')


# write 		self.signal_handler.emit("log", f"open {filename}")

# replace
# except OSError as err:
# 			# print(f'Could not open {filename}: {err}')
# 			self.signal_handler.emit("log-error", f'Could not open {filename}: {err}')
# 			return
# 		except PermissionError as err:
# 			# print(f'Could not open {filename}: {err}')			
# 			self.signal_handler.emit("log-error", f'Could not open {filename}: {err}')			
# 			return
			
# in open_file_mixin.py



# close gamma reopen 
# gamma plugins/logger/logger.py plugins/logger/commands.py /some/dummy/path.file


# open plugins/logger/logger.py
# open plugins/logger/commands.py
# ERROR: Could not open /some/dummy/path.file: [Errno 2] No such file or directory: '/some/dummy/path.file'


# try uncomment "logger.logger", from pluigns_manager and restart gamma
# nothing hurts open_file_mixin, it is independent 




# store logs in array
# self.log_array = []
# def log(self, message):
# 	print(message)
# 	self.log_array.append(message)
# 	
# def log_warning(self, message):
# 	print(f'WARNING: {message}')
# 	self.log_array.append(f'WARNING: {message}')
# 	
# def log_error(self, message):
# 	print(f'ERROR: {message}')
# 	self.log_array.append(f'ERROR: {message}')


# def show_log(self, log_type=0):
# 	print("\nlog:")
# 	
# 	if log_type == 0:
# 		for l in self.log_array:
# 			print(l)
# 	elif log_type == 1:
# 		for l in self.log_array:
# 			if l.find("WARNING:") == 0:
# 				print(l)
# 	elif log_type == 2:
# 		for l in self.log_array:
# 			if l.find("ERROR:") == 0:
# 				print(l)



# plugin.commands.append( 
# 	{
# 		"plugin-name": plugin.name,
# 		"name": "Show Log",
# 		"ref": plugin.show_log,
# 		"shortcut": "<Shift><Ctrl> + L",
# 	}
# )

# plugin.commands.append( 
# 	{
# 		"plugin-name": plugin.name,
# 		"name": "Show WARNINGS",
# 		"ref": plugin.show_log,
# 		"parameters": 1,
# 		"shortcut": "",
# 	}
# )

# plugin.commands.append( 
# 	{
# 		"plugin-name": plugin.name,
# 		"name": "Show ERRORS",
# 		"ref": plugin.show_log,
# 		"parameters": 2,
# 		"shortcut": "",
# 	}
# )


# restart gamma, press alt, type err, click on Show ERRORS



# create ui 
# open glade
# create new project
# click toplevels, select GtkWindow (save)
# save to ./plugins/logger/logger.glade
# click Display, search and select GtkTextView (save)
# right click on GtkTextView, add parent, select ScrolledWindow (save)
# select GtkWindow and set id to log_window 
# select GtkTextView and set id to log_textview (save) 

#  make sure the logger.glade looks like
# <?xml version="1.0" encoding="UTF-8"?>
# <!-- Generated with glade 3.22.1 -->
# <interface>
#   <requires lib="gtk+" version="3.20"/>
#   <object class="GtkWindow" id="log_window">
#     <property name="can_focus">False</property>
#     <property name="title" translatable="yes">Gamma Log</property>
#     <property name="default_width">600</property>
#     <property name="default_height">300</property>
#     <child>
#       <object class="GtkScrolledWindow">
#         <property name="visible">True</property>
#         <property name="can_focus">True</property>
#         <property name="shadow_type">in</property>
#         <child>
#           <object class="GtkTextView" id="log_textview">
#             <property name="visible">True</property>
#             <property name="can_focus">True</property>
#           </object>
#         </child>
#       </object>
#     </child>
#   </object>
# </interface>




# change
# def show_log(self, log_type=0):
# 	text = "\nlog:\n"

# 	if log_type == 0:
# 		for l in self.log_array:
# 			text += l + '\n'
# 	elif log_type == 1:
# 		for l in self.log_array:
# 			if l.find("WARNING:") == 0:
# 				text += l + '\n'
# 	elif log_type == 2:
# 		for l in self.log_array:
# 			if l.find("ERROR:") == 0:
# 				text += l + '\n'

# 	print(text)
# 	self.show_log_window(text)


# def show_log_window(self, text):
# 	dir_path = os.path.dirname(os.path.realpath(__file__))
# 	builder = Gtk.Builder()
# 	builder.add_from_file(f"{dir_path}/logger.glade")
# 	window = builder.get_object("log_window")
# 	textview = builder.get_object("log_textview")
# 	textview.get_buffer().set_text(text)
# 	window.set_transient_for(self.app.window)
# 	window.show_all()


# restart gamma, press shift+ctrl+L or alt and search show log

# alt again and search show errors




# add to bottom

# def show_log_window(self, text):
# 	dir_path = os.path.dirname(os.path.realpath(__file__))
# 	builder = Gtk.Builder()
# 	builder.add_from_file(f"{dir_path}/logger.glade")
# 	window = builder.get_object("log_window")
# 	log_scrolled = builder.get_object("log_scrolled_window")
# 	textview = builder.get_object("log_textview")
# 	textview.get_buffer().set_text(text)
# 	window.remove(log_scrolled)
# 	
# 	style_provider = Gtk.CssProvider()
# 	style_provider.load_from_path(f"{dir_path}/logger.css")
# 	log_scrolled.get_style_context().add_provider(
# 		style_provider,
# 		Gtk.STYLE_PROVIDER_PRIORITY_USER
# 	)
# 	
# 	textview.get_style_context().add_provider(
# 		style_provider,
# 		Gtk.STYLE_PROVIDER_PRIORITY_USER
# 	)
# 	
# 	log_scrolled.show_all()
# 	
# 	# get right side body
# 	right_side_body = self.builder.get_object("right_side_body")
# 	scrolled_sourceview = right_side_body.get_children()[0]
# 	right_side_body.remove(scrolled_sourceview)
# 	
# 	# create paned
# 	paned = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
# 	paned.pack1(scrolled_sourceview, True, False)
# 	paned.pack2(log_scrolled, False, True)
# 	paned.set_position(500)
# 			
# 	right_side_body.pack_start(paned, True, True, 0)
# 	right_side_body.show_all()
		
		






# css
#log_scrolled_window {
	# border: none;
# }

#log_textview text {
	# background: @gamma_bg_color;
	# color: @gamma_fg_color;
# }




# self.plugins["message_notify.message_notify"] \
# 											.show_message(f'ERROR: {message}', 3)


# restart gamma 
# ctrl+O
# try to open /etc/shadow
# see the message on top left



# help pages

