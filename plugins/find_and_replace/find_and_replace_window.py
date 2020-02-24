import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class FindReplaceWindow(object):
	
	def set_handlers(self):
		self.signals = {
			"on_window_delete_event": self.on_window_delete_event,
			"on_find_btn_clicked": self.on_find_btn_clicked,
			"on_replace_btn_clicked": self.on_replace_btn_clicked,
			"on_replace_all_btn_clicked": self.on_replace_all_btn_clicked,
			"on_match_case_btn_toggled": self.on_match_case_btn_toggled,
			"on_whole_world_btn_toggled": self.on_whole_world_btn_toggled,
			"on_close_find_btn_clicked": self.on_close_find_btn_clicked,
			}
		
	
	def load_ui(self):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		self.builder = Gtk.Builder()
		self.builder.add_from_file(f"{dir_path}/ui.glade")
		
		self.builder.connect_signals(self.signals)
		
		self.find_text_view = self.builder.get_object("find_text_view")
		self.find_text_view.get_buffer().connect("changed", self.on_find_text_view_changed)
		
		self.replace_text_view = self.builder.get_object("replace_text_view")
				
		self.window = self.builder.get_object("window")
		self.window.set_transient_for(self.app.window)
		
		
	
	def hide(self):
		self.window.hide()
		self.new_search = True
		
		# to clear highlights
		self.plugins["search.search_in_file"].do_highlight("")
		self.plugins["search.search_in_file"].quit_search()
		
		
		
	def show_window(self):
		if not self.window:
			self.load_ui()
			
		self.window.show_all()
		
		
	def on_window_delete_event(self, w, e):
		self.hide()
		return True
		
	def on_find_btn_clicked(self, w):
		self.do_find()
	
	def on_replace_btn_clicked(self, w):
		pass
	
	def on_replace_all_btn_clicked(self, w):
		pass
	
	def on_match_case_btn_toggled(self, w):
		# get_active
		pass
	
	def on_whole_world_btn_toggled(self, w):
		# get_active
		pass
	
	def on_close_find_btn_clicked(self, w):
		self.hide()


	def on_find_text_view_changed(self, buffer):
		self.new_search = True