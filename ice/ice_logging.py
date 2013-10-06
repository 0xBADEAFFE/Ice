#!/usr/bin/env python
# encoding: utf-8
"""
IceLogging.py

Created by Scott on 2013-01-24.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os
import time
import traceback

def log_file_path():
    """Directory to store the log file"""
    # http://stackoverflow.com/questions/279237/python-import-a-module-from-a-folder
    current_directory = os.path.dirname(sys.modules['__main__'].__file__)
    return os.path.join(current_directory,"log.txt")

def log_timestamp_str():
    """
    Returns a nice string that represents the current time for use in logging
    
    Example:
    [1/24/2013 13:01:30]
    """
    time_str = time.strftime("%m/%d/%y %H:%M:%S")
    return "[%s]" % time_str
        
def log_user(s):
    """
    Logs the string s to the user
    """
    print s
    
def log_file(s):
    """
    Logs the string s in a file, defined in filesystem_helper
    """
    f = open(log_file_path(),"a")
    f.write("%s %s\n" % (log_timestamp_str(),s))
    f.close()
    
def log_both(s):
    """
    Logs the string s to both the user and to a file
    """
    log_user(s)
    log_file(s)
    
def log_exception():
    traceback.print_exc(file=open(log_file_path(),"a"))