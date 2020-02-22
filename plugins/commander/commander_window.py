
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from .list_functions import ListFunctionsMixin

class CommanderWindow(ListFunctionsMixin):
	def __init__(self, app, commander):
		self.app = app
		self.builder = app.builder
		self.commander = commander
		self.window = None
		self.listbox = None
		self.commanderSearchEntry = None
		self.window = self.builder.get_object("commanderWindow")
		self.commanderSearchEntry = self.builder.get_object("commanderSearchEntry")
		self.listbox = self.builder.get_object("commanderList")
		self.listbox.set_filter_func(self.filter, self.commanderSearchEntry)
		self.listbox.set_sort_func(self.sort, self.commanderSearchEntry)
				
		# when search, first command must be highlighted
		self.selected_first_row = None
		
		# this is to fix press down from search 
		# to move selection to the seacond row 
		# since the first row is already selected
		self.prepare_second_row = None


	
	def cache_commander_window(self):
		
		self.remove_all_commands()
	
		# commands are added to list only once
		# list takes care of filtering and sorting
		if not self.commands_added:
			self.add_commands(self.commander.commands)
			self.commands_added = True
			
		self.add_commands(self.commander.dynamic_commands)
		
		print("commands# " + str(len(self.listbox.get_children())))
	
		
		
		
	def show_commander_window(self):
	
		# must empty search every time showing commander
		self.commanderSearchEntry.set_text("")
		
		# get the focus to search to let user type right away
		self.commanderSearchEntry.grab_focus()
				
		# unselect_all previously selected row
		self.listbox.unselect_all()
		self.listbox.show_all()
			
		self.window.show()
		
		# unhighlight first row when show commander
		self.selected_first_row = None
		
		
	
	def remove_all_commands(self):
		rows = self.listbox.get_children()
		for r in rows:
			self.listbox.remove(r)
		
		self.commands_added = False
		
		
		
	def add_commands(self, commands):
		# loop through commands,
		for c in commands:
			# put each in gtkbox (name, shurtcut) and bind the command 
			box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
			
			# box doesn't have command, but in python
			# we are allowed to bind any method in run time
			# we can get command from activated rows
			box.command = c
			
			lblName = Gtk.Label.new(c['name'])
			lblShortcut = Gtk.Label.new(c['shortcut'])
			box.pack_start(lblName, False, False, 0)
			box.pack_end(lblShortcut, False, False, 0)
	
			# adding styles
			box.get_style_context().add_class("commanderRow")
			lblName.get_style_context().add_class("commanderCommandName")
			lblShortcut.get_style_context().add_class("commanderCommanShortcut")
			
			# add to listbox
			self.listbox.insert(box, -1)
				
		
	
	
	################### WINDOW EVENTS ########################
	def on_commanderWindow_key_press_event(self, window, event):
		keyval_name = Gdk.keyval_name(event.keyval)
		ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
		alt = (event.state & Gdk.ModifierType.MOD1_MASK)
		shift = (event.state & Gdk.ModifierType.SHIFT_MASK)
				
		# the same way as commander when open commander window,
		# this will close it with the same key
		if not ctrl:
			self.only_ctrl = True
		else:
			self.only_ctrl = False
			
		# also if press escape then close commander
		if keyval_name == "Escape":
			self.close()



	# if user preseed and released ctrl key, commander will close
	def on_commanderWindow_key_release_event(self, window, event):
		keyval_name = Gdk.keyval_name(event.keyval)
		ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
		alt = (event.state & Gdk.ModifierType.MOD1_MASK)
		shift = (event.state & Gdk.ModifierType.SHIFT_MASK)
		
		if ctrl and self.only_ctrl and keyval_name == "Control_L":
			self.close()
			
			
	# if user clicked outside commander window then close
	def on_commanderWindow_focus_out_event(self, window, d):
		self.close()
		

	# use hide to not lose the widgets from builder		
	def close(self):
		self.window.hide()

		


	################### LIST EVENTS ########################		
	# activated means either row clicked or selected by keyboard and hit enter 
	def on_commanderList_row_activated(self, widget, row):
		# run the command 
		self.run_command(row.get_child().command)
		
	
	
	def on_commanderList_key_press_event(self, widget, event):
		keyval_name = Gdk.keyval_name(event.keyval)
		
		# go up back to searchEntry
		if keyval_name == "Up":
			first_row = self.listbox.get_row_at_y(1)
			if not first_row or first_row.is_selected():
				self.commanderSearchEntry.grab_focus_without_selecting()
				
		# if start typing again, back to searchEntry
		# and insert that key to search 
		elif keyval_name != "Return" and keyval_name != "Up" and keyval_name != "Down":
			self.commanderSearchEntry.grab_focus_without_selecting()
			
			# pass the key press to search entry
			self.commanderSearchEntry.do_key_press_event(self.commanderSearchEntry, event)




	################### SEARCH ENTRY EVENTS ########################
	# The “search-changed” signal is emitted with a short delay of
	# 150 milliseconds after the last change to the entry text.
	# (see https://developer.gnome.org/gtk3/stable/GtkSearchEntry.html#GtkSearchEntry-search-changed) 
	def on_commanderSearchEntry_changed(self, widget):
		# reset first and second row refs
		self.selected_first_row = None
		self.prepare_second_row = None
		
		# for performance it is better to filter first then sort 
		# but to be able to detected first and second rows, we
		# have to run sort first, then filter.
		# when filter ran last, we can get the first and second rows
		# if sort ran after filter, then first and second rows would be 
		# sorted in different locations
		self.listbox.invalidate_sort()		# to force list to sort items
		self.listbox.invalidate_filter()	# to force list to filter items
		
		
	
	
	def on_commanderSearchEntry_key_press_event(self, widget, event):
		keyval_name = Gdk.keyval_name(event.keyval)
				
		# run the first result when hit enter, or right numpad enter
		if keyval_name == "Return" or keyval_name == "KP_Enter":
			
			# get the selected row, it should be the first (filtered/sorted) row 
			first_row = self.listbox.get_selected_row()
			
			if first_row:
				self.run_command(first_row.get_child().command)
			else:
				# if no rows, then show message no commands selected
				self.app.plugins_manager.plugins["message_notify.message_notify"].show_message("No commands selected!")

		
		# move to next row when press down key from searchEntry
		elif keyval_name == "Down":
			
			# if just opened the commander (i.e. no row selected)
			# then select the first row in list
			if not self.selected_first_row:
				# passing None as row makes listbox to select
				# the first row
				# shortcut of self.listbox.select_row(self.listbox.get_row_at_index(0)) 
				self.listbox.select_row(None)
			else:	
				# move to second row then focus
				# without this, user need to press "down" key twice
				# first to get listbox focus, second to move to second row
				self.listbox.select_row(self.prepare_second_row)
			
			# get the focus to listbox
			self.listbox.grab_focus()
			


	def run_command(self, command):
		if "parameters" in command:
			p = command["parameters"]
			command["ref"](p)
		else:
			command["ref"]()
			
		self.close()
