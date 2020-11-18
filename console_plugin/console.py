from army.api.click import verbose_option 
from army.api.debugtools import print_stack
from army.api.log import log, get_log_level
from army import cli, build
import console_plugin
import click
import subprocess
import shutil

# load plugin default values
default_tty = "ttyUSB0"
default_baud = "115200"

if console_plugin.args and 'tty' in console_plugin.args:
    default_tty = console_plugin.args['tty']

if console_plugin.args and 'baud' in console_plugin.args:
    default_baud = console_plugin.args['baud']

@build.command(name='console', help='Open console')
@verbose_option()
@click.option('-t', '--tty', default=default_tty, help='TTY to use', show_default=True)
@click.option('-b', '--baud', default=default_baud, help='RS232 speed to use', show_default=True)
@click.option('-c', '--echo', help='Echo input data on screen', is_flag=True)
@click.option('-d', '--detach', help='Detach console in a window', is_flag=True)
@click.pass_context
def console(ctx, tty, baud, echo, detach, **kwargs):
    log.info(f"console")
    
    print("Use ctrl-a to send content to serial")
    
    opts = []
    if echo==True:
        opts.append("-c")

#sudo xterm -j -rightbar -sb -si -sk -sl 99999 -e picocom /dev/$opt_tty -b $opt_baud -l --imap=lfcrlf --omap=crlf --escape='a' --echo
    command = []

    picocom = shutil.which("picocom")
    if picocom is None:
        print(f"picocom: not found, you can install it with 'sudo apt-get install picocom'")
        return 
    
    try: 
        if detach==True:
            xterm = shutil.which("xterm")
            if xterm is None:
                print(f"xterm: not found, you can install it with 'sudo apt-get install xterm'")
                return 
            command += [
                "xterm",
                "-j",
                "-rightbar",
                "-sb",
                "-si",
                "-sk",
                "-sl", "99999",
                "-e"
            ]

        command += [
            "picocom", f"/dev/{tty}",
            "-b", f"{baud}",
            "-l",
            "--imap=lfcrlf",
            "--omap=crlf",
            "--escape=a"
        ]
        
        command += opts
        
        if detach==True:
            command += ["&"]

        # TODO add check picocom is installed
        subprocess.check_call(command)
    except Exception as e:
        print_stack()
        log.error(f"{e}")

