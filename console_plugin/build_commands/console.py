import shutil
import os
import extargparse
import sys
from config import Config
from command import Command
import console_plugin
from debugtools import print_stack
from log import log
import subprocess

def init_parser(parentparser, config):
    parser = parentparser.add_parser('console', help='Open console')
    parser.add_argument('-t', '--tty', default="ttyUSB0", help='TTY to use (default ttyUSB0)')
    parser.add_argument('-b', '--baud',  type=int, default=9600, help='RS232 speed to use (default 9600)')
    parser.add_argument('-c', '--echo', action='store_true', default=False, help='Echo input data on screen')
    parser.set_defaults(func=project_console)

    # add army default commands
    subparser = parser.add_subparsers(metavar='COMMAND', title=None, description=None, help=None, parser_class=extargparse.ArgumentParser, required=False)

    console_command = Command('console', console_plugin.build_commands.console, subparser, {})
    console_command.register()
    console_command.add_parent('flash', config)

def project_console(args, config, **kwargs):
    pass

    print("Use ctrl-a to send content to serial")
    
    opts = []
    if args.echo==True:
        opts.append("-c")

#sudo xterm -j -rightbar -sb -si -sk -sl 99999 -e picocom /dev/$opt_tty -b $opt_baud -l --imap=lfcrlf --omap=crlf --escape='a' --echo


    try: 
        command = [
            "picocom", f"/dev/{args.tty}",
            "-b", f"{args.baud}",
            "-l",
            "--imap=lfcrlf",
            "--omap=crlf",
            "--escape=a"
        ]

        subprocess.check_call(command+opts)
#        subprocess.check_call(['vi'])

    except Exception as e:
        print_stack()
        log.error(f"{e}")

