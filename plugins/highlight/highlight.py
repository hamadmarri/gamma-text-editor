#
#### Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Feb 11th, 2020
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
# 
#	highlight: is responsible for highlighting the selected text by user. It
#	highlights all occurrences of selected text. The highlight_signal functions
#	is connected with mark-set signal in sourceview_manager.py
#

import re # for regex

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Plugin():
	
	def __init__(self, app):
		self.name = "highlight"
		self.app = app
		self.sourceview_manager = app.sourceview_manager
		self.plugins = app.plugins_manager.plugins
		self.commands = []
		self.tag_name = "search-match"
		self.spaces_pattern = re.compile("^\s+$")

		
	def activate(self):
		# connect signal mark-set event which is when user select text
		# user clicks to unselect text is also connected
		# see highlight.highlight_signal function for handling 
		# mark-set event
		self.sourceview_manager.source_view.get_buffer().connect("mark-set", self.highlight_signal)
		
		
	
	def highlight_signal(self, buffer, location, mark):
		# insert is the mark when user change
		# the cursor or select text
		if mark.get_name() == "insert":
			# gets (start, end) iterators of 
			# the selected text
			iters = buffer.get_selection_bounds()
			
			# if user only clicked/placed the cursor
			# without any selected chars, then remove
			# previously highlighted texts
			if not iters:
				# remove highlight
				self.remove_highlight(self.tag_name)
			else:
				# when user selected some text
				# get the start and end iters
				(iter_start, iter_end) = iters
				
				# get the text is being selected, False means without tags
				# i.e. only appearing text without hidden tags set by sourceview
				# (read: https://developer.gnome.org/gtk3/stable/GtkTextBuffer.html#gtk-text-buffer-get-text)
				search = buffer.get_text(iter_start, iter_end, False)
				
				
				# if select only one letter
				if len(search) == 1 and search.isalpha():
					# remove highlight
					self.remove_highlight(self.tag_name)
					return
				
				# if selected is only spaces
				if self.spaces_pattern.match(search):
					# remove highlight
					self.remove_highlight(self.tag_name)
					return
		
		
				# highlight text is in seperate method
				# which help to select any text string 
				# by other plugins like find or search
				counter = self.highlight(search)
				self.plugins["message_notify.message_notify"].show_message(f"Highlighted | {counter}")
		
	
	# "search" is a string text
	# highlighting is done by adding tag(s) to
	# the text you want to highlight. The tag 
	# can have custom styling like "background color"
	# or you can copy the "search-match" style from
	# the style scheme which is set for styling the 
	# sourceview ins source_style plugin
	def highlight(self, search, search_flags=0):
			
		self.remove_highlight(self.tag_name)
		
		# if search is empty, exit
		if not search:
			return
		
		# get the currently openned/showing buffer
		buffer = self.plugins["files_manager.files_manager"].current_file.source_view.get_buffer()
		
		tag = self.setup_tag(buffer)

		# to count occurrences
		counter = 0

		# need to search for the text needed to be highlighted
		# and keep searching and taging every occurrence of the 
		# "search" text in buffer
		start_iter = buffer.get_start_iter()
		
		# gets start,end iters or None if no match
		# first search start from the beggining of the buffer
		# i.e. start_iter
		matches = start_iter.forward_search(search, search_flags, None)			
		
		# loop while still have matches (occurrences)
		while matches != None:
			counter += 1
			
			# extract start, end iters from matches
			(match_start, match_end) = matches
			
			# set the tag to current match 
			buffer.apply_tag(tag, match_start, match_end)
			
			# do search again but start from the match_end
			# i.e. continue the search, do not search from the 
			# beggining of the file again!
			matches = match_end.forward_search(search, search_flags, None)
		
		return counter
		
	
	def setup_tag(self, buffer):
		# get the tags table 
		tag_table = buffer.get_tag_table();
		
		# create new tag
		tag = Gtk.TextTag.new(self.tag_name)
		
		# get the style scheme to copy "search-match" styling 
		style = buffer.get_style_scheme()
		search_tag = style.get_style("search-match")
		tag.props.background = search_tag.props.background
		
		# add the styled tag to tag_table
		tag_table.add(tag)
		
		return tag
		
	
	
	def highlight_custom_tag(self, buffer, start_iter, end_iter, tag, tag_name):
		self.remove_highlight(tag_name)
		
		# get the tags table 
		tag_table = buffer.get_tag_table();
		
		# add the styled tag to tag_table
		tag_table.add(tag)
		buffer.apply_tag(tag, start_iter, end_iter)
		

		
	# props can have:
	#	background
	#	weight
	def setup_custom_tag(self, buffer, tag_name, props):
		# create new tag
		tag = Gtk.TextTag.new(tag_name)
				
		if "background" in props:
			tag.props.background = props["background"]
		
		if "weight" in props:
			tag.props.weight = props["weight"]
		
		return tag
		
	
	
	
	def remove_highlight(self, tag_name):
		buffer = self.plugins["files_manager.files_manager"].current_file.source_view.get_buffer()
		tag_table = buffer.get_tag_table();
		
		# get the tag by looking up to it is name "search-match"
		tag = tag_table.lookup(tag_name)
		
		# if no tag with this name then return/done
		if not tag:
			return
			
		# must remove tag from both tag table and buffer
		tag_table.remove(tag)
		buffer.remove_tag_by_name(tag_name, buffer.get_start_iter(), buffer.get_end_iter())
	
	
