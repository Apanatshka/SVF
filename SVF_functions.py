#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3.2 code
#
# SVF_functions
# Functions for the SVF commandline tool for interpreting the statements

from SVF_class import SVF
import copy

def get_var(vars, func_args, callback = None):
	args = SVF.args
	err  = SVF.parser.error
	vars = copy.deepcopy(vars)
	def listtostr(list):
		return str(list[0])+"["+("][".join(list[1:]))+"]"
	
	cur_vars = vars
	for i in range(len(func_args)-1):
		try:
			cur_vars = cur_vars[func_args[i]]
		except KeyError:
			if args.ignore:
				return None
			else:
				#print("functions: 25")#debug
				err("file value: can't find variablename '"+listtostr(func_args[0:i])+
					"' in file '"+args.file.name+"': [Errno 2] KeyError: '"+func_args[i]
					+"'")
				return
	
	try:
		var = copy.copy(cur_vars[func_args[len(func_args)-1]])
	except KeyError:
		if args.ignore:
			return None
		else:
			#print("functions: 35")#debug
			err("file value: can't find variablename '"+listtostr(func_args)+
					"' in file '"+args.file.name+"': [Errno 2] KeyError: '"
					+func_args[len(func_args)-1]+"'")
			return
	del cur_vars[func_args[len(func_args)-1]]
	
	if callback != None:
		return callback(vars, func_args, var)
	else:
		return var

def join(vars, func_args, callback = None):
	args = SVF.args
	err  = SVF.parser.error
	try:
		iter(vars[func_args[0]])
	except KeyError:
		if args.ignore:
			return None
		else:
			#print("functions: 55")#debug
			err("file value: can't find variablename '"+func_args[0]+"' in "
				"file '"+args.file.name+"': [Errno 2] KeyError: '"+func_args[0]+"'")
	except TypeError as exc:
		if args.ignore:
			return None
		else:
			err("file value: variable '"+func_args[0]+"' in file '"
				+args.file.name+"' is not joinable: [Errno 2] "+str(exc))
	else:
		if callback != None:
			return func_args[1].join(
				callback(vars, func_args, x) for x in vars[func_args[0]])
		else:
			return func_args[1].join(vars[func_args[0]])

def q(vars, func_args, to_quote):
	return '"'+to_quote+'"'

def sq(vars, func_args, to_quote):
	return "'"+to_quote+"'"

def r(vars, func_args, to_reinterpret):
	return SVF.interpret(to_reinterpret, vars)

#TODO: add ec_classpath which reads a .classpath file created by Eclipse and 
#  puts it in variables. 

functions = {
	'':       get_var,
	'join':   join,
	'q':      lambda x,y: get_var(x,y,q),
	'sq':     lambda x,y: get_var(x,y,sq),
	'r':      lambda x,y: get_var(x,y,r),
	'qjoin':  lambda x,y: join(x,y,q),
	'sqjoin': lambda x,y: join(x,y,sq),
	'rjoin':  lambda x,y: join(x,y,r),
}

for name in functions:
	SVF.functions[name] = functions[name]