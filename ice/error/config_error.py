#!/usr/bin/env python
# encoding: utf-8
"""
config_error.py

Created by Scott on 2013-05-23.
Copyright (c) 2013 Scott Rice. All rights reserved.
"""

import sys
import os

class ConfigError(StandardError):
    def __init__(self,fix_instructions,referenced_config):
        self.fix_instructions = fix_instructions
        self.referenced_config = referenced_config
        
    def __str__(self):
        return repr("%s || %s" % (self.fix_instructions, self.referenced_config))