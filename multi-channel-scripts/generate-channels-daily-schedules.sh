#!/bin/bash

# file: generate-channels-daily-schedules.sh

#----
# Simple script to generate the daily schedule for each individual channel. 
# 
#----

#---- 
# To Use:
# This script needs to be setup with a crontab entry that runs everyday at midnight.
#----

#----BEGIN EDITABLE VARS----

SCRIPT_TO_EXECUTE_PLUS_ARGS='PseudoChannel.py -g'

OUTPUT_PREV_CHANNEL_PATH=.

CHANNEL_DIR_INCREMENT_SYMBOL="_"

PYTHON_TO_USE="$(which python)"

# If using 'virtualenv' with python, specify the local virtualenv dir.
VIRTUAL_ENV_DIR="env"

#----END EDITABLE VARS-------

# If virtualenv specified & exists, using that version of python instead.
if [ -d "$VIRTUAL_ENV_DIR" ]; then

	PYTHON_TO_USE="$VIRTUAL_ENV_DIR/bin/python"

	echo "+++++ Virtualenv found, using: $VIRTUAL_ENV_DIR/bin/python"

fi

# Scan the dir to see how many channels there are, store them in an arr.
CHANNEL_DIR_ARR=( $(find . -maxdepth 1 -type d -name '*'"$CHANNEL_DIR_INCREMENT_SYMBOL"'[[:digit:]]*' -printf "%P\n" | sort -t"$CHANNEL_DIR_INCREMENT_SYMBOL" -n) )

# If this script see's there are multiple channels, 
# then loop through each channel and run the daily schedule generator
if [ "${#CHANNEL_DIR_ARR[@]}" -gt 1 ]; then

	echo "+++++ There are ${#CHANNEL_DIR_ARR[@]} channels detected."

	for channel in "${CHANNEL_DIR_ARR[@]}"
	do

		# If the .pid file exists for this channel, skip it because it will update while running.
		if [ ! -f "$channel/running.pid" ]; then
		
			echo "+++++ Trying to generate daily schedule: ""$PYTHON_TO_USE" ./"$channel"/$SCRIPT_TO_EXECUTE_PLUS_ARGS

			cd "$channel" && "./generate_daily_sched.sh"

			echo "+++++ Generated: $channel - new schedule."

			sleep 1

			cd ../

			sleep 1

		fi

	done
	
fi

exit 0