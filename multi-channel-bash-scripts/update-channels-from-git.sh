#!/bin/bash

# file: update-channels-from-git.sh

#----
# Simple script to update every channel with updates from the github repo. 
# BACKUP EACH XML/DB IN EACH CHANNEL.
#----

#---- 
# To Use:
# chmod +x update-channels-from-git.sh
# ./update-channels-from-git.sh
#----

#----BEGIN EDITABLE VARS----

SCRIPT_TO_EXECUTE_PLUS_ARGS='git clone https://github.com/justinemter/pseudo-channel . --branch develop'

OUTPUT_PREV_CHANNEL_PATH=.

CHANNEL_DIR_INCREMENT_SYMBOL="_"

#----END EDITABLE VARS-------

# Scan the dir to see how many channels there are, store them in an arr.
CHANNEL_DIR_ARR=( $(find . -maxdepth 1 -type d -name '*'"$CHANNEL_DIR_INCREMENT_SYMBOL"'[[:digit:]]*' -printf "%P\n" | sort -t"$CHANNEL_DIR_INCREMENT_SYMBOL" -n) )

# If this script see's there are multiple channels, 
# then loop through each channel and run clone the repo there
if [ "${#CHANNEL_DIR_ARR[@]}" -gt 1 ]; then

	echo "+++++ There are ${#CHANNEL_DIR_ARR[@]} channels detected."

	for channel in "${CHANNEL_DIR_ARR[@]}"
	do

		echo "+++++ Trying to update channel:"./"$channel"/$SCRIPT_TO_EXECUTE_PLUS_ARGS

		cd "$channel" 

		mkdir ../.pseudo-temp

		cp ./pseudo-channel.db ../.pseudo-temp

		cp ./pseudo_schedule.xml ../.pseudo-temp

		cp ./pseudo_config.py ../.pseudo-temp

		find -mindepth 1 -delete && $SCRIPT_TO_EXECUTE_PLUS_ARGS

		cp ../.pseudo-temp/pseudo-channel.db .

		cp ../.pseudo-temp/pseudo_schedule.xml .

		cp ../.pseudo-temp/pseudo_config.py .

		echo "+++++ Done."

		sleep 1

		rm -rf ../.pseudo-temp

		cd ../

		sleep 1

	done
	
fi

exit 0