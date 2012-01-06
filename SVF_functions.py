#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3.2 code
#
# SVF_functions
# version 0.3
# Functions for the SVF commandline tool for interpreting the statements

def get_var(args, vars, parser, func_args):
	try:
		vars[func_args[0]]
	except KeyError:
		if args.ignore:
			return None
		else:
			parser.error("file value: can't find variablename '"+func_args[0]+"' in "
				"file '"+args.file.name+"': [Errno 2] KeyError: '"+func_args[0]+"'")
	if len(func_args) == 1:
		return vars[func_args[0]]
	else:
		return get_var(args, vars[func_args[0]], parser, func_args[1:])

def join(args, vars, parser, func_args):
	try:
		iter(vars[func_args[0]])
	except KeyError:
		if args.ignore:
			return None
		else:
			parser.error("file value: can't find variablename '"+func_args[0]+"' in "
				"file '"+args.file.name+"': [Errno 2] KeyError: '"+func_args[0]+"'")
	except TypeError as err:
		if args.ignore:
			return None
		else:
			parser.error("file value: variable '"+func_args[0]+"' in file '"
				+args.file.name+"' is not joinable: [Errno 2] "+str(err))
	else:
		return func_args[1].join(vars[func_args[0]])

#TODO: add r_getvar and r_join which recursively interpret the values they 
#  output and WATCH OUT for endless recursion

#TODO: add ec_classpath which reads a .classpath file created by Eclipse and 
#  puts it in variables. 

fncs = {
	"": get_var,
	"join": join,
}