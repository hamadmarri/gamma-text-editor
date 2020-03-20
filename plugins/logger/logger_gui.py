import os


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class LoggerGUI(object):


	def on_log_window_destroy(self, w):
		self.need_reload = True
		self.log_body = None
		
	def on_page_remove(self, widget):
		self.need_reload = True
		self.log_body = None
	
	
	def show_log_gui(self, text):
		self.load_from_builder()
		buffer = self.textview.get_buffer()
		start_iter = buffer.get_start_iter()
		end_iter = buffer.get_end_iter()
		buffer.delete(start_iter, end_iter)
		start_iter = buffer.get_start_iter()
		
		self.original_results = text
		buffer.insert_markup(start_iter, self.colorize_textview(text), -1)
		self.show_log_in_bottom_panel()
		
		
	
	def load_from_builder(self):
		if not self.need_reload:
			return
			
		self.need_reload = False
				
		dir_path = os.path.dirname(os.path.realpath(__file__))
		builder = Gtk.Builder()
		builder.add_from_file(f"{dir_path}/logger.glade")
		builder.connect_signals(self.signals)
		
		self.window = builder.get_object("log_window")
		self.log_body = builder.get_object("log_body")
		self.log_scrolled = builder.get_object("log_scrolled_window")
		self.textview = builder.get_object("log_textview")
		self.log_search = builder.get_object("log_search")
		
		style_provider = Gtk.CssProvider()
		style_provider.load_from_path(f"{dir_path}/logger.css")
		self.log_scrolled.get_style_context().add_provider(
			style_provider,
			Gtk.STYLE_PROVIDER_PRIORITY_USER
		)
		
		self.textview.get_style_context().add_provider(
			style_provider,
			Gtk.STYLE_PROVIDER_PRIORITY_USER
		)
		
		
	
	
	def show_log_window(self):
		self.window.set_transient_for(self.app.window)
		
		if not self.window.get_visible():
			self.window.show_all()
		
		
		
	def show_log_in_bottom_panel(self):
		if self.window.get_child():
			self.window.remove(self.log_body)
			
		self.log_body.show_all()
		args = {
			"plugin": self,
			"label": "Log",
			"widget": self.log_body,
			"on_page_remove": self.on_page_remove
		}
		
		if self.log_type == 1:
			args["label"] = "Log <WARNINGS>"
		elif self.log_type == 2:
			args["label"] = "Log <ERRORS>"
		
		added = self.THE("bottom_panel", "add", args)
		
		# TODO DEBUG
		# added = False
		
		if not added:
			self.window.add(self.log_body)
			self.show_log_window()
			
			
			
	
	def append_to_log(self, log_entry):
		if self.log_body:
			if  self.log_type == 1 and log_entry.level != "WARNING":
				return
			
			if  self.log_type == 2 and log_entry.level != "ERROR":
				return
		
			text = log_entry.message
			buffer = self.textview.get_buffer()
			text += "\n"
			self.original_results += text
			
			
			search_term = self.log_search.get_buffer().get_text().lower()
			filtered = self.filter(text, search_term)
			
			if filtered:
				buffer.insert_markup(buffer.get_end_iter(), self.colorize_textview(filtered), -1)
		
		
		
	def on_log_search_search_changed(self, widget):
		search_term = widget.get_text().lower()
		
		buffer = self.textview.get_buffer()
		start_iter = buffer.get_start_iter()
		end_iter = buffer.get_end_iter()
		
		filtered = self.filter(self.original_results, search_term)
		
		buffer.delete(start_iter, end_iter)
		start_iter = buffer.get_start_iter()
		buffer.insert_markup(start_iter, self.colorize_textview(filtered), -1)
		
		
		
	
	def filter(self, original_results, search_term):
		lines = original_results.splitlines(keepends=True)
		filtered = ""
		
		for line in lines:
			if line.lower().find(search_term) != -1:
				filtered += line
		
		return filtered
			
