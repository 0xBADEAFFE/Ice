#!/usr/bin/env python
# encoding: utf-8
"""
Emulator.py

Created by Scott on 2013-01-04.
Copyright (c) 2013 Scott Rice. All rights reserved.

Emulator is the base class of all my emulators.

Functionality should be added here if every single emulator (whether downloaded
or not) would use it
"""

import sys
import os
import urllib
import tempfile
import shutil
from ice import settings

import abc

class Emulator(object):
    __metaclass__ = abc.ABCMeta
    
    # directory should be set by any subclasses which manage where emulators
    # are stored (such as the Downloaded Emulator class)
    directory = ""
    
    # Location should be set by any subclasses which manage where emulators
    # are stored (such as the Downloaded Emulator class)
    location = ""
    
    # Since one emulator may handle many consoles, it is important to make sure
    # we specify which console we are having the emulator handle currently
    def __init__(self,console_name):
        self._console_name_ = console_name
        self.set_control_scheme(settings.controls()[console_name])
    
    @abc.abstractmethod
    def set_control_scheme(self,controls):
        """
        Sets the control scheme of the emulator to be the one designated by
        'controls'. This method should avoid doing any serious work on the value
        of 'controls' at a given point, so that the user can specify exactly
        what they want.
        """
        pass
        
    def is_functional(self):
        """
        A basic emulator is always functional.
        """
        return True
        
    def valid_rom(self,path):
        """
        This function determines if a given path is actually a valid ROM file.
        There are many different file extensions that could be used as ROMs,
        and it would be a pretty bad user experience if a valid rom got ignored
        by Ice, so I will err on the side of "Valid". The exception to this is
        bsnes, whose functionality should be described in it's class
        """
        return True
    
    @abc.abstractmethod
    def command_string(self):
        """
        Returns the string which is used by Steam to launch the Emulator+ROM
        """
        return
        
    def startdir(self,rom):
        """
        Returns the directory which stores the emulator. This value is useful
        as the 'StartDir' option of a Steam Shortcut
        """
        return os.path.dirname(self.location)
        
    def replace_contents_of_file(self,file_path,replacement_function):
        """
        Replaces the contents of a file with the results of replacement_function
        
        'replacement_function' is a function which takes a line of input and
        returns another line, which gets put in the new file.
        """
        # Code mainly taken from:
        # http://stackoverflow.com/questions/39086/search-and-replace-a-line-in-a-file-in-python
        fh, abs_path = tempfile.mkstemp()
        new_file = open(abs_path,'w')
        old_file = open(file_path)
        for line in old_file:
            new_file.write(replacement_function(line))
        # Close handles
        new_file.close()
        os.close(fh)
        old_file.close()
        # Replace file_path with new file
        os.remove(file_path)
        shutil.move(abs_path, file_path)