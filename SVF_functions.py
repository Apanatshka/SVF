#!/usr/bin/python
#
#
# SVF_functions
# version 0.1
# Functions for the SVF commandline tool

def get_var(cl_args, vars, var_name):
	if var_name in vars:
		return vars[var_name]
	#planned functionality: print errors
	#planned functionality: be robust
	else:
		pass

def join(cl_args, vars, var_name, glue):
	if var_name in vars:
		return glue.join(vars[var_name])
	#planned functionality: print errors
	#planned functionality: be robust
	else:
		pass

fncs = {
	"": get_var,
	"join": join,
}