"""
command_line_runner.py

Created by Scott on 2014-08-14.
Copyright (c) 2014 Scott Rice. All rights reserved.
"""

from pysteam.steam import Steam

from ice.error.config_error import ConfigError

from ice.steam_shortcut_manager import SteamShortcutManager

from ice import filesystem_helper as fs
from ice import console
from ice import emulator
from ice import utils
from ice.rom_manager import IceROMManager
from ice.ice_logging import ice_logger

class CommandLineRunner(object):

    def main(self, argv):
        if utils.steam_is_running():
            ice_logger.error("Ice cannot be run while Steam is open. Please close Steam and try again")
            return

        ice_logger.log("Starting Ice")
        ice_logger.log_state_of_the_world(emulator.Emulator.all(), console.Console.all())
        steam = Steam()
        # Find all of the ROMs that are currently in the designated folders
        roms = console.find_all_roms()
        # Find the Steam Account that the user would like to add ROMs for
        users = steam.local_users()
        for user in users:
            ice_logger.log("Running for user %s" % str(user.id32))
            # Load their shortcuts into a SteamShortcutManager object
            shortcuts_manager = SteamShortcutManager(user.shortcuts_file())
            rom_manager = IceROMManager(shortcuts_manager)
            # Add the new ROMs in each folder to our Shortcut Manager
            rom_manager.sync_roms(roms)
            # Backup the current shortcuts.vdf file
            shortcuts_manager.backup(user.id32)
            # Generate a new shortcuts.vdf file with all of the new additions
            shortcuts_manager.save()
            rom_manager.update_artwork(user, roms)
        ice_logger.log('Ice finished')

    def run(self, argv):
      try:
          self.main(argv)
      except ConfigError as error:
          ice_logger.error('Stopping')
          ice_logger.log_config_error(error)
          ice_logger.exception()
      except StandardError as error:
          ice_logger.exception()
      # Keeps the console from closing (until the user hits enter) so they can
      # read any console output
      print ""
      print "Close the window, or hit enter to exit..."
      raw_input()
