import os


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class FakePlugin(object):
	pass

class OutputGUI(object):

	
	def show_output_gui(self, label, a_copy):
		self.show_output_in_bottom_panel(label, a_copy)
	
	
	def clear_buffer(self, button, buffer):
		buffer.delete(buffer.get_start_iter(), buffer.get_end_iter())
	
	
	def window_close_event(self, w):
		self.delete_copy(w.a_copy)
	
	
	def instantiate_widgets(self):		
		window = Gtk.Window.new(Gtk.WindowType.TOPLEVEL)
		output_body = Gtk.Overlay.new()
		output_scrolled_window = Gtk.ScrolledWindow.new(None, None)
		textview = Gtk.TextView.new()
		clear_btn = Gtk.Button.new()
		
		window.set_default_size(*(self.window.get_default_size()))
		window.connect("destroy", self.window_close_event)
		
		textview.set_editable(False)
		textview.set_bottom_margin(self.textview.get_bottom_margin())
		buffer = textview.get_buffer()
		
		clear_btn.set_label(self.clear_btn.get_label())
		clear_btn.set_valign(self.clear_btn.get_valign())
		clear_btn.set_halign(self.clear_btn.get_halign())
		clear_btn.connect("clicked", self.clear_buffer, buffer)
		
		output_scrolled_window.set_name("output_scrolled_window")
		textview.set_name("output_textview")
		
		output_scrolled_window.get_style_context().add_provider(
			self.style_provider,
			Gtk.STYLE_PROVIDER_PRIORITY_USER
		)
		
		textview.get_style_context().add_provider(
			self.style_provider,
			Gtk.STYLE_PROVIDER_PRIORITY_USER
		)
		
		output_body.add(output_scrolled_window)
		output_body.add_overlay(clear_btn)
		window.add(output_body)
		output_scrolled_window.add(textview)
		window.set_transient_for(self.app.window)
		
		a_copy = {
			"plugin": FakePlugin(),
			"window": window,
			"output_body": output_body,
			"textview": textview,
			"buffer": buffer
		}
		
		# bind a_copy to its window
		window.a_copy = a_copy
		return a_copy
		
		
	
	
	def load_from_builder(self):				
		dir_path = os.path.dirname(os.path.realpath(__file__))
		builder = Gtk.Builder()
		builder.add_from_file(f"{dir_path}/output.glade")
		
		self.window = builder.get_object("output_window")
		self.output_body = builder.get_object("output_body")
		self.output_scrolled_window = builder.get_object("output_scrolled_window")
		self.textview = builder.get_object("output_textview")
		self.clear_btn = builder.get_object("clear_btn")
		
		self.style_provider = Gtk.CssProvider()
		self.style_provider.load_from_path(f"{dir_path}/output.css")
		
		
		
	
	
	def show_output_window(self, label, a_copy):		
		if not a_copy["window"].get_visible():
			a_copy["window"].show_all()
		
		
		
	def show_output_in_bottom_panel(self, label, a_copy):
		if a_copy["window"].get_child():
			a_copy["window"].remove(a_copy["output_body"])
			
		a_copy["output_body"].show_all()
		args = {
			"plugin": a_copy["plugin"],
			"label": label,
			"widget": a_copy["output_body"],
		}

		
		added = self.THE("bottom_panel", "add", args)
		
		# TODO DEBUG
		# added = False
		
		if not added:
			a_copy["window"].add(a_copy["output_body"])
			self.show_output_window(label, a_copy)
				
		
			
