#! /usr/bin/bash


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
#


# if passed args
# echo $1
export GAMMA_OPEN_FILE="$@"


# run gamma with python3
python3 /home/hamad/dev/pygtk/gamma/gamma.py

