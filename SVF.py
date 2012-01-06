#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3.2 code
#
# SVF - Strings/Variables/Function
# version 0.3
# This commandline tool reads a data-file with name-value pairs, 
# and outputs the value of the specified name with some special parts 
# substituted. 
#
# Known encoding issue: Please note that Python cannot handle a BOM in a UTF-8
# encoded file. 
#
# I've tried to keep almost everything in this tool configurable and/or 
# extendable. This includes:
# - The kind of data-file, although currently only the json format is supported.
#   Planned support for formats: ini, plist (with some restrictions)
# - The special characters for identifying to be substituted part, although
#   only changable in this file. Perhaps commandline changability will be added.
# - The functions which can be used, found in SVF_functions. Planned functions 
#   are functions which interpret any newly pasted values. But those will need 
#   a recursion guard. And I plan to write a function which can read a 
#   .classpath file created by Eclipse. 

import argparse
import json
import re

from SVF_functions import fncs
from SVF_parsers import psrs

interpret_chars = ['!', ':', '&']

def main():
	global parser
	parser = get_parser()
	
	global args
	args = parser.parse_args()
	
	global vars
	try:
		vars = psrs[args.format](args, parser)
	except KeyError:
		parser.error("argument -a/--format: can't find a function for format "
			"'"+args.format+"': [Errno 2] KeyError: '"+args.format+"'")
	
	args.file.close()
	
	try:
		print(interpret(vars[args.var]))
	except KeyError:
		parser.error("argument -v/--var: can't find variablename '"+args.var+"' in "
			"file '"+args.file.name+"': [Errno 2] KeyError: '"+args.var+"'")

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
		choices=('gen', 'json'), help="Format of the input FILE, possible values: "
		"(%(choices)s), default: %(default)s", metavar="FORMAT", 
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
		version="%(prog)s 0.2")
	
	return parser

def func_map(match):
	global interpret_chars
	global parser
	global args
	global vars
	
	if match.group(1) == None:
		func_name = ""
	else:
		func_name = match.group(1)
	
	if match.group(2) == None:
		ret = fncs[func_name]()
	else:
		ret = fncs[func_name](args, vars, parser, 
			match.group(2).split(interpret_chars[2]))
	
	if ret == None:
		return match.group(0)
	else:
		return ret

def interpret(string):
	global interpret_chars
	pattern = re.compile(interpret_chars[0]+r"([A-Za-z0-9_.]*)"+interpret_chars[1]
		+r"([A-Za-z0-9.,;'\"\/_+~@#$%^&*|]*)"+interpret_chars[0])
	return pattern.sub(func_map, string)

if __name__ == "__main__":
	main()