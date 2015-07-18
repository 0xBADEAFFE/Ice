
import mock
import os
import shutil
import tempfile
import unittest

from ice import rom_finder


class ROMFinderTests(unittest.TestCase):

  def setUp(self):
    self.mock_console = mock.MagicMock()
    self.mock_config = mock.MagicMock()
    self.mock_filesystem = mock.MagicMock()
    self.mock_parser = mock.MagicMock()
    self.rom_finder = rom_finder.ROMFinder(
      self.mock_config,
      self.mock_filesystem,
      self.mock_parser,
    )

  def tearDown(self):
    pass

  def test_roms_for_console_returns_a_rom_for_every_file_in_roms_directory(
          self):
    dirname = "RandomDir"
    rom1 = os.path.join(dirname, "rom1")
    rom2 = os.path.join(dirname, "rom2")
    rom3 = os.path.join(dirname, "rom3")
    rom_paths = [rom1, rom2, rom3]
    self.mock_console.is_valid_rom.return_value = True
    self.mock_config.roms_directory_for_console.return_value = dirname
    self.mock_filesystem.files_in_directory.return_value = rom_paths

    roms = self.rom_finder.roms_for_console(self.mock_console)
    self.assertEquals(len(roms), 3)
    for rom in roms:
      self.assertIn(rom.path, rom_paths)
      self.assertEquals(rom.console, self.mock_console)

  def test_roms_for_console_ignores_invalid_roms(self):
    dirname = "RandomDir"
    rom1 = os.path.join(dirname, "rom1")
    rom2 = os.path.join(dirname, "rom2")
    rom3 = os.path.join(dirname, "rom3")
    rom_paths = [rom1, rom2, rom3]
    self.mock_console.is_valid_rom.return_value = False
    self.mock_config.roms_directory_for_console.return_value = dirname
    self.mock_filesystem.files_in_directory.return_value = rom_paths

    self.assertEquals([], self.rom_finder.roms_for_console(self.mock_console))

  def test_roms_for_console_returns_nothing_for_disabled_consoles(self):
    dirname = "RandomDir"
    rom1 = os.path.join(dirname, "rom1")
    rom2 = os.path.join(dirname, "rom2")
    rom3 = os.path.join(dirname, "rom3")
    rom_paths = [rom1, rom2, rom3]
    self.mock_filesystem.files_in_directory.return_value = rom_paths

    console = mock.MagicMock()
    console.is_enabled.return_value = False
    self.assertEquals(self.rom_finder.roms_for_console(console), [])

  def test_roms_for_consoles_returns_roms_in_subdirs(self):
    firstdir = "RandomDir"
    rom1 = os.path.join(firstdir, "rom1")
    subdir = "RandomSubdir"
    rom2 = os.path.join(subdir, "rom2")
    rom_paths = [rom1, rom2]

    def fake_files_in_directory(dirname, include_subdirectories):
      self.assertTrue(include_subdirectories)
      return rom_paths
    self.mock_filesystem.files_in_directory.side_effect = fake_files_in_directory

    # No matter what the console is tell it to check firstdir
    self.mock_config.roms_directory_for_console.return_value = firstdir

    # Doesn't matter what 'console' we throw in here, we're always going
    # to return firstdir
    roms = self.rom_finder.roms_for_consoles([mock.MagicMock()])
    self.assertEquals(len(roms), 2)
    [self.assertIn(rom.path, rom_paths) for rom in roms]

  def test_roms_for_consoles_returns_collection_of_all_roms(self):
    firstdir = "RandomDir"
    rom1 = os.path.join(firstdir, "rom1")
    rom2 = os.path.join(firstdir, "rom2")
    seconddir = "RandomDir2"
    rom3 = os.path.join(seconddir, "rom3")
    rom_paths = [rom1, rom2, rom3]

    def fake_files_in_directory(dirname, include_subdirectories):
      return [rom1, rom2] if dirname == firstdir else [rom3]
    self.mock_filesystem.files_in_directory.side_effect = fake_files_in_directory

    console1 = mock.MagicMock()
    console2 = mock.MagicMock()
    def fake_roms_directory_for_console(console):
      return firstdir if console == console1 else seconddir
    self.mock_config.roms_directory_for_console.side_effect = fake_roms_directory_for_console
    both_consoles = [console1, console2]

    roms = self.rom_finder.roms_for_consoles([console1])
    self.assertEquals(len(roms), 2)
    for rom in roms:
      self.assertIn(rom.path, rom_paths)
      self.assertEquals(rom.console, console1)

    roms = self.rom_finder.roms_for_consoles(both_consoles)
    self.assertEquals(len(roms), 3)
    for rom in roms:
      self.assertIn(rom.path, rom_paths)
      self.assertIn(rom.console, both_consoles)

  def test_uses_parser_to_determine_rom_name(self):
    dirname = "RandomDir"
    rom1 = os.path.join(dirname, "rom1")
    rom_paths = [rom1]
    self.mock_console.is_valid_rom.return_value = True
    self.mock_config.roms_directory_for_console.return_value = dirname
    self.mock_filesystem.files_in_directory.return_value = rom_paths
    self.mock_parser.parse.return_value = "ROM Name"

    roms = self.rom_finder.roms_for_console(self.mock_console)
    self.assertEquals(len(roms), 1)
    returned_rom = roms[0]
    self.assertEquals(returned_rom.name, "ROM Name")
