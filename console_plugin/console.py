from army.api.click import verbose_option 
from army.api.debugtools import print_stack
from army.api.log import log, get_log_level
from army import cli, build
import console_plugin
import click
import subprocess

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
@click.pass_context
def console(ctx, tty, baud, echo, **kwargs):
    log.info(f"console")
    
    print("Use ctrl-a to send content to serial")
    
    opts = []
    if echo==True:
        opts.append("-c")

#sudo xterm -j -rightbar -sb -si -sk -sl 99999 -e picocom /dev/$opt_tty -b $opt_baud -l --imap=lfcrlf --omap=crlf --escape='a' --echo

    
    try: 
        command = [
            "picocom", f"/dev/{tty}",
            "-b", f"{baud}",
            "-l",
            "--imap=lfcrlf",
            "--omap=crlf",
            "--escape=a"
        ]
        
        # TODO add check picocom is installed
        subprocess.check_call(command+opts)
    except Exception as e:
        print_stack()
        log.error(f"{e}")

