# encoding: utf-8
"""
_shortcut_parser.py

Created by Scott on 2013-12-29.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import struct
import os
import re

from steam_model import Shortcut

class ShortcutParser(object):

  def parse(self, path, require_exists=False):
    if not os.path.exists(path):
      if not require_exists:
        return []
      raise IOError("Shortcuts file '%s' does not exist" % path)

    file_contents = open(path, "r").read()
    return self.match_base(file_contents)

  def match_base(self,string):
    match = re.match(ur"\u0000shortcuts\u0000(.*)\u0008\u0008$",string, re.IGNORECASE)
    if match:
        return self.match_array_string(match.groups()[0])
    else:
        return None

  def match_array_string(self,string):
    # Match backwards (aka match last item first)
    if string == "":
      return []
    # One side effect of matching this way is we are throwing away the
    # array index. I dont think that it is that important though, so I am
    # ignoring it for now
    shortcuts = []
    while True:
      match = re.match(ur"(.*)\u0000[0-9]+\u0000(\u0001AppName.*)\u0008",string, re.IGNORECASE)
      if match:
        groups = match.groups()
        string = groups[0]
        shortcuts.append(self.match_shortcut_string(groups[1]))
      else:
        shortcuts.reverse()
        return shortcuts

  def match_shortcut_string(self,string):
    # I am going to cheat a little here. I am going to match specifically
    # for the shortcut string (Appname, Exe, StartDir, etc), as opposed
    # to matching for general Key-Value pairs. This could possibly create a
    # lot of work for me later, but for now it will get the job done
    pattern = (
        ur"\u0001AppName\u0000(.*)\u0000"                               # groups[0]  appname
        ur"\u0001exe\u0000(.*)\u0000"                                   # groups[1]  exe
        ur"\u0001StartDir\u0000(.*)\u0000"                              # groups[2]  startdir
        ur"\u0001icon\u0000(.*)\u0000"                                  # groups[3]  icon
        ur"\u0001ShortcutPath\u0000(.*)\u0000"                          # groups[4]  shortcut path
        ur"\u0001LaunchOptions\u0000(.*)\u0000"                         # groups[5]  launch options
        ur"\u0002IsHidden\u0000(\u0000|\u0001)(?:\u0000){3}"            # groups[6]  hidden
        ur"\u0002AllowDesktopConfig\u0000(\u0000|\u0001)(?:\u0000){3}"  # groups[7]  allow_desktop_config
        ur"\u0002OpenVR\u0000(\u0000|\u0001)(?:\u0000){3}"              # groups[8]  open_vr
        ur"\u0002LastPlayTime\u0000(.{4})"                              # groups[9]  last_play_time
        ur"\u0000tags\u0000(.*)"                                        # groups[10] tags
        ur"\u0008"                                                      # end
    )
    match = re.match(pattern, string, re.IGNORECASE)
    if match:
      # The 'groups' that are returned by the match should be the data
      # contained in the file. Now just make a Shortcut out of that data
      groups = match.groups()
      return Shortcut(
          groups[0],
          groups[1],
          groups[2],
          groups[3],
          groups[4],
          groups[5],
          groups[6] == '\x01',
          groups[7] == '\x01',
          groups[8] == '\x01',
          struct.unpack('<i', groups[9])[0],
          self.match_tags_string(groups[10])
      )
    else:
      print("Unable to parse shortcuts.vdf, try adding a shortcut in steam to ensure latest file format")
      print(string)
      exit()
      return None

  def match_tags_string(self,string):
    tags = []
    while True:
      match = re.match(ur"(.*)\u0001[0-9]+\u0000(.*?)\u0000",string)
      if match:
        groups = match.groups()
        string = groups[0]
        tag = groups[1]
        tags.append(tag)
      else:
        tags.reverse()
        return tags
