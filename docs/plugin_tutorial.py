# Plugin Tutorial

## Copy template

## Author, name of the plugin, remove unwanted comments and methods

## Add logger to plugins_array in plugins_manager


## remove 		self.handlers = app.signal_handler.handlers  since no need to handle signals from gtk other than keypress
# def set_handlers(self):
# 		pass


## uncomment self.signal_handler.key_bindings_to_plugins.append(self) <-- if need key_bindings


## add 
# def key_bindings(self, event, keyval_name, ctrl, alt, shift):
# 		if shift and ctrl and keyval_name == "L":
# 			print("logger") 


## comment commands.py and 
# commands.set_commands(self)


# close gamma and run from command line
# gamma
# hold shift and ctrl and press 'L'
# logger is printed

# close and reopen gamma again 
# gamma plugins/logger/logger.py plugins/logger/commands.py



# uncomment 
# commands.set_commands(self)

# change to
# if shift and ctrl and keyval_name == "L":
# 			self.show_log()



# create
# def show_log(self):
# 		print("logger")



# create 
# def set_commands(plugin):
# 	plugin.commands.append( 
# 		{
# 			"plugin-name": plugin.name,
# 			"name": "Show Log",
# 			"ref": plugin.show_log,
# 			"shortcut": "<Shift><Ctrl> + L",
# 		}
# 	)


# close gamma and reopen again
# press Alt type show log



# designa the API interface
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




