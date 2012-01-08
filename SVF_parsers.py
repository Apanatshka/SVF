#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3.2 code
#
# SVF_functions
# version 0.3
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
	if ext is 'gen':
		err("argument -a/--format: can't recognise extension '"+ext+"' of "
			"file '"+args.file.name+"': [Errno 2] KeyError: "+str(err))
	try:
		return parsers[ext]()
	#TODO: add checking what the first characters of the file are. 
	#  On {" or {' or [" or ['    try json
	#  On <?xml                   try plist
	#  On [\w or \w               try ini
	except KeyError as err:
		err("argument -a/--format: can't recognise extension '"+ext+"' of "
			"file '"+args.file.name+"': [Errno 2] '"+ext+"'")

def _json():
	args = SVF.args
	err  = SVF.parser.error
	try:
		return json.load(args.file)
	except Exception as err:
		err("argument -f/--file: can't find any json in file '"
			+args.file.name+"': [Errno 2] "+str(err)+"\nWrong encoding maybe?")

#TODO: add plist and ini support

parsers = {
	'gen':  generic,
	'json': _json,
	'js':   _json,
}

for name in parsers:
	SVF.parsers[name] = parsers[name]