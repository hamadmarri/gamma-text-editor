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
		self.visible = False
		self.added_plugins = {}
		self.old_position = 0


	
	def activate(self):
		self.signal_handler.key_bindings_to_plugins.append(self)
		commands.set_commands(self)
		
		dir_path = os.path.dirname(os.path.realpath(__file__))
		self.builder = Gtk.Builder()
		self.builder.add_from_file(f"{dir_path}/bottom_panel.glade")
		self.builder.connect_signals(self.signals)
		
		window = self.builder.get_object("window")
		self.bottom_panel_body = self.builder.get_object("bottom_panel_body")
		self.notebook = self.builder.get_object("bottom_panel_notebook")
		window.remove(self.bottom_panel_body)
		
		self.close_button = self.builder.get_object("close_button")
		
		# get right side body
		self.right_side_body = self.app.builder.get_object("right_side_body")
		
	
	
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
		if not self.visible:
			self.show_panel()
		else:
			self.hide_panel()
	
	
	
	def on_notebook_switch_page(self, notebook, page, page_num):
		self.set_current_page(page, page_num)
		
		
	def set_current_page(self, page, page_num):
		self.current_page = page
		self.current_page_num = page_num
		current_label = self.notebook.get_tab_label_text(page)
		self.close_button.set_tooltip_text(f"Close {current_label}")
		
		
	
	def on_close_button_clicked(self, widget):
	
		# notify plugin that the page is closed/removed
		if hasattr(self.current_page, "on_page_remove"):
			self.current_page.on_page_remove(self.current_page)

		del self.added_plugins[self.current_page.plugin]
		self.notebook.remove_page(self.current_page_num)
		
		if self.notebook.get_n_pages() == 0:
			self.hide_panel()
	
	
	def on_hide_button_clicked(self, widget):
		self.hide_panel()
	
	
	
	def is_under_resized(self, paned):
		return (paned.get_allocated_height() - paned.get_position() < 25)
		
		
	
	def hide_panel(self):
		if not self.visible:
			return
	
		paned = self.right_side_body.get_children()[0]
		
		if self.is_under_resized(paned):
			self.old_position = 500
		else:
			self.old_position = paned.get_position()
		
		paned.remove(self.scrolled_sourceview)
		paned.remove(self.bottom_panel_body)
		self.right_side_body.remove(paned)		
		self.right_side_body.pack_start(self.scrolled_sourceview, True, True, 0)		
		self.visible = False
			
	
	
	def show_panel(self):
		if self.visible:
			return
		
		# if not pages, then show logs as default
		if self.notebook.get_n_pages() == 0:
			self.THE("logger", "show_log", {})
			return
			
		self.scrolled_sourceview = self.right_side_body.get_children()[0]
		self.right_side_body.remove(self.scrolled_sourceview)
		
		# create paned
		paned = Gtk.Paned.new(Gtk.Orientation.VERTICAL)
		paned.pack1(self.scrolled_sourceview, True, False)
		paned.pack2(self.bottom_panel_body, False, True)
		
		if self.old_position == 0:
			self.old_position = 500
		
		paned.set_position(self.old_position)
		
		self.right_side_body.pack_start(paned, True, True, 0)		
		self.right_side_body.show_all()
				
		# set current page
		page_num = self.notebook.get_current_page()
		page = self.notebook.get_nth_page(page_num)
		self.set_current_page(page, page_num)
		
		self.visible = True
		
		
		
		
	def add(self, plugin, label, widget, on_page_remove=None):
		# check if page is already added
		added = self.added_plugins.get(plugin)
		if added:
			self.show_panel()
			page_num = self.notebook.page_num(plugin.bottom_panel_page)
			
			# switch to this page
			self.notebook.set_current_page(page_num)
			
			# update label (sometimes it is needed)
			self.notebook.set_tab_label(plugin.bottom_panel_page, Gtk.Label.new(label))
			return True
		
		self.added_plugins[plugin] = plugin
	
		tab_label = Gtk.Label.new(label)

		page = widget
		
		# bind plugin to page
		page.plugin = plugin
		
		# bind on_page_remove callback to box_child
		if on_page_remove:
			page.on_page_remove = on_page_remove
		
		self.notebook.append_page(page, tab_label)
		self.notebook.show_all()
		
		self.show_panel()
		
		# bind page to plugin
		plugin.bottom_panel_page = page
		
		page_num = self.notebook.page_num(page)
		self.notebook.set_current_page(page_num)
		return True
		
