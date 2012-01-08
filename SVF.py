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
# This is just a wrapper file which imports everything. Check the files
# for a small documentation on their functionality. 

from SVF_class import SVF
import SVF_parsers
import SVF_functions

if __name__ == "__main__":
	SVF.init()