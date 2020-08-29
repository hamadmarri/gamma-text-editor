import os

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk


class LoggerGUI(object):


	def on_log_window_destroy(self, w):
		self.window.parent_window.logger_need_reload = True
		self.window.parent_window.logger_log_body = None
		self.window = None
	
	def on_page_remove(self, widget):
		self.app.window.logger_need_reload = True
		self.app.window.logger_log_body = None
	
	
	def show_log_gui(self, text):
		if self.window != None and self.window.get_visible():
			return
				
		self.load_from_builder()
		buffer = self.app.window.logger_textview.get_buffer()
		start_iter = buffer.get_start_iter()
		end_iter = buffer.get_end_iter()
		buffer.delete(start_iter, end_iter)
		start_iter = buffer.get_start_iter()
		
		self.app.window.logger_original_results = text
		buffer.insert_markup(start_iter, self.colorize_textview(text), -1)
		self.show_log_in_bottom_panel()
		
		GLib.idle_add(self.scroll_to_end)
		
				
	
	def load_from_builder(self):
		if not self.app.window.logger_need_reload:
			return
				
		self.app.window.logger_need_reload = False
				
		dir_path = os.path.dirname(os.path.realpath(__file__))
		builder = Gtk.Builder()
		builder.add_from_file(f"{dir_path}/logger.glade")
		builder.connect_signals(self.signals)
		
		self.window = builder.get_object("log_window")
		self.app.window.logger_log_body = builder.get_object("log_body")
		self.app.window.logger_log_scrolled = builder.get_object("log_scrolled_window")
		self.app.window.logger_textview = builder.get_object("log_textview")
		self.app.window.logger_log_search = builder.get_object("log_search")
				
		
		style_provider = Gtk.CssProvider()
		style_provider.load_from_path(f"{dir_path}/logger.css")
		self.app.window.logger_log_scrolled.get_style_context().add_provider(
			style_provider,
			Gtk.STYLE_PROVIDER_PRIORITY_USER
		)
		
		self.app.window.logger_textview.get_style_context().add_provider(
			style_provider,
			Gtk.STYLE_PROVIDER_PRIORITY_USER
		)
		
		
	
	
	def show_log_window(self):
		self.window.set_transient_for(self.app.window)
		
		if not self.window.get_visible():
			self.window.show_all()
			self.window.parent_window = self.app.window
		
		
		
	def show_log_in_bottom_panel(self):
		if self.window.get_child():
			self.window.remove(self.app.window.logger_log_body)
			
		self.app.window.logger_log_body.show_all()
		args = {
			"plugin": self,
			"label": "Log",
			"widget": self.app.window.logger_log_body,
			"on_page_remove": self.on_page_remove
		}
		
		if self.app.window.logger_log_type == 1:
			args["label"] = "Log <WARNINGS>"
		elif self.app.window.logger_log_type == 2:
			args["label"] = "Log <ERRORS>"
		
		added = self.THE("bottom_panel", "add", args)
		
		# TODO DEBUG
		# added = False
		
		if not added:
			self.window.add(self.app.window.logger_log_body)
			self.show_log_window()
			
			
	
	def scroll_to_end(self):
		scrolled = self.app.window.logger_log_scrolled
		adj = scrolled.get_vadjustment()
		adj.set_value(adj.get_upper())
		scrolled.set_vadjustment(adj)
		return False
		
	
	def append_to_log(self, log_entry):
		if self.app.window.logger_log_body:
			if  self.app.window.logger_log_type == 1 and log_entry.level != "WARNING":
				return
			
			if  self.app.window.logger_log_type == 2 and log_entry.level != "ERROR":
				return
		
			text = log_entry.message
			buffer = self.app.window.logger_textview.get_buffer()
			text += "\n"
			self.app.window.logger_original_results += text
			
			
			search_term = self.app.window.logger_log_search.get_buffer().get_text().lower()
			filtered = self.filter(text, search_term)
			
			if filtered:
				buffer.insert_markup(buffer.get_end_iter(), self.colorize_textview(filtered), -1)
			
			GLib.idle_add(self.scroll_to_end)
			
		
		
	def on_log_search_search_changed(self, widget):
		search_term = widget.get_text().lower()
		
		buffer = self.app.window.logger_textview.get_buffer()
		start_iter = buffer.get_start_iter()
		end_iter = buffer.get_end_iter()
		
		filtered = self.filter(self.app.window.logger_original_results, search_term)
		
		buffer.delete(start_iter, end_iter)
		start_iter = buffer.get_start_iter()
		buffer.insert_markup(start_iter, self.colorize_textview(filtered), -1)
		
		GLib.idle_add(self.scroll_to_end)
		
		
	
	def filter(self, original_results, search_term):
		lines = original_results.splitlines(keepends=True)
		filtered = ""
		
		for line in lines:
			if line.lower().find(search_term) != -1:
				filtered += line
		
		return filtered
			
