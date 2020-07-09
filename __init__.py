import sys
import os

# add plugin to python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import console_plugin
console_plugin.args = args

import console_plugin.console

