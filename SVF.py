#!/usr/bin/python
#
#
# SVF - Strings/Variables/Function
# version 0.1
# This commandline tool reads a data-file with name-value pairs, 
# and outputs the value of the specified name with some special parts 
# substituted. 
#
# I"ve tried to keep almost everything in this tool configurable and/or 
# extendable. This includes:
# - The kind of data-file
# - The special characters for identifying to be substituted part
# - The functions which can be used

import argparse
import json
import re

from SVF_functions import fncs

def main():
	global args
	args = get_args()
	global vars
	vars = json.load(args.file)
	args.file.close()
	if args.var in vars:
		print(interpret(vars[args.var]))
	#planned functionality: print errors
	else:
		pass

def get_args():
	parser = argparse.ArgumentParser(description="Reads a data-file with "
		"name-value pairs, and outputs the value of the specified name with the "
		"denoted parts substituted according. ", prog="svf", 
		usage="svf [options] -f FILE -v VAR", add_help=False)
	
	option_args = parser.add_argument_group(title="optional arguments")
	
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
		version="%(prog)s 0.1")
	
	return parser.parse_args()

def func_map(match):
	global args
	global vars
	
	if match.group(1) == None:
		func_name = ""
	else:
		func_name = match.group(1)
	
	if match.group(2) == None:
		return fncs[func_name]()
	else:
		return fncs[func_name](args, vars, *match.group(2).split("."))

def interpret(string):
	pattern = re.compile(r"!([A-Za-z_.]*):([A-Za-z.,;'\"\/_+~@#$%^&*|]*)")
	return pattern.sub(func_map, string)

if __name__ == "__main__":
	main()