#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3.2 code
#
# Copyright (c) 2011 Jeff Smits
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# SVF_functions
# Parser functions for the SVF commandline tool for reading the file given

from SVF_class import SVF

import os.path
import json

def generic():
	args = SVF.args
	err  = SVF.parser.error
	dont_care, ext = os.path.splitext(args.file.name)
	#remove dot
	ext = ext[1:]
	if ext == 'gen':
		err("argument -a/--format: can't recognise extension '"+ext+"' of "
			"file '"+args.file.name+"': [Errno 2] KeyError: "+str(ext))
	try:
		return parsers[ext]()
	#TODO: add checking what the first characters of the file are. 
	#  On {" or {' or [" or ['    try json
	#  On <?xml                   try plist
	#  On [\w or \w               try ini
	except KeyError as exc:
		err("argument -a/--format: can't recognise extension '"+ext+"' of "
			"file '"+args.file.name+"': [Errno 2] '"+ext+"'")

def _json():
	args = SVF.args
	err  = SVF.parser.error
	try:
		return json.load(args.file)
	except Exception as exc:
		err("argument -f/--file: can't find any json in file '"
			+args.file.name+"': [Errno 2] "+str(exc)+"\nWrong encoding maybe?")

#TODO: add plist and ini support

parsers = {
	'gen':  generic,
	'json': _json,
	'js':   _json,
}

for name in parsers:
	SVF.parsers[name] = parsers[name]