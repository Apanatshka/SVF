#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3.2 code
#
# SVF_functions
# version 0.2
# Functions for the SVF commandline tool for interpreting the statements

def get_var(cl_args, vars, parser, var_name):
	if var_name in vars:
		return vars[var_name]
	elif cl_args.robust:
		return None
	else:
		parser.error("file value: can't find variablename '"+var_name+"' in "
			"file '"+cl_args.file.name+"': [Errno 2] KeyError: '"+var_name+"'")

def join(cl_args, vars, parser, var_name, glue):
	if var_name in vars:
		try:
			iter(vars[var_name])
		except TypeError as err:
			if cl_args.robust:
				return None
			else:
				parser.error("file value: variable '"+var_name+"' in file '"
					+cl_args.file.name+"' is not joinable: [Errno 2] "+str(err))
		else:
			return glue.join(vars[var_name])
	elif cl_args.robust:
		return None
	else:
		parser.error("file values: can't find variablename '"+var_name+"' in "
			"file '"+cl_args.file.name+"': [Errno 2] KeyError: '"+var_name+"'")

fncs = {
	"": get_var,
	"join": join,
}