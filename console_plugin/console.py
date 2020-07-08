from army.api.click import verbose_option 
from army.api.debugtools import print_stack
from army.api.log import log, get_log_level
from army.army import cli, build
import click
import subprocess

@build.command(name='console', help='Open console')
@verbose_option()
@click.option('-t', '--tty', default="ttyUSB0", help='TTY to use (default ttyUSB0)')
@click.option('-b', '--baud', default=115200, help='RS232 speed to use (default 115200)')
@click.option('-c', '--echo', help='Echo input data on screen', is_flag=True)
@click.pass_context
def console(ctx, tty, baud, echo, **kwargs):
    log.info(f"console")
    
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

