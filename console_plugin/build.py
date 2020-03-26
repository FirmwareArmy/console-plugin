import shutil
import os
import extargparse
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
print(sys.path)
import console_plugin.build_commands.console

def init_parser(parentparser, config):
    group = None
    for action in parentparser._choices_actions:
        if hasattr(action, 'id') and action.id=='build':
            group = action

    # init sub parsers
    console_plugin.build_commands.console.init_parser(group, config)

