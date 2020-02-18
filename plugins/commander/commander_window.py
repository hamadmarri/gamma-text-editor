
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class CommanderWindow:
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
		self.commands_added = False
		self.selected_row = False



	def show_commander_window(self):
		if not self.commands_added:
			self.add_commands()
			self.commands_added = True
		
		self.commanderSearchEntry.set_text("")
		
		
		#no_result = Gtk.Label.new("No commands found!")
		#no_result.command = None
		#self.listbox.insert(no_result, -1)
		self.listbox.unselect_all()
		self.listbox.show_all()
		
		self.window.show()
		
	
	
	def add_commands(self):
		lbl = None
		for c in self.commander.commands:
			#print(c, "\n")
			lbl = Gtk.Label.new(f"{c['name']}\t{c['shortcut']}")
			lbl.command = c
			self.listbox.insert(lbl, -1)
		
		
		
		
	def filter(self, row, *user_data):
		searchEntry = user_data[0]
		search_text = searchEntry.get_text().lower()
		show = False
		
		# if empty, show all
		if not search_text:
			self.listbox.select_row(None)
			return True
		
		row_text = row.get_child().get_text().lower()
		show = (row_text.find(search_text) != -1)
			
		if not self.selected_row and show:
			self.selected_row = True
			self.listbox.select_row(row)
		
		return show
		
	
	
	def sort(self, row1, row2, *user_data):
		search = user_data[0].get_text().lower()
		
		if not search:
			return -1
		
		command1 = row1.get_child().get_text().lower()
		command2 = row2.get_child().get_text().lower()
		index1 = command1.find(search)
		index2 = command2.find(search)
		
		
		return (index1 - index2)
		
		
	
	
	################### WINDOW EVENTS ########################
	def on_commanderWindow_key_press_event(self, window, event):
		keyval_name = Gdk.keyval_name(event.keyval)
		ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
		alt = (event.state & Gdk.ModifierType.MOD1_MASK)
		shift = (event.state & Gdk.ModifierType.SHIFT_MASK)
				
		if not alt:
			self.only_alt = True
		else:
			self.only_alt = False
			
		if keyval_name == "Escape":
			self.close()



	def on_commanderWindow_key_release_event(self, window, event):
		keyval_name = Gdk.keyval_name(event.keyval)
		ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)
		alt = (event.state & Gdk.ModifierType.MOD1_MASK)
		shift = (event.state & Gdk.ModifierType.SHIFT_MASK)
		
		if alt and self.only_alt and keyval_name == "Alt_L":
			self.close()
			
			
	
	def on_commanderWindow_focus_out_event(self, window, d):
		self.close()
		
		
	def close(self):
		self.window.hide()
		


	################### LIST EVENTS ########################		
	def on_commanderList_row_activated(self, widget, row):
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
	def on_commanderSearchEntry_changed(self, widget):
		self.selected_row = False
		self.listbox.invalidate_sort()
		self.listbox.invalidate_filter()
		
		
		
	def on_commanderSearchEntry_key_press_event(self, widget, event):
		keyval_name = Gdk.keyval_name(event.keyval)
				
		# run the first result
		if keyval_name == "Return":
			first_row = self.listbox.get_selected_row()
			
			if first_row:
				self.run_command(first_row.get_child().command)
			else:
				self.app.plugins_manager.plugins["message_notify.message_notify"].show_message("No commands found!")
						
		


	def run_command(self, command):
		command["ref"]()
		#print(command["name"])
		self.close()
