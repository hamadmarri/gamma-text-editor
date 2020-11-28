# How to contribute to Gamma Text Editor

If you are interested in contributing to Gamma core development or in making plugins for Gamma, then
this section is for you. Gamma is built on top of GTK3. GTK3 is a GUI library that works on Linux,
Windows, and Mac. You have to read about GTK3 and you need to keep GTK3 documentations handy. GTK3's
main language is C, but there are many wrappers for GTK3 in different languages such as C++, Python,
javascript, Rust, and Vala. I decided to use the python wrapper which is called pygobject. Pygobject
is simpler to write, even though I am kind of a C guy, but making GUI editor with C would be time
consuming to me. That is not the only reason I chose python, the other yet very important reason
is that python makes it easy to apply a plugin design where it can load modules at run time.

Anyway, you need first to understand the Gamma structure (which is not that complex), know some
basic GTK3 techniques and terminologies, for example GTK3 allows you to style your widgets (GUI components)
with CSS files. Also, the layout of GTK3 widgets can be designed in XML formats seperetly from the code and imported
at run time. Instead of writing raw XML files to design your UI, you can use a tool called Glade
which is a graphical tool that allows to drag/drop widgets and set widgets' properties graphically.   

To sum up, here is the road map to start developing for Gamma:
*	Read about GTK3
	*	You do not need to learn everything in GTK3, just an overview of what GTK3 can do ( [GTK](https://www.gtk.org/) ).
	*	Read about GTK basics, widgets, windows, layout... [GTK+ 3 Reference Manual](https://developer.gnome.org/gtk3/3.24/)
	*	See [Devhelp](https://wiki.gnome.org/Apps/Devhelp)
	*	See [gtk3-demo](https://developer.gnome.org/gtk3/stable/gtk3-demo.html)
	*	See [Interactive debugging](https://developer.gnome.org/gtk3/stable/gtk-running.html) 
	*	Read about how is the styling with GTK3 
		*	[GTK+ CSS Overview](https://developer.gnome.org/gtk3/stable/chap-css-overview.html)
		*	[GTK+ CSS Properties](https://developer.gnome.org/gtk3/stable/chap-css-properties.html)
	* See [Glade](https://glade.gnome.org/) and [Glade Tutorials](https://wiki.gnome.org/action/show/Apps/Glade/Tutorials?action=show&redirect=Glade%2FTutorials)
*	Read about [The Python GTK+ 3 Tutorial](https://python-gtk-3-tutorial.readthedocs.io/en/latest/index.html)
	*	[PyGObject API Reference ](https://lazka.github.io/pgi-docs/)
*	Learn the structure of Gamma and how to write a plugin 
	*	Soon I will write a tutorial of making a plugin that deals with:
		*	Getting input or information from Gamma editor
		*	Getting input or information from other plugins
		*	Designing UI layout using Glade
		*	Writing css for plugin widgets
		*	Output back to the editor
		*	Changing the main layout of Gamma (example, inserting a bottom panel)
		*	Using other plugins features
		*	Listening to GTK signals
		*	Creating signals to your plugin 
		*	Listening to other plugins signals
		*	The idea of the plugin would be a logger which logs every action\
			and outputs the log in bottom panel (the bottom panel would be a seperate plugin)
	
-	See [Gamma Structure](https://gitlab.com/hamadmarri/gamma-text-editor/-/wikis/Gamma-Structure)
-	See [Plugin Tutorial](https://gitlab.com/hamadmarri/gamma-text-editor/-/wikis/Plugin-Tutorial)
