
import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk



class FilesUI(object):


	def rename_file(self, file_object):
		box = file_object.ui_ref
		btnName = box.get_children()[0]

		# set the text of button to filename
		basename = os.path.basename(file_object.filename)
		btnName.set_label(basename)

		# get the label of the button, and set left padding to 0
		btnName.get_children()[0].set_xalign(0)

		# set headerbar text to the filename
		current_file = self.THE("files_manager", "get_current_file", {})
		if current_file:
			self.update_header(current_file.filename)



	# adds ui button with filename label in toolbar_file
	# (the left side panel)
	def add_filename_to_ui(self, newfile):

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
		btnName.connect("clicked", self.side_file_clicked, box, newfile)

		# connect clicked signal to close method
		btnClose.connect("clicked", self.close_file_clicked, box, newfile)

		btnName.connect("enter_notify_event", self.enter_notify_event)
		btnName.connect("leave_notify_event", self.leave_notify_event)

		btnClose.connect("enter_notify_event", self.enter_notify_event)
		btnClose.connect("leave_notify_event", self.leave_notify_event)

		btnName.connect("motion_notify_event", self.mouse_move)
		btnName.connect("button-press-event", self.drag_begin)
		btnName.connect("button-release-event", self.drag_end)


	# drag file to reorder
	def mouse_move(self, w, e):
		i = -1
		w_height = w.get_parent().get_allocated_height()
		top_level = w.get_toplevel()

		(x, y) = w.translate_coordinates(top_level, 0 ,0 )
		dragging_pos = y + e.y

		children = self.toolbar_files.get_children()
		for c in children:
			i += 1

			if c == w.get_parent():
				continue

			(x2, y2) = c.translate_coordinates(top_level, 0 ,0 )
			if dragging_pos >= y2 and dragging_pos <= y2 + w_height:
				self.toolbar_files.reorder_child(w.get_parent(), i)


	def drag_begin(self, w, e):
		cursor = Gdk.Cursor.new_from_name(Gdk.Display.get_default(), "grab")
		self.app.window.get_window().set_cursor(cursor)

	def drag_end(self, w, e):
		cursor = Gdk.Cursor(Gdk.CursorType.ARROW)
		self.app.window.get_window().set_cursor(cursor)


	def enter_notify_event(self, widget, event):
		widget.get_parent().get_style_context().add_class("openned_file_hover")


	def leave_notify_event(self, widget, event):
		widget.get_parent().get_style_context().remove_class("openned_file_hover")



	# handler of "clicked" event
	# it switch the view to the filename in clicked button
	def side_file_clicked(self, btn, box, newfile):
		self.THE("files_manager", "side_file_clicked", {"filename": newfile.filename})



	def close_file_clicked(self, btn, box, newfile):
		self.THE("files_manager", "close_file", {"filename": newfile.filename})




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
	def update_header(self, filename, editted=False):
		# get headerbar widget reference, to show current filename
		# in headerbar label
		headerbar = self.app.builder.get_object("headerbarMain")

		# gets basename of the file, not the full path
		basename = os.path.basename(filename)

		if editted:
			headerbar.get_style_context().add_class("openned_file_editted")
			# set the edited title of headerbar
			headerbar.set_title("*" + basename)
		else:
			headerbar.get_style_context().remove_class("openned_file_editted")
			# set the title of headerbar
			headerbar.set_title(basename)




	# updates the headerbar by filename
	def set_header(self, text):
		# get headerbar widget reference, to show current filename
		# in headerbar label
		headerbar = self.app.builder.get_object("headerbarMain")

		# set the title of headerbar
		headerbar.set_title(text)




	def replace_sourceview_widget(self, newsource):

		# scrolledwindow is object that contains sourceviews
		# basically, a new opened file has its own sourceview
		# and got added to scrolledwindow
		# previouse sourceview got removed from scrolledwindow
		scrolledwindow = self.app.builder.get_object("source_scrolledwindow")
		scroll_and_source_and_map_box = self.app.builder.get_object("scroll_and_source_and_map_box")


		# remove old source map
		old_sourcemap = scroll_and_source_and_map_box.get_children()[1]
		if old_sourcemap:
			scroll_and_source_and_map_box.remove(old_sourcemap)

		# remove previously displayed sourceview
		prev_child = scrolledwindow.get_child()
		if prev_child:
			scrolledwindow.remove(prev_child)

		# add the newsource view
		scrolledwindow.add(newsource)

		# the order of set_view for sourcemap is very important
		# when move this line below/after pack_start, sometimes
		# it crashes when open files which have no \n at the end!!
		newsource.sourcemap.set_view(newsource)
		scroll_and_source_and_map_box.pack_start(newsource.sourcemap, False, True, 0)

		# place the cursor in it
		newsource.grab_focus()





	def set_editted(self, box):
		# get headerbar widget reference, to show current filename
		# in headerbar label
		headerbar = self.app.builder.get_object("headerbarMain")

		box.get_style_context().add_class("openned_file_editted")
		headerbar.get_style_context().add_class("openned_file_editted")
		headerbar.set_title("*" + headerbar.get_title())


	def reset_editted(self, box):
		# get headerbar widget reference, to show current filename
		# in headerbar label
		headerbar = self.app.builder.get_object("headerbarMain")

		box.get_style_context().remove_class("openned_file_editted")
		headerbar.get_style_context().remove_class("openned_file_editted")
		self.update_header(box.file.filename)
