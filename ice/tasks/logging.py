#!/usr/bin/env python
# encoding: utf-8

from ice.logs import logger

# TODO(#368); This shouldn't be necessary as part of the app. We shouldn't be
# relying on log messages as our UI
class LogAppStateTask(object):
  def __init__(self, app_settings):
    self.app_settings = app_settings

  def __call__(self, users, roms, dry_run):
    for emulator in self.app_settings.emulators:
      logger.info("Detected Emulator: %s" % emulator.name)

    for console in self.app_settings.consoles:
      logger.info("Detected Console: %s => %s" % (console.fullname, console.emulator.name))

    user_ids = map(lambda u: u.user_id, users)
    logger.info("===== Running for users: %s =====" % ", ".join(user_ids))
