#
#### Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Mar 18th, 2020
#
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#

import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from . import commands


class Plugin():
	
	def __init__(self, app):
		self.name = "bottom_panel"
		self.app = app
		self.signal_handler = app.signal_handler
		self.handlers = app.signal_handler.handlers
		self.THE = app.plugins_manager.THE
		self.commands = []
		self.set_handlers()
		self.old_position = 0

		self.signal_handler.key_bindings_to_plugins.append(self)
		commands.set_commands(self)
	

	
	def activate(self):
		self.app.window.bottom_panel_builder = None
		self.app.window.bottom_panel_added_plugins = {}
		self.app.window.bottom_panel_added_pages = {}
		self.app.window.bottom_panel_visible = False

	
	def load_from_builder(self):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		self.app.window.bottom_panel_builder = Gtk.Builder()
		builder = self.app.window.bottom_panel_builder
		builder.add_from_file(f"{dir_path}/bottom_panel.glade")
		builder.connect_signals(self.signals)
		
		window = builder.get_object("window")
		self.app.window.bottom_panel_panel_body = builder.get_object("bottom_panel_body")
		self.app.window.bottom_panel_notebook = builder.get_object("bottom_panel_notebook")
		window.remove(self.app.window.bottom_panel_panel_body)
		
		self.app.window.bottom_panel_close_button = builder.get_object("close_button")
		
		
	
	
	def set_handlers(self):
		self.signals = {
			"on_notebook_switch_page": self.on_notebook_switch_page,
			"on_close_button_clicked": self.on_close_button_clicked,
			"on_hide_button_clicked": self.on_hide_button_clicked
		}
		
			
	
	def key_bindings(self, event, keyval_name, ctrl, alt, shift):
		if keyval_name == "F9":
			self.toggle_bottom_panel()
			
			
	
	def toggle_bottom_panel(self):
		self.assert_widgets_loaded()
		
		if not self.app.window.bottom_panel_visible:
			self.show_panel()
		else:
			self.hide_panel()
	
	
	
	def assert_widgets_loaded(self):
		if not self.app.window.bottom_panel_builder:
			self.load_from_builder()
	
	
	def on_notebook_switch_page(self, notebook, page, page_num):
		self.set_current_page(page, page_num)
		
		
	def set_current_page(self, page, page_num):
		self.app.window.bottom_panel_current_page = page
		self.app.window.bottom_panel_current_page_num = page_num
		current_label = self.app.window.bottom_panel_notebook.get_tab_label_text(page)
		self.app.window.bottom_panel_close_button.set_tooltip_text(f"Close {current_label}")
		
		
	
	def on_close_button_clicked(self, widget):
		# notify plugin that the page is closed/removed
		if hasattr(self.app.window.bottom_panel_current_page, "on_page_remove"):
			self.app.window.bottom_panel_current_page.on_page_remove(self.app.window.bottom_panel_current_page)

		del self.app.window.bottom_panel_added_plugins[str(self.app.window) + str(self.app.window.bottom_panel_current_page.plugin)]
		self.app.window.bottom_panel_notebook.remove_page(self.app.window.bottom_panel_current_page_num)
		
		if self.app.window.bottom_panel_notebook.get_n_pages() == 0:
			self.hide_panel()
	
	
	def on_hide_button_clicked(self, widget):
		self.hide_panel()
	
	
	
	def is_under_resized(self, paned):
		return (paned.get_allocated_height() - paned.get_position() < 25)
		
		
	
	def hide_panel(self):
		if not self.app.window.bottom_panel_visible:
			return
	
		# get right side body
		right_side_body = self.app.builder.get_object("right_side_body")
		scrolled_sourceview = self.app.builder.get_object("scroll_and_source_and_map_box")
		
		paned = right_side_body.get_children()[0]
		
		if self.is_under_resized(paned):
			self.old_position = 500
		else:
			self.old_position = paned.get_position()
		
		paned.remove(scrolled_sourceview)
		paned.remove(self.app.window.bottom_panel_panel_body)
		right_side_body.remove(paned)		
		right_side_body.pack_start(scrolled_sourceview, True, True, 0)		
		self.app.window.bottom_panel_visible = False
			
	
	
	def show_panel(self):		
		if self.app.window.bottom_panel_visible:
			return
		
		# if not pages, then show logs as default
		if self.app.window.bottom_panel_notebook.get_n_pages() == 0:
			self.THE("logger", "show_log", {})
			return
		
		# get right side body
		right_side_body = self.app.builder.get_object("right_side_body")
		scrolled_sourceview = self.app.builder.get_object("scroll_and_source_and_map_box")
		
		right_side_body.remove(scrolled_sourceview)
		
		# create paned
		paned = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
		paned.pack1(scrolled_sourceview, True, False)
		paned.pack2(self.app.window.bottom_panel_panel_body, False, True)
		
		if self.old_position == 0:
			self.old_position = 500
		
		paned.set_position(self.old_position)
		
		right_side_body.pack_start(paned, True, True, 0)		
		right_side_body.show_all()
				
		# set current page
		page_num = self.app.window.bottom_panel_notebook.get_current_page()
		page = self.app.window.bottom_panel_notebook.get_nth_page(page_num)
		self.set_current_page(page, page_num)
		
		self.app.window.bottom_panel_visible = True
		
		
		
		
	def add(self, plugin, label, widget, on_page_remove=None):
		self.assert_widgets_loaded()
		
		# check if page is already added
		added = self.app.window.bottom_panel_added_plugins.get(str(self.app.window) + str(plugin))
		if added:
			self.show_panel()
			page_num = self.app.window.bottom_panel_notebook.page_num(self.app.window.bottom_panel_added_pages[plugin])
			
			# switch to this page
			self.app.window.bottom_panel_notebook.set_current_page(page_num)
			
			# update label (sometimes it is needed)
			self.app.window.bottom_panel_notebook.set_tab_label(self.app.window.bottom_panel_added_pages[plugin], Gtk.Label.new(label))
			return True
		
		self.app.window.bottom_panel_added_plugins[str(self.app.window) + str(plugin)] = plugin
	
		tab_label = Gtk.Label.new(label)

		page = widget
		
		# bind plugin to page
		page.plugin = plugin
		
		# bind on_page_remove callback to box_child
		if on_page_remove:
			page.on_page_remove = on_page_remove
		
		self.app.window.bottom_panel_notebook.append_page(page, tab_label)
		self.app.window.bottom_panel_notebook.show_all()
		
		self.show_panel()
		
		# bind page to plugin
		# plugin.bottom_panel_page = page
		self.app.window.bottom_panel_added_pages[plugin] = page
		
		page_num = self.app.window.bottom_panel_notebook.page_num(page)
		self.app.window.bottom_panel_notebook.set_current_page(page_num)
		return True
		
