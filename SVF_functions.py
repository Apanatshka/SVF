#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3.2 code
#
# SVF_functions
# version 0.3
# Functions for the SVF commandline tool for interpreting the statements

def get_var(args, vars, parser, var_name):
	try:
		return vars[var_name]
	except KeyError:
		if args.ignore:
			return None
		else:
			parser.error("file value: can't find variablename '"+var_name+"' in "
				"file '"+args.file.name+"': [Errno 2] KeyError: '"+var_name+"'")

def join(args, vars, parser, var_name, glue):
	try:
		iter(vars[var_name])
	except KeyError:
		if args.ignore:
			return None
		else:
			parser.error("file value: can't find variablename '"+var_name+"' in "
				"file '"+args.file.name+"': [Errno 2] KeyError: '"+var_name+"'")
	except TypeError as err:
		if args.ignore:
			return None
		else:
			parser.error("file value: variable '"+var_name+"' in file '"
				+args.file.name+"' is not joinable: [Errno 2] "+str(err))
	else:
		return glue.join(vars[var_name])

fncs = {
	"": get_var,
	"join": join,
}