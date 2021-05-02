from army.api.command import parser, group, command, option, argument
from army.api.debugtools import print_stack
from army.api.log import log, get_log_level
from army.api.package import load_project_packages, load_installed_package
from army.api.project import load_project
import os
import re
# from subprocess import Popen, PIPE, STDOUT
import subprocess
import sys
import shutil
from time import sleep

def to_relative_path(path):
    home = os.path.expanduser("~")
    abspath = os.path.abspath(path)
    if abspath.startswith(home):
        path = abspath.replace(home, "~", 1)
    cwd = os.path.abspath(os.path.expanduser(os.getcwd()))
    if abspath.startswith(cwd):
        path = os.path.relpath(abspath, cwd)
    return path
 
tools_path = os.path.expanduser(to_relative_path(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))))

# load plugin default values
default_tty = "ttyUSB0"
default_baud = "115200"

# TODO
# if console_plugin.args and 'tty' in console_plugin.args:
#     default_tty = console_plugin.args['tty']
# 
# if console_plugin.args and 'baud' in console_plugin.args:
#     default_baud = console_plugin.args['baud']

@parser
@group(name="build")
@command(name='console', help='Open tty console')
@option(shortcut='t', name='tty', value='tty', default=default_tty, help='TTY to use')
@option(shortcut='b', name='baud', value='VALUE', default=default_baud, help='RS232 speed to use')
@option(shortcut='c', name='echo', help='Echo input data on screen', flag=True, default=True)
@option(shortcut='d', name='detach', help='Detach console in a window', flag=True, default=False)
def console(ctx, tty, baud, echo, detach, **kwargs):
    log.info(f"console")
    
    global tools_path
    
    print("Use ctrl-a to send content to serial")
    
    opts = []
    if echo==True:
        opts.append("-c")

    picocom_command = []

    picocom = shutil.which("picocom")
    if picocom is None:
        print(f"picocom: not found, you can install it with 'sudo apt-get install picocom'")
        return 
    
    try: 
        picocom_command += [
            "picocom", f"/dev/{tty}",
            "-b", f"{baud}",
            "-l",
            "--imap=lfcrlf",
            "--omap=crlf",
            "--escape=a"
        ]
        
        picocom_command += opts
        
        if detach==True:
#             xterm = shutil.which("xterm")
#             if xterm is None:
#                 print(f"xterm: not found, you can install it with 'sudo apt-get install xterm'")
#                 return 
#             command += [
#                 "nohup",
#                 "xterm",
#                 "-j",
#                 "-rightbar",
#                 "-sb",
#                 "-si",
#                 "-sk",
#                 "-sl", "99999",
#                 "-e"
#             ]

            terminator = shutil.which("terminator")
            if terminator is None:
                print(f"terminator: not found, you can install it with 'sudo apt-get install terminator'")
                return 
            command = [
                "terminator",
                "--no-dbus",
                "--command",
                ' '.join([f'{tools_path}/plugin/daemon.sh']+picocom_command),
            ]

            log.debug(" ".join(command))
            subprocess.Popen(command, start_new_session=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT
                    )
            sleep(1)
        else:
            log.debug(" ".join(picocom_command))
            subprocess.check_call(picocom_command)

    except Exception as e:
        print_stack()
        log.error(f"{e}")
        exit(1)
