import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class FindReplaceWindow(object):
	
	def set_handlers(self):
		self.signals = {
			"on_window_delete_event": self.on_window_delete_event,
			# "on_find_replace_window_focus_in_event": self.on_find_replace_window_focus_in_event,
			"on_find_prev_btn_clicked": self.on_find_prev_btn_clicked,
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
				
		self.window = self.builder.get_object("find_replace_window")
		self.window.set_transient_for(self.app.window)
		
		
	
	def hide(self):
		self.window.hide()
		self.new_search = True
		self.clear_highlights()
		
		
		
	def show_window(self, show_replace=False):
		self.show_replace = show_replace
		if not self.window:
			self.load_ui()
		
		replace_expander = self.builder.get_object("replace_expander")
		replace_expander.set_expanded(self.show_replace)
		
		self.window.show_all()

		
	
	# def on_find_replace_window_focus_in_event(self, w, d):
	# 	self.sourceview = self.plugins["files_manager.files_manager"].current_file.source_view
	# 	if not self.buffer:
	# 		self.buffer = self.sourceview.get_buffer()
	# 	elif self.buffer != self.sourceview.get_buffer():
	# 		self.new_search = True
	# 		self.buffer = self.sourceview.get_buffer()

 
	
	def on_window_delete_event(self, w, e):
		self.hide()
		return True
	
	
	def on_find_prev_btn_clicked(self, w):
		self.do_find(previous=True)
		
		
	def on_find_btn_clicked(self, w):
		self.do_find()
	
	
	
	def on_replace_btn_clicked(self, w):
		self.do_replace()
	
	def on_replace_all_btn_clicked(self, w):
		self.do_replace_all()
	
	def on_match_case_btn_toggled(self, w):
		self.match_case = w.get_active()
		self.new_search = True
		
	
	def on_whole_world_btn_toggled(self, w):
		self.whole_word = w.get_active()
		self.new_search = True
		
	
	def on_close_find_btn_clicked(self, w):
		self.hide()


	def on_find_text_view_changed(self, buffer):
		self.new_search = True
