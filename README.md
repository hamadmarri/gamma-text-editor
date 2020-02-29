# Gamma text editor
current version 0.0.1 Beta\
Author: Hamad Al Marri


## Description 
Gamma (Γ) is a lightweight text editor. It is meant to be an alternative to Gedit or Notepad++.
Although the current implementation is tested on linux under Gnome desktop environment,
Gamma can run on Linux, Windows, and Mac if dependencies are installed
(see Dependencies section below).
Gamma uses [GTK3](https://www.gtk.org/) (cross-platform GUI toolkit) and
[PyGObject](https://pygobject.readthedocs.io/en/latest/) which is 
a Python package that provides bindings for GObject based libraries such as GTK, GStreamer,
WebKitGTK, GLib, GIO and many more.


## Why a new text editor?
-	Not cpu/ram heavy
-	No learning curve (shortcuts, difficult dealing with plugin/extensions)
-	fully customizable from A to Z
-	new UX approach for text editors
-	Made using Python for plugin developers 


## Dependencies
*	GTK+3
*	Python 3
*	gobject-introspection

If you are using Linux with a Gnome desktop, you probably have those dependencies installed already. I
am not sure if the libraries are installed for other desktops such as KDE, XFCE, or MATE. But if
you have libgtk-3-0 and python3 installed, then Gamma is probably going to work.
 


## Installation
```
git clone https://gitlab.com/hamadmarri/gamma-text-editor
cd gamma-text-editor 
chmod +x setup.sh
./setup.sh
```



## Gamma Philosophy
The philosophy of Gamma is to decouple all functionalities and features into seperate plugins.
It is designed in a way that every featuer is a plugin, even for some basic and core functionalities
such as open, save, and close files, they are made in a seperate plugins which located under 
`./plugins/files_manager` folder. However, these plugins (`openfile` and `savefile`) are highly coupled with
`files_manager` plugin since they are working togather. But nothing prevent you from replacing any of these 
coupled plugins with a different plugin with respect of taking care of integrating them togather with 
the new/replacement plugin. That being said, it is a special case where they are core basic plugins for 
Gamma to work as a text editor, therefore they are highly coupled with each other. For different types
of plugins such as a plugin for showing the terminal at bottom panel, or a plugin opens a tree view of 
a directory, there is no dependencies on other plugins. For developers, see 
[For Developers](#for-developers) section.


## Featuers and current available plugins
Here are brief descriptions about currently implemented plugins and features

### style
sets the theme style to Gamma window \
the style.css file is set in `config.py` `style-path`
 

### source_style
sets the style for the source view (text editting area) \
"style_scheme" is set in config.py \
style scheme for srource view style, usually sourceview style xml files are in \
`~/.local/share/gtksourceview-4/styles` (see `config.py`)


### window_ctrl
is responsible for handling basic window operations maximize, minimize, and quit.


### openfile
opens file(s) by showing open dialog and send filenames array\
to files_manager.open_files method

### opendir
shows open folder dialog and opens all files\
under the selected folder (recursively) and send filenames array\
to files_manager.open_files method


### savefile
saves the current file opened or all editted files\
it gets current_file from files_manager plugin\
and saves it. Message notify is sent to tell the user\
that the file is saved successfully


### files_manager
is responsible to manage all opened documents.


### simple_completion
Auto completion assistant which shows popup with words for completion\
words are collected from current opened files. 


### highlight
is responsible for highlighting the selected text by user. It\
highlights all occurrences of selected text. 


### message_notify
is responsible of displaying notification\
messages (file saved, opened file, ...)\
the default message is placed on top right corner\
default message time is 7.5 seconds, which is the time\
of a message being displayed. After this time, the message will be cleared



### search_in_file
Quick search on current opened file. It is located at\
the top of the editor. It auto scroll to first found\
match and moving to the next/previous one by UP/DOWN keywords or Enter/Shift+Enter.\
It is case sensitive. For case insensitive, see find_and_replace plugin.



### ui_manager
Deals with UI events such as changing background color for hovered element.



### codecomment2
Comments line/block of code. Auto detect the language and\
the comments symbols. The shortcut (Ctrl+/) comments/uncomment code


### find_and_replace
Find and replace text with some options such as case sensitive/insensitive,\
whole word, and replace one or replace all.


### terminal
Opens terminal on new window with cd to current directory.\
It needs to have an option to be placed in bottom panel in future.


### welcome
Shows the Welcome Page


### help
Shows help window


### about
Shows the About window


### fast_copy_cut_duplicate
Copy, cut, or duplicate a line without selecting all line. Just\
place the cursor in the line and press Ctrl+c for copy, Ctrl+x to\
cut, or Ctrl+d to duplicate. Also after copying and cutting, pressing\
Ctrl+v will paste into next line.



### typing_assistant
Auto types closing brackets and quotes while typing.




### commander
Commander is a plugin that collects all other plugins' commands\
and make it easy and fast for the user to use those commands.\
By pressing `<Alt>`, commander window is shown with search entry and\
list of commands with their key bindings. Typing in search auto filters the\
commands and the very first command is selected. When hit Enter the command runs.

Commands can be open file, close file, close all files, switch to file, zoom in,\
maximize window, find and replace ....\
basically any plugin exported its commands, commander will show theirs commands. 

Commander uses splay tree to store commands. It is a binary search tree\
with splay featuer. Search in commands is fast. Also, recent used\
commands are placed at top because of the splay operation.
  



## Screenshots

## TODO
*	Check if file got updated externally, so reload file option
*	Themes plugin (change theme, change sourceview style)
*	Open recent files
*	Open more than one window
*	Files tree view
*	Search in directory
*	Mark file with blue color when click one more click if selected
*	Arrange files in side (drag / drop)
*	Output plugin
*	Bottom panel
*	Code snippets
*	Lazy plugin manager
*	Close, min, max buttons' hover show x + -
*	Drag/drop file to editor must open file not path
*	Updater plugin
*	Abstract way to communicate with other plugins
*	Find and replace on selected area




## For Developers
If you are interested in contributin to Gamma core development or in making plugins for Gamma, then
this section is for you. Gamma is built on top of GTK3. GTK3 is a GUI platform that works on Linux,
Windows, and Mac. You have to read about GTK3 and you need to keep GTK3 documentations handy. GTK3's
main language is C, but there are many wrappers for GTK3 in different languages such as C++, Python,
javascript, Rust, and Vala. I decided to use the python wrapper which is called pygobject. Pygobject
is simpler to write, even though I am kind of a C guy, but making GUI editor with C would be time
consuming to me. That is not the only reason I chose python, the other yet very important reason
is that python make it easy to apply a plugin design where it can load modules at run time.

Anyway, you need first to understand the Gamma structure (which is not that complex), know some
basic GTK3 techniques and terminologies, for example GTK3 allows you to style your widgets (GUI components)
with CSS files. Also, GTK3 widgets can be designed in XML formats seperetly from the code and imported
at run time. Instead of writing row XML files to design your UI, you can use a tool called Glade
which is a graphical tool that allows to drag/drop widgets and set widgets' properties graphically.   

To sum up, here is the road map to start developing for Gamma:
*	Read about GTK3
	*	You do not need to learn everything in GTK3, just an overview what GTK3 can do. [GTK](https://www.gtk.org/)
	*	Read about GTK basics, widgets, windows, layout... [GTK+ 3 Reference Manual](https://developer.gnome.org/gtk3/3.24/) 
	*	Read about how is the styling with GTK3 
		*	[GTK+ CSS Overview](https://developer.gnome.org/gtk3/stable/chap-css-overview.html)
		*	[GTK+ CSS Properties](https://developer.gnome.org/gtk3/stable/chap-css-properties.html)


