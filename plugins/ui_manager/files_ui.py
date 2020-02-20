



import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk	



class FilesUI(object):
	

	# adds ui button with filename label in toolbar_file
	# (the left side panel)
	def add_filename_to_ui(self, newfile):
	
		# create event box to detect hover signal on box
		# eventBox = Gtk.EventBox()
		
		# create box for both filename and close btn 
		box = Gtk.Box(Gtk.Orientation.HORIZONTAL, 0)
				
		# create new buttons for filename and close btn
		btnName = Gtk.Button()
		btnClose = Gtk.Button()
		
		# associate box widget to File object
		newfile.ui_ref = box
		
		# set the text of button to filename
		basename = os.path.basename(newfile.filename)
		btnName.set_label(basename)

		# bind newfile to box
		box.file = newfile
		
		# set the text of close btn
		btnClose.set_label("x")
		
		# get the label of the button, and set left padding to 0
		lbl = btnName.get_children()[0]
		lbl.set_xalign(0)
		
		# add file name to the left
		box.pack_start(btnName, True, True, 0)
		
		# add close btn to the right
		box.pack_end(btnClose, False, False, 0)
		
		
		# add button to toolbar_files
		# (read: https://developer.gnome.org/gtk3/stable/GtkBox.html#gtk-box-pack-start)
		self.toolbar_files.pack_start(box, False, False, 0)
		
		# position new opened file's button to top of toolbar_files
		# (read: https://developer.gnome.org/gtk3/unstable/GtkBox.html#gtk-box-reorder-child)
		self.toolbar_files.reorder_child(box, 0)
		
		# add css styling classes
		self.add_css_classes(box, btnName, btnClose)
		
		# connect all signals
		self.connect_signals(box, btnName, btnClose, newfile)
		
		# show the widgets
		box.show_all()
		
		
		
	
	def add_css_classes(self, box, btnName, btnClose):
		# set the ui/css class to the box (.openned_file)
		box.get_style_context().add_class("openned_file")
		btnClose.get_style_context().add_class("close_btn")

	
		
	def connect_signals(self, box, btnName, btnClose, newfile):
		# connect clicked signal to side_file_clicked method		
		btnName.connect("clicked", self.side_file_clicked, box, newfile.filename)
		
		# connect clicked signal to close method		
		btnClose.connect("clicked", self.close_file_clicked, box, newfile.filename)
		
		btnName.connect("enter_notify_event", self.enter_notify_event)
		btnName.connect("leave_notify_event", self.leave_notify_event)
		
		btnClose.connect("enter_notify_event", self.enter_notify_event)
		btnClose.connect("leave_notify_event", self.leave_notify_event)
		
		
		
	def enter_notify_event(self, widget, event):
		#print("enter", widget)
		widget.get_parent().get_style_context().add_class("openned_file_hover")
		
	
	def leave_notify_event(self, widget, event):
		#print("leave", widget)
		widget.get_parent().get_style_context().remove_class("openned_file_hover")
		
				
		
	# handler of "clicked" event
	# it switch the view to the filename in clicked button
	def side_file_clicked(self, btn, box, filename):
		self.set_currently_displayed(box)	
		self.plugins["files_manager.files_manager"].side_file_clicked(filename)
		
		
		
	def close_file_clicked(self, btn, box, filename):
		self.set_currently_displayed(box)
		self.plugins["files_manager.files_manager"].side_file_clicked(filename)
		self.plugins["files_manager.files_manager"].close_current_file()
				
		
		
	def set_currently_displayed(self, box):
		boxes = self.toolbar_files.get_children()
		
		# if only one file, dont highlight
		if len(boxes) == 1:
			return
		
		# remove current displayed class
		for b in boxes:
			b.get_style_context().remove_class("openned_file_current_displayed")
		
		box.get_style_context().add_class("openned_file_current_displayed")
		
		
	
	# updates the headerbar by filename
	def update_header(self, filename):		
		# gets basename of the file, not the full path
		basename = os.path.basename(filename)
		
		# set the title of headerbar
		self.headerbar.set_title(basename)
		
		# show message of the full path of the file 
		# it is useful to avoid confusion when having 
		# different files with similar names in different paths
		self.plugins["message_notify.message_notify"].show_message(filename)
		

	
	
	# updates the headerbar by filename
	def set_header(self, text):
		# set the title of headerbar
		self.headerbar.set_title(text)




	def replace_sourceview_widget(self, newsource):
		# remove previously displayed sourceview
		# DEBUG: print("scrolledwindow.remove before")
		prev_child = self.scrolledwindow.get_child()
		# DEBUG: print(prev_child)
		if prev_child:
			self.scrolledwindow.remove(prev_child)
		# DEBUG: print("scrolledwindow.remove")
		
		# add the newsource view
		self.scrolledwindow.add(newsource)
		# DEBUG: print("scrolledwindow.add")
		
		# place the cursor in it
		newsource.grab_focus()
		
		# need to update the mini map too
		self.sourceview_manager.update_sourcemap(newsource)
		# DEBUG: print("sourceview_manager.update_sourcemap")
