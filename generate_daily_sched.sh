#!/bin/bash

# file: generate_daily_sched.sh

#----
# This file is meant to be setup with a crontab task to generate daily schedule (even if app is already running).
#
# **This file is also used to startstop a running channel, trigger an update and restart the channel**
#
# If planning on using the ./startstop.sh script to save power, etc. this script needs to be used to 
# update the daily schedule if the app is not running.
#----

#---- 
# To Use:
# % crontab -e
# 0 0 * * * cd /home/pi/pseudo-channel/ && /home/pi/pseudo-channel/env/bin/python /home/pi/pseudo-channel/PseudoChannel.py -g  >> /home/pi/pseudo-channel/pseudo-channel.log 2>&1
# 
# INFO: The above runs every midnight, triggering the virtualenv python version to trigger PsuedoChannel.py -g & send all output to the log.
# Update the paths as you see fit using your user / directories. Mine is using the defualt pi /home dir and virtualenv dirs.
#----

#----BEGIN EDITABLE VARS----

pid_file=running.pid

output_pid_path=.

python_to_use="$(which python)"

log_file=pseudo-channel.log

SCRIPT_PATH=$(pwd)

#----END EDITABLE VARS-------

if [ ! -e $SCRIPT_PATH/$pid_file ]; then

	$python_to_use $SCRIPT_PATH/PseudoChannel.py -g >> $SCRIPT_PATH/$log_file

	echo "+++++ PseudoChannel.py is not already running am generating the daily schedule." >> $SCRIPT_PATH/$log_file

else

	echo "+++++ PseudoChannel.py @: $the_pid is already running, stopping channel and running daily schedule update." >> $SCRIPT_PATH/$log_file

	bash $SCRIPT_PATH/startstop.sh

	$python_to_use $SCRIPT_PATH/PseudoChannel.py -g >> $SCRIPT_PATH/$log_file

	bash $SCRIPT_PATH/startstop.sh

	echo "+++++ Successfully stopped running channel, generated daily schedule and restarted script."

fi