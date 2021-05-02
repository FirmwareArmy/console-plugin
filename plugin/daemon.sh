#!/bin/bash -i

command=$*
end=1
tty=$2


# launch xterm and detach it from
while [ $end -eq 1 ]
do	
	if [ -c $tty ]
	then
		if [ ! -r $tty ]
		then
			echo "$tty: incorrect permissions, add user to dialout group by executing 'usermod -aG dialout $USER'"
			read
			exit 1
		fi
		
		echo "launch $command"
		$command
		end=$?
	else 
		echo "waiting for $tty"
		sleep 1
	fi
done