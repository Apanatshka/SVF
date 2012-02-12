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
# SVF - Strings/Variables/Function
# This commandline tool reads a data-file with name-value pairs, 
# and outputs the value of the specified name with some special parts 
# substituted. 
#
# Known encoding issue: Please note that Python cannot handle a BOM in a UTF-8
# encoded file. 
#
# I've tried to keep almost everything in this tool configurable and/or 
# extendable. This includes:
# - The kind of data-file (parsers are found in SVF_parsers), although currently
#   only the json format is supported. 
# - The special characters for identifying to be substituted part, although
#   only changable in this file. 
# - The functions which can be used, found in SVF_functions. 

import argparse
import json
import re
import copy

class SVF:
	"""SVF static class wrapper"""
	
	interpret_chars = ('!', ':', '&')
	functions       = {}
	parsers         = {}
	version         = "0.4"
	
	def init():
		parser = SVF.parser = SVF.get_parser()
		
		args = SVF.args = parser.parse_args()
		
		try:
			vars = SVF.vars = SVF.parsers[args.format]()
		except KeyError:
			parser.error("argument -a/--format: can't find a function for format "
				"'"+args.format+"': [Errno 2] KeyError: '"+args.format+"'")
		
		args.file.close()
		
		interpret_chars = SVF.interpret_chars
		SVF.pattern = re.compile(interpret_chars[0]+r"([A-Za-z0-9_.]*)"
			+interpret_chars[1]+r"([A-Za-z0-9.,;'\"\/_+~@#$%^&*|]*)"
			+interpret_chars[0])
		
		try:
			var = copy.copy(vars[args.var])
		except KeyError:
			#print("class: 62")#debug
			parser.error("argument -v/--var: can't find variablename '"+args.var+
				"' in file '"+args.file.name+"': [Errno 2] KeyError: '"+args.var+"'")
		del vars[args.var]
		print(SVF.interpret(var, vars))

	def get_parser():
		parser = argparse.ArgumentParser(description="Reads a data-file with "
			"name-value pairs, and outputs the value of the specified name with the "
			"denoted parts substituted according. ", prog="svf", 
			usage="svf [options] -f FILE -v VAR", add_help=False)
		
		option_args = parser.add_argument_group(title="optional arguments")
		
		option_args.add_argument("-i", "--ignore", action="store_true", 
			help="Don't throw errors on uninterpretable statements, "
			"simply leave them alone. ", dest="ignore")
		
		option_args.add_argument("-a", "--format", default="gen", 
			choices=('gen', 'json'), help="Format of the input FILE, possible values:"
			" (%(choices)s), default: %(default)s", metavar="FORMAT", 
			dest="format")
		
		required_args = parser.add_argument_group(title="required arguments")
		
		required_args.add_argument("-f", "--file", type=argparse.FileType("r"), 
			required=True, help="File with name-value pairs to be read. ", 
			metavar="FILE", dest="file")
		
		required_args.add_argument("-v", "--var", required=True, 
			help="Variable name to be interpreted and outputted. ", metavar="VAR", 
			dest="var")
		
		
		other_args = parser.add_argument_group(title="additional arguments")
		
		other_args.add_argument("-h", "--help", action="help", 
			help="show this help message and exit")
		
		other_args.add_argument("--version", action="version", 
			version="%(prog)s "+SVF.version)
		
		return parser

	def func_map(match, vars):
		functions = SVF.functions
		args = SVF.args
		
		if match.group(1) == None:
			func_name = ""
		else:
			func_name = match.group(1)
		
		if match.group(2) == None:
			ret = functions[func_name](vars, [])
		else:
			ret = functions[func_name](vars, 
				match.group(2).split(SVF.interpret_chars[2]))
		
		if ret == None:
			if args.ignore:
				return match.group(0)
			elif args.clear:
				return ""
			else:
				raise Exception("You're not supposed to see this error")
		else:
			return ret

	def interpret(string, vars):
		return SVF.pattern.sub(lambda x: SVF.func_map(x, vars), string)