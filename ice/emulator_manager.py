#!/usr/bin/env python
# encoding: utf-8
"""
emulator_manager.py

Created by Scott on 2013-01-04.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os
import settings

from emulators import *

# List of emulators to use for each conole
#
# I was originally going to include a Dreamcast emulator, but none of the
# emulators that I looked at seemed good. The sound especially was super
# buggy. It was most likely because I was on Windows 7, but I want to provide
# a good experience to Win7 as well, so I won't support Dreamcast for now.
#
# I was also originally going to include a Wii emulator, since Dolphin already
# includes Wii support, but it occured to me that the main use case for this
# application was using an Xbox 360 controller with Steam Big Picture, and
# since Wii emulation would require a Wiimote, I figured it didn't make sense
# to include it.
platform = settings.platform_string()
if platform == "Windows":
    emulators = {
        "NES":          winbsnes.Winbsnes("NES"),
        "SNES":         winbsnes.Winbsnes("SNES"),
        "N64":          winproject64.WinProject64("N64"),
        "Gamecube":     windolphin.WinDolphin("Gamecube"),
        "PS1":          winepsxe.WinePSXe("PS1"),
        "PS2":          winpcsx2.WinPCSX2("PS2"),
        "Genesis":      wingens.WinGens("Genesis"),
        "Gameboy":      winbsnes.Winbsnes("Gameboy"),
        "GBA":          winvisualboyadvance.WinVisualBoyAdvance("GBA"),
    }
if platform == "OSX":
    emulators = {
        "NES":          macmednafen.MacMednafen("NES"),
        "SNES":         macsnes9x.MacSnes9x("SNES"),
        # "N64":          ,
        # "Gamecube":     ,
        # "PS1":          ,
        # "PS2":          ,
        "Genesis":      macmednafen.MacMednafen("Genesis"),
        "Gameboy":      macmednafen.MacMednafen("Gameboy"),
        "GBA":          macmednafen.MacMednafen("GBA"),
    }
if platform == "Linux":
    emulators = {
        # "NES":          ,
        # "SNES":         ,
        # "N64":          ,
        # "Gamecube":     ,
        # "PS1":          ,
        # "PS2":          ,
        # "Genesis":      ,
        # "Gameboy":      ,
        # "GBA":          ,
    }

def emulator_exists(platform,console):
    return lookup_emulator(platform,console) is not None
        
def lookup_emulator(platform,console):
    try:
        return emulators[console.shortname]
    except KeyError:
        return None