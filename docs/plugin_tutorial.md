# Plugin Tutorial

-	[Introduction](#introduction)
-	[Copy form the template](#copy-form-the-template)
-	[Author, Name of the plugin, and Remove unwanted comments and methods](#author-name-of-the-plugin-and-remove-unwanted-comments-and-methods)
-	[Add logger to plugins_array in plugins_manager](#add-logger-to-plugins_array-in-plugins_manager)
-	[Test our plugin](#test-our-plugin)
-	[Export our commands to the commander](#export-our-commands-to-the-commander)
-	[Design our plugin programming interface](#design-our-plugin-programming-interface)
-	[Store logs in array](#store-logs-in-array)
-	[Create the UI for logger window](#create-the-ui-for-logger-window)
-	[Add logger to the bottom of the editor](#add-logger-to-the-bottom-of-the-editor)
-	[Apply .css style to logger widgets](#apply-css-style-to-logger-widgets)
-	[Use other plugins in Logger](#use-other-plugins-in-logger)
-	[Add Help pages for Logger](#add-help-pages-for-logger)


## Introduction
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

**Note: Do not change the plugin class name, it should be called `class Plugin`.**


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
For logging process, a nice way to log thigs is to emit a signal for logging.
Let's say that other plugins can do something like
-	`self.signal_handler.emit("log", some_message) # for normal log`
-	`self.signal_handler.emit("log-warning", some_message) # for warning log`
-	`self.signal_handler.emit("log-error", some_message) # for error log`

To connect our logger to these signals, add the following in the `__init__` method
```
self.signal_handler.connect("log", self.log)
self.signal_handler.connect("log-warning", self.log_warning)
self.signal_handler.connect("log-error", self.log_error)
```
We connected/listened to `log`, `log-warning`, and `log-error` signals and connected each 
to corresponding local method. Next, create the methods:
```
def log(self, message):
	print(message)
 	
def log_warning(self, message):
	print(f'WARNING: {message}')

def log_error(self, message):
	print(f'ERROR: {message}')
```

Now let's use this logging signals when opening new file. Open `./plugins/files_manager/open_file_mixin.py`,
write `self.signal_handler.emit("log", f"open {filename}")` to the end of `open_file` method. And apply
the changes in the try bock when cannot open a file instead of printing to console, we emit log-error message:
```
except OSError as err:
	# print(f'Could not open {filename}: {err}')
	self.signal_handler.emit("log-error", f'Could not open {filename}: {err}')
	return
except PermissionError as err:
	# print(f'Could not open {filename}: {err}')			
	self.signal_handler.emit("log-error", f'Could not open {filename}: {err}')			
	return
```

Close gamma open again with:
```
gamma plugins/logger/logger.py plugins/logger/commands.py /some/non-existed/path.file
```
See printed log in the terminal:
```
open plugins/logger/logger.py
open plugins/logger/commands.py
ERROR: Could not open /some/non-existed/path.file: [Errno 2] No such file or directory: '/some/non-existed/path.file'
```

Now, try comment out `logger.logger` from `pluigns_manager` and restart Gamma.
Nothing hurts `open_file_mixin` when disabling `logger.logger`, it is independent.

Uncomment `logger.logger` back to enable it.




## Store logs in array
Instead of just printing the log out to the terminal, let's keep it in an array and use that array when needed.
Add `self.log_array = []` to the end of `__init__` method. Edit `log`, `log_warning`, and `log_error` methods:
```
def log(self, message):
	print(message)
 	self.log_array.append(message)
 	
def log_warning(self, message):
	print(f'WARNING: {message}')
 	self.log_array.append(f'WARNING: {message}')
 	
def log_error(self, message):
 	print(f'ERROR: {message}')
 	self.log_array.append(f'ERROR: {message}')
```
After printing the log action, we store the message to `log_array`.
Now, let's make `show_log` method prints all stored logs. We will add a parameter `log_type` to `show_log`
which is used to know what type of log will be printed (0: all logs, 1: warning logs, and 2: errors).
```
def show_log(self, log_type=0):
	print("\nlog:")
 	
	if log_type == 0:
 		for l in self.log_array:
 			print(l)
 	elif log_type == 1:
 		for l in self.log_array:
 			if l.find("WARNING:") == 0:
 				print(l)
 	elif log_type == 2:
 		for l in self.log_array:
 			if l.find("ERROR:") == 0:
 				print(l)
```
Since we changed the `show_log` method, we need to update our commands. Open `./plugins/logger/commands.py`
and apply the changes below:
```
plugin.commands.append( 
 	{
 		"plugin-name": plugin.name,
 		"name": "Show Log",
 		"ref": plugin.show_log,
 		"shortcut": "<Shift><Ctrl> + L",
 	}
)

plugin.commands.append( 
 	{
 		"plugin-name": plugin.name,
 		"name": "Show WARNINGS",
 		"ref": plugin.show_log,
 		"parameters": 1,
 		"shortcut": "",
 	}
)

plugin.commands.append( 
 	{
 		"plugin-name": plugin.name,
 		"name": "Show ERRORS",
 		"ref": plugin.show_log,
 		"parameters": 2,
 		"shortcut": "",
 	}
)
```
We do not have to pass a parameter to the `Show Log` command since the default is `0`. We passed
parameter `1` to `Show WARNINGS`, and `2` to `Show ERRORS`. Notices that it is ok to not write a shortcut
for a command because `Show WARNINGS` and `Show ERRORS` have no shortcuts but can be called via commander window.

Restart Gamma, press Alt, type err, click on Show ERRORS.



## Create the UI for logger window
-	Open Glade
-	Create new project
-	Click `toplevels`, select `GtkWindow` (click save)
	-	save to `./plugins/logger/logger.glade`
-	Click `Display`, search and select `GtkTextView` (click save)
-	Right click on `GtkTextView`, add parent, select `ScrolledWindow` (click save)
-	Select `GtkWindow` and set `id` to `log_window`
-	Select `GtkScrolledWindow` and set `id` to `log_scrolled_window`
-	Select `GtkTextView` and set `id` to `log_textview` (click save)

Sometimes when not saving after adding a widget the rest actions will not work.
That's why I recommend after each widget addition.
Make sure the `logger.glade` looks like the xml below:
```
<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.22.1 -->
<interface>
   <requires lib="gtk+" version="3.20"/>
   <object class="GtkWindow" id="log_window">
     <property name="can_focus">False</property>
     <property name="title" translatable="yes">Gamma Log</property>
     <property name="default_width">600</property>
     <property name="default_height">300</property>
     <child>
       <object class="GtkScrolledWindow">
         <property name="visible">True</property>
         <property name="can_focus">True</property>
         <property name="shadow_type">in</property>
         <child>
           <object class="GtkTextView" id="log_textview">
             <property name="visible">True</property>
             <property name="can_focus">True</property>
           </object>
         </child>
       </object>
     </child>
   </object>
</interface>
```

Import the `os` library at the top of `logger.py` (`import os`). Apply the following changes in `show_log` method:
```
def show_log(self, log_type=0):
 	text = "\nlog:\n"

 	if log_type == 0:
 		for l in self.log_array:
 			text += l + '\n'
 	elif log_type == 1:
 		for l in self.log_array:
 			if l.find("WARNING:") == 0:
 				text += l + '\n'
 	elif log_type == 2:
 		for l in self.log_array:
 			if l.find("ERROR:") == 0:
 				text += l + '\n'

 	print(text)
 	self.show_log_window(text)
```

Add `show_log_window` method below:
```
def show_log_window(self, text):
	# get current file's directory path
 	dir_path = os.path.dirname(os.path.realpath(__file__))
 	
 	# create new GtkBuilder
 	builder = Gtk.Builder()
 	
 	# load the UI glade file we have just created to the builder
 	builder.add_from_file(f"{dir_path}/logger.glade")
 	
 	# get the window "log_window" from .glade file
 	window = builder.get_object("log_window")
 	 	
 	# get the window "log_textview" from .glade file
 	textview = builder.get_object("log_textview")
 	
 	# set the text in GtkTextView to "text"
 	textview.get_buffer().set_text(text)
 	
 	# make the log window as transient for the main app window
 	# i.e. always at top
 	window.set_transient_for(self.app.window)
 	
 	# show log window and its all children
 	window.show_all()
```

Restart Gamma, press shift+ctrl+L or Alt and search show log to see the log window. Close log window and 
press Alt again and search show errors.



## Add logger to the bottom of the editor
Instead of opening new window to show the log, we will add it to the bottom of the Gamma editor.
This is done by:
-	Detaching/remove `log_scrolled` from `log_window`
-	Get the `right_side_body` widget (GtkBox) from our main window/builder
-	Detaching/remove `scrolled_sourceview` (has the GtkSourceview as child) from `right_side_body`
-	Create a `Gtk.Paned` (which allow to add two children widgets and adjust their size)
-	Add `scrolled_sourceview` and `log_scrolled` to the `paned`
-	Add the `paned` to `right_side_body`

Apply the changes below to `show_log_window` method: 
```
def show_log_window(self, text):
 	dir_path = os.path.dirname(os.path.realpath(__file__))
 	builder = Gtk.Builder()
 	builder.add_from_file(f"{dir_path}/logger.glade")
 	window = builder.get_object("log_window")
 	log_scrolled = builder.get_object("log_scrolled_window")
 	textview = builder.get_object("log_textview")
 	textview.get_buffer().set_text(text)
 	
 	window.remove(log_scrolled) 	 	
 	log_scrolled.show_all()
 	
 	# get right side body
 	right_side_body = self.builder.get_object("right_side_body")
 	scrolled_sourceview = right_side_body.get_children()[0]
 	right_side_body.remove(scrolled_sourceview)
 	
 	# create paned
 	paned = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
 	paned.pack1(scrolled_sourceview, True, False)
 	paned.pack2(log_scrolled, False, True)
 	paned.set_position(500)
 			
 	right_side_body.pack_start(paned, True, True, 0)
 	right_side_body.show_all()
```

Restart Gamma, press shift+ctrl+L or Alt and search show log to see the log at the bottom.



## Apply .css style to logger widgets
Create a new `.css` file by pressing `Ctrl+N`. Save the file to `./plugins/logger/logger.css`.
Write the following `css` code to `logger.css`:
```
#log_scrolled_window {
	border: none;
}

#log_textview text {
	background: @gamma_bg_color;
	color: @gamma_fg_color;
}
```
The `@gamma_bg_color` and `@gamma_fg_color` are defined colors in `chocolate-icecream-solid.css`, so
make sure that the current Gamma style selected is `chocolate-icecream-solid.css`. Or,
change `background` and `color` to your favourite colors.

Make sure that in `logger.glade` you have set `Widget Name` for each widget. Open `Glade`, open 
`logger.glade` files. Select `log_window`, click on `Common`, write `log_window` in the `Widget Name` field.
Apply this to both `log_scrolled_window` and `log_textview` write their ids in `Widget Name`.

The `Widget Name` is the name that is accessible as `id` to `.css` file. To use `#log_textview` id in `.css`, you 
neet to have the `Widget Name` of the `GtkTextView` widget set to `log_textview`. Notice that you can also add style
classes in Glade.


To apply the `./plugins/logger/logger.css` to our logger widgets add the following to `show_log_window` method:
```
style_provider = Gtk.CssProvider()
style_provider.load_from_path(f"{dir_path}/logger.css")
log_scrolled.get_style_context().add_provider(
	style_provider,
	Gtk.STYLE_PROVIDER_PRIORITY_USER
)

textview.get_style_context().add_provider(
	style_provider,
	Gtk.STYLE_PROVIDER_PRIORITY_USER
)
```

The `show_log_window` method will look like:
```
def show_log_window(self, text):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	builder = Gtk.Builder()
	builder.add_from_file(f"{dir_path}/logger.glade")
	window = builder.get_object("log_window")
	log_scrolled = builder.get_object("log_scrolled_window")
	textview = builder.get_object("log_textview")
	textview.get_buffer().set_text(text)
	window.remove(log_scrolled)
	
	style_provider = Gtk.CssProvider()
	style_provider.load_from_path(f"{dir_path}/logger.css")
	log_scrolled.get_style_context().add_provider(
		style_provider,
		Gtk.STYLE_PROVIDER_PRIORITY_USER
	)
	
	textview.get_style_context().add_provider(
		style_provider,
		Gtk.STYLE_PROVIDER_PRIORITY_USER
	)
	
	log_scrolled.show_all()
	
	# get right side body
	right_side_body = self.builder.get_object("right_side_body")
	scrolled_sourceview = right_side_body.get_children()[0]
	right_side_body.remove(scrolled_sourceview)
	
	# create paned
	paned = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
	paned.pack1(scrolled_sourceview, True, False)
	paned.pack2(log_scrolled, False, True)
	paned.set_position(500)
			
	right_side_body.pack_start(paned, True, True, 0)
	right_side_body.show_all()
```

Restart Gamma, press shift+ctrl+L or Alt and search show log to see the log at the bottom with applied style.



## Use other plugins in Logger
Let's use the `message_notify` plugin to show an error message when cannot open a file.
Add the following line in `log_error` method.
```
self.plugins["message_notify.message_notify"] \
											.show_message(f'ERROR: {message}', 3)
```
Make sure you have a reference to `app.plugins_manager.plugins` in your `__init__` method.
```
self.plugins = app.plugins_manager.plugins
```

Restart Gamma, press `Ctrl+O`, and try to open `/etc/shadow`. See the message on top right.



## Add Help pages for Logger
Gamma uses [Yelp](https://wiki.gnome.org/Apps/Yelp/) for help display. For the pages formate,
Gamma uses [Mallard](http://projectmallard.org/).

Add these two files to `./plugins/help`:

`./plugins/help/logger_plugin.page`
```
<page xmlns="http://projectmallard.org/1.0/"
      type="guide"
      id="logger_plugin">
<info>
  <link type="guide" xref="plugins"/>
</info>
<title>Logger Plugin</title>
<p>Displays logs in both console and bottom panel</p>

<p>Plugin: <code>logger</code></p>
</page>
```


`./plugins/help/logger_shortcuts.page`
```
<page xmlns="http://projectmallard.org/1.0/"
      type="topic"
      id="logger_shortcut">
<info>
  <link type="guide" xref="shortcuts"/>
  <link type="guide" xref="logger_plugin"/>
</info>
<title>Logger Shortcuts</title>
<table shade="rows" frame="all" rules="rows cols">
  <tr>
    <td><p>Show Log</p></td> <td><code>Shift + Ctrl + L</code></td>
  </tr>
</table>
<p>Plugin: <code>logger</code></p>
</page>
```




