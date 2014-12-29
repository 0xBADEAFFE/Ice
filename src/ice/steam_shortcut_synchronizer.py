
from rom import ICE_FLAG_TAG

class SteamShortcutSynchronizer(object):

  def __init__(self, logger):
    self.logger = logger

  def shortcut_is_managed_by_ice(self, shortcut):
    return ICE_FLAG_TAG in shortcut.tags

  def unmanaged_shortcuts(self, shortcuts):
    return filter(lambda shortcut: not self.shortcut_is_managed_by_ice(shortcut), shortcuts)

  def removed_shortcuts(self, current_shortcuts, new_shortcuts):
    # To get the list of only removed shortcuts we take all of the current
    # shortcuts and filter out any that exist in the new shortcuts
    return filter(lambda shortcut: shortcut not in new_shortcuts, current_shortcuts)

  def added_shortcuts(self, current_shortcuts, new_shortcuts):
    # To get the list of only added shortcuts we take all of the new shortcuts
    # and filter out any that existed in the current shortcuts
    return filter(lambda shortcut: shortcut not in current_shortcuts, new_shortcuts)

  def sync_roms_for_user(self, user, roms):
    """
    This function takes care of syncing ROMs. After this function exits,
    Steam will contain only non-Ice shortcuts and the ROMs represented
    by `roms`.
    """
    # 'Unmanaged' is just the term I am using for shortcuts that the user has
    # added that Ice shouldn't delete. For example, something like a shortcut
    # to Plex would be 'Unmanaged'
    unmanaged_shortcuts = self.unmanaged_shortcuts(user.shortcuts)
    current_ice_shortcuts = filter(lambda shortcut: shortcut not in unmanaged_shortcuts, user.shortcuts)
    # Generate a list of shortcuts out of our list of ROMs
    rom_shortcuts = map(lambda rom: rom.to_shortcut(), roms)
    # Calculate which ROMs were added and which were removed so we can inform
    # the user
    removed = self.removed_shortcuts(current_ice_shortcuts, rom_shortcuts)
    map(lambda shortcut: self.logger.info("Removing ROM: `%s`" % shortcut.name), removed)
    added = self.added_shortcuts(current_ice_shortcuts, rom_shortcuts)
    map(lambda shortcut: self.logger.info("Adding ROM: `%s`" % shortcut.name), added)

    # Set the updated shortcuts
    user.shortcuts = unmanaged_shortcuts + rom_shortcuts
