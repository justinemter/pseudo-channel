#!/bin/bash

# file: startstop.sh

#----
# Simple script to start / stop PseudoChannel.py
#----

#---- 
# To Use:
# Just run: "./startstop.sh". If the process is running it will stop it or it will start it if not.
#----

#----BEGIN EDITABLE VARS----

pid_file=running.pid

output_pid_path=.

python_to_use="$(which python)"

#----END EDITABLE VARS-------

if [ ! -e $output_pid_path/$pid_file ]; then

	# If the running.pid file doesn't exists, create it, start PseudoChannel.py and add the PID to it.
	nohup $python_to_use ./PseudoChannel.py -m -r > /dev/null 2>&1 & echo $! > $output_pid_path/$pid_file

	echo "Started PseudoChannel.py @ Process: $!"
	sleep .7
	echo "Created $pid_file file in $output_pid_path dir"

else

	# If the running.pid exists, read it & try to kill the process if it exists, then delete it.
	the_pid=$(<$output_pid_path/$pid_file)
	rm $output_pid_path/$pid_file
	echo "Deleted $pid_file file in $output_pid_path dir"
	kill $the_pid
	while [ -e /proc/$the_pid ]
	do
	    echo "PseudoChannel.py @: $the_pid is still running"
	    sleep .7
	done
	echo "PseudoChannel.py @: $the_pid has finished"

fi