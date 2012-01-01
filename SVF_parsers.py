#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3.2 code
#
# SVF_functions
# version 0.3
# Parser functions for the SVF commandline tool for reading the file given

import os.path
import json

def generic(args, parser):
	no_interest, ext = os.path.splitext(args.file.name)
	#remove dot
	ext = ext[1:]
	if ext is 'gen':
		parser.error("argument -a/--format: can't recognise extension '"+ext+"' of "
			"file '"+args.file.name+"': [Errno 2] KeyError: "+str(err))
	try:
		return psrs[ext](args, parser)
	except KeyError as err:
		parser.error("argument -a/--format: can't recognise extension '"+ext+"' of "
			"file '"+args.file.name+"': [Errno 2] '"+ext+"'")

def _json(args, parser):
	try:
		return json.load(args.file)
	except Exception as err:
		parser.error("argument -f/--file: can't find any json in file '"
			+args.file.name+"': [Errno 2] "+str(err)+"\nWrong encoding maybe?")

psrs = {
'gen': generic,
'json': _json,
'js': _json,
}