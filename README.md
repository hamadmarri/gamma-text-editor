# Gamma text editor
Current version 0.0.4\
Author: Hamad Al Marri

-	[Description](#description)
-	[Screenshots](#screenshots)
-	[Why a new text editor?](#why-a-new-text-editor)
-	[Dependencies](#dependencies)
-	[Installation](#installation)
-	[Gamma Philosophy](#gamma-philosophy)
-	[Features and current available plugins](#features-and-current-available-plugins)
-	[TODO](#todo)
-	[For Developers](https://gitlab.com/hamadmarri/gamma-text-editor/-/wikis/For-Developers)
-	[Wiki](https://gitlab.com/hamadmarri/gamma-text-editor/-/wikis/home)


## Description 
Gamma (Γ) is a lightweight text editor. It is meant to be an alternative to Gedit or Notepad++.
Although the current implementation is tested on linux under Gnome desktop environment,
Gamma can run on Linux, Windows, and Mac if dependencies are installed
(see [Dependencies](#dependencies) section below).
Gamma uses [GTK3](https://www.gtk.org/) (cross-platform GUI toolkit) and
[PyGObject](https://pygobject.readthedocs.io/en/latest/) which is 
a Python package that provides bindings for GObject based libraries such as GTK, GStreamer,
WebKitGTK, GLib, GIO and many more.



## Screenshots
![s1](https://gitlab.com/hamadmarri/gamma-text-editor/uploads/ef0364ca533bbed7febab7a7e2462619/Screenshot_from_2020-03-01_01-53-52.png)

![s2](https://gitlab.com/hamadmarri/gamma-text-editor/uploads/232c19c6af148fc6a83ea55fdacace69/Screenshot_from_2020-03-01_02-28-21.png)

![s3](https://gitlab.com/hamadmarri/gamma-text-editor/uploads/a3a9328a78918aa4415c9355274adb5a/Screenshot_from_2020-03-01_02-01-59.png)

![Screenshot_from_2020-11-26_03-53-53](https://gitlab.com/hamadmarri/gamma-text-editor/uploads/6a14366e46305c4bb051c8a4ca6004b2/Screenshot_from_2020-11-26_03-53-53.png)

![blackleaf](https://gitlab.com/hamadmarri/gamma-text-editor/uploads/7d840c1177f05017bba5207d479fef8c/blackleaf-scrn.png)

[More Screenshots](https://gitlab.com/hamadmarri/gamma-text-editor/-/wikis/Screenshots)



## Why a new text editor?
-	Lightweight, not CPU/RAM hungry
-	No learning curve (easy/familiar shortcuts, easy use of plugin/extensions)
-	Fully customizable from A to Z (even the UI layout)
-	New UX approach for text editors
-	Easy plugin system
-	Made using Python for python contributors


## Dependencies
*	GTK+3
*	GtkSourceview 4 (works for 3.0 but currently need to manually change the version in python files)
*	Python 3
*	gobject-introspection

If you are using Linux with a Gnome desktop, you probably have those dependencies installed already. I
am not sure if the libraries are installed for other desktops such as KDE, XFCE, or MATE. But if
you have libgtk-3-0 and python3 installed, then Gamma is probably going to work.

You might need to install the following (in case of missing dependencies):
```
gobject-introspection
python3-gobject
typelib-1_0-Gtk-3_0
typelib-1_0-GtkSource-4

// for help pages
typelib-1_0-WebKit2-4_0
yelp

// for terminal plugin
typelib-1_0-Vte-2.91 
gedit-plugin-terminal

// for ctags plugin
ctags
```

You might find this usefull: https://pygobject.readthedocs.io/en/latest/getting_started.html

### Install dependencies on OpenSuse
Usually these dependencies are already installed on Opensuse, but in case some are missing:
```
sudo zypper in libgtk-3-0 python3-gobject python3-gobject-Gdk python3-gobject-cairo typelib-1_0-Gtk-3_0 libgtksourceview-4-0 typelib-1_0-GtkSource-4 typelib-1_0-WebKit2-4_0 yelp libvte-2_91-0 vte-devel typelib-1_0-Vte-2.91 ctags
```

If no python3, try install the latest python3. In my case, python38 (i.e. 3.8)
```
sudo zypper in python38
```


### Install dependencies on Debian
```
sudo apt install python3 libgtk-3-0 gobject-introspection libgtksourceview-4-0 libgtksourceview-4-dev python3-gi (>= 3.0) python3-gi-cairo (>= 3.0) gir1.2-glib-2.0 gir1.2-gtk-3.0 gir1.2-gtksource-4 gir1.2-pango-1.0 gir1.2-vte-2.91 ctags gir1.2-webkit2-4.0 yelp

```


## Installation

### Git Installation (Recommended)
```
git clone https://gitlab.com/hamadmarri/gamma-text-editor
cd gamma-text-editor 
chmod +x setup.sh
./setup.sh
```

### OpenSUSE
[OpenSUSE package (.rpm)](https://gitlab.com/hamadmarri/gamma-text-editor/-/raw/opensuse/rpmbuild/RPMS/x86_64/gamma-text-editor-0.0.4-0.x86_64.rpm?inline=false)

### Debian
[Debian package (.deb)](https://gitlab.com/hamadmarri/gamma-text-editor/-/raw/debian/deb/gamma-text-editor_0.0.4_amd64.deb?inline=false)


## Run Gamma
Gamma will be visible in your applications list after installation (launcher) - click to open.
If you need to run Gamma via terminal:
```
# run Gamma
$ gamma-editor

# edit file/s with Gamma
$ gamma-editor /path/to/file1 ./file2

# edit file/s with Root privilege (use EDITOR=gamma-editor sudoedit). Example:
$ EDITOR=gamma-editor sudoedit /etc/X11/xorg.conf.d/70-synaptics.conf
```

## Gamma Philosophy
The philosophy of Gamma is to decouple all functionalities and features into separate plugins.
It is designed in a way that every feature is a plugin, even for some basic and core functionalities
such as open, save, and close files, they are made in a separate plugins which located under 
`./plugins/files_manager` folder. However, these plugins (`openfile` and `savefile`) are highly coupled with
`files_manager` plugin since they are working together. But nothing prevents you from replacing any of these 
coupled plugins with a different plugin with respect of taking care of integrating them together with 
the new/replacement plugin. That being said, it is a special case where they are core basic plugins for 
Gamma to work as a text editor, therefore they are highly coupled with each other. For different types
of plugins such as a plugin for showing the terminal at bottom panel, or a plugin opens a tree view of 
a directory, there is no dependencies on other plugins. For developers, see 
[For Developers](#for-developers) section.


## Features and current available plugins
Here are brief descriptions about currently implemented plugins and features

### style
Sets the theme style to Gamma window \
the `style.css` file is set in `config.py` `style-path`
 

### source_style
Sets the style for the source view (text editting area) \
`style_scheme` is set in `config.py` \
style scheme for srource view style, usually sourceview style xml files are in \
`~/.local/share/gtksourceview-4/styles` (see `config.py`)


### window_ctrl
Is responsible for handling basic window operations maximize, minimize, and quit.


### openfile
Opens file(s) by showing open dialog and send filenames array\
to files_manager.open_files method

### opendir
Shows open folder dialog and opens all files\
under the selected folder (recursively) and send filenames array\
to files_manager.open_files method


### savefile
Saves the current file opened or all edited files\
it gets current_file from files_manager plugin\
and saves it. Message notify is sent to tell the user\
that the file is saved successfully


### files_manager
Is responsible to manage all opened documents.


### simple_completion
Auto completion assistant which shows popup with words for completion\
words are collected from current opened files. 


### highlight
Is responsible for highlighting the selected text by user. It\
highlights all occurrences of selected text. 


### message_notify
Is responsible of displaying notification\
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



### codecomment
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
with splay feature. Search in commands is fast. Also, recent used\
commands are placed at top because of the splay operation.
  



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

For all issues/todos [Issues](https://gitlab.com/hamadmarri/gamma-text-editor/issues).

## Contacts
Telegram Channel: https://t.me/gamma_text_editor

## Donate
* BTC: 19FBeR6TAABYTAPALWggTU6f8Nou6hrYfY
* Paypal: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=8F7F4D8BKR8XC
