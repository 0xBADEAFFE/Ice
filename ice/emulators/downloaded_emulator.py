#!/usr/bin/env python
# encoding: utf-8
"""
downloaded_emulator.py

Created by Scott on 2013-01-04.
Copyright (c) 2013 Scott Rice. All rights reserved.

DownloadedEmulator represents an emulator which I download from a specific 
location. This location should be defined in the emulator subclass as opposed
to as a parameter, as I dont think it would be possible to create a class
suitable for all cases if it was a parameter

Functionality should be added here if it involves the downloading of emulators,
or if it involves managing the downloaded emulators
"""

import os
import sys
import abc
import stat
import shutil
import urllib
import zipfile

import IceFilesystemHelper
from IceLogging import log

import emulator

class DownloadedEmulator(emulator.Emulator):
    __metaclass__ = abc.ABCMeta    
    
    # Should be overwritten by a subclass
    #
    # Describes the URL at which the emulator zip file can be found
    _download_location_ = None
    
    # Should be overwritten by a subclass
    #
    # Describes a list of relative paths inside the zip file which should have
    # their executable bit set. This is only applicable on Mac and Linux.
    _executable_files_ = []
    
    # Should be overwritten by a subclass
    #
    # Describes the location inside of the zip file of the emulator executable.
    # This will be used to set the final location variable after unzipping has
    # finished
    _relative_exe_path_ = None
    
    def __init__(self,console_name):
        assert self._download_location_, "Download Location must be defined for all subclasses of DownloadedEmulator"
        assert self._relative_exe_path_, "Relative Exe Path must be defined for all subclasses of DownloadedEmulator"
        self._directory_name_ = IceFilesystemHelper.highest_directory_in_path(self._relative_exe_path_)
        # Download the emulator
        self._download_()
        super(DownloadedEmulator,self).__init__(console_name)
        
    def _download_(self):
        emulators_dir = IceFilesystemHelper.downloaded_emulators_directory()
        zips_dir = IceFilesystemHelper.downloaded_zips_directory()
        # Make sure the directorys exists
        IceFilesystemHelper.create_directory_if_needed(emulators_dir)
        IceFilesystemHelper.create_directory_if_needed(zips_dir)
        url = self._download_location_
        zip_path = os.path.join(IceFilesystemHelper.downloaded_zips_directory(),os.path.basename(url))
        # If we have downloaded (and therefore extracted) the zip file before,
        # there is no reason to do it again
        if not os.path.exists(zip_path):
            log("Downloading %s" % url)
            (downloaded_path,headers) = urllib.urlretrieve(url)
            log("Finished downloading %s" % url)
            shutil.copyfile(downloaded_path,zip_path)
            self._unzip_(downloaded_path,emulators_dir)
        self.location = os.path.join(emulators_dir,self._relative_exe_path_)
        self.directory = os.path.join(emulators_dir,self._directory_name_)

    def _unzip_(self,file,destdir):
        log("Unzipping %s to %s" % (file,destdir))
        z = zipfile.ZipFile(file)
        for f in z.namelist():
            # Zipfiles store paths internally using a forward slash. If os.sep
            # is not a forward slash, then we will compute an incorrect path.
            # Fix that by replacing all forward slashes with backslashes if
            # os.sep is a backslash
            if os.sep == "\\" and "/" in f:
                destfile = os.path.join(destdir,f.replace("/","\\"))
            else:
                destfile = os.path.join(destdir,f)
            if destfile.endswith(os.sep):
                if not os.path.exists(destfile):
                    os.makedirs(destfile)
            else:
                file = open(destfile,"wb")
                file.write(z.read(f))
                file.close()
        z.close()
        self._set_execute_permissions_()
        
    def _set_execute_permissions_(self):
        """
        Apparently permissions aren't preserved in zip files, so I need to
        manually make sure that the executable has the +x bit set. This section
        is completely unnecessary on Windows, and Windows emulators should leave
        _executable_files_ empty
        """
        for x_file in self._executable_files_:
            log("Setting executable permission on %s" % x_file)
            # Get the full path
            file_path = os.path.join(destdir,x_file)
            # Taken from StackOverflow answer: 
            # http://stackoverflow.com/questions/12791997/how-do-you-do-a-simple-chmod-x-from-within-python
            st = os.stat(file_path)
            os.chmod(file_path, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)