#!/bin/bash

# file: stopall.sh

#----
# Simple script to stop any/all channels by killing the processes/deleting the corresponding
# .pid files/previouschannel file. 
# 
#----

#---- 
# To Use:
# This script needs to be placed on the same level as your channels.
#----

#----BEGIN EDITABLE VARS----

OUTPUT_PREV_CHANNEL_PATH=.

OUTPUT_PREV_CHANNEL_FILE=".prevplaying"

CHANNEL_DIR_INCREMENT_SYMBOL="_"

PID_FILE_NAME="running.pid"

# If using 'virtualenv' with python, specify the local virtualenv dir.
VIRTUAL_ENV_DIR="env"

#----END EDITABLE VARS-------
FIRST_RUN=false

# If the prevplaying file exists, delete it
if [ -e "$OUTPUT_PREV_CHANNEL_PATH/$OUTPUT_PREV_CHANNEL_FILE" ]; then

	rm "$OUTPUT_PREV_CHANNEL_PATH/$OUTPUT_PREV_CHANNEL_FILE"

fi

# Scan the dir to see how many channels there are, store them in an arr.
CHANNEL_DIR_ARR=( $(find . -maxdepth 1 -type d -name '*'"$CHANNEL_DIR_INCREMENT_SYMBOL"'[[:digit:]]*' -printf "%P\n") )

# If this script see's there are multiple channels, 
# check each channel dir for running .pid file to kill the process/delete the file:
if [ "${#CHANNEL_DIR_ARR[@]}" -gt 1 ]; then

	NEXT_CHANNEL=""

	PREV_CHANNEL_FOUND=false

	PREV_CHANNEL_DIR=""

	echo "+++++ There are ${#CHANNEL_DIR_ARR[@]} channels detected."

	# Loop through each Channel Dir, if .pid file exists, then kill pid and rm pid file.
	for channel in "${CHANNEL_DIR_ARR[@]}"
	do
		if [ -e "$channel/$PID_FILE_NAME" ]; then

			the_pid=$(<$channel/$PID_FILE_NAME)

			kill "$the_pid"

			COUNTER=1

			while [ -e /proc/$the_pid ]
			
			do

			    echo "+++++ $the_pid is still running"

			    sleep .7

			    COUNTER=$[$COUNTER +1]

			    if [ $COUNTER -eq 20 ]; then

			    	kill -9 "$the_pid"

			    fi

			    if [ $COUNTER -eq 40 ]; then

			    	exit 1

			    fi

			done

			echo "+++++ $the_pid has finished"

			echo "+++++ Removing $channel/$PID_FILE_NAME"

			rm "$channel/$PID_FILE_NAME"

		fi

	done

	echo "Exiting stop-all-channels.sh script."

fi

exit 0