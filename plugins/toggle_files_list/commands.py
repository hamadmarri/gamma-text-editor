#
#### Author: Hamad Al Marri <hamad.s.almarri@gmail.com>
#### Date: Mar 10th, 2020
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
#
# 	plugin info: Toggle (hides/shows) the files list to make the text editing area wider
# 
# 
# 

def set_commands(plugin):
	plugin.commands.append( 
		{
			"plugin-name": plugin.name,
			"name": "Toggle Show/Hide Files",
			"ref": plugin.toggle_files_list,
			"shortcut": "<Alt> + f",
		}
	)
	
