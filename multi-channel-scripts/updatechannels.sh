#!/bin/bash

# file: updatechannels.sh

#----
# Simple script to updates each channels local db with new Plex lib items / xml.
#----

#---- 
# To Use:
# If you added new content to your Plex Library, just make this file executable move it
# to where the plex_token.py file is and run ./updatechannels.sh
#----

# Make sure that each channel dir ends with a "_" + an incrementing number as seen above.

#----BEGIN EDITABLE VARS----

SCRIPT_TO_EXECUTE_PLUS_ARGS='PseudoChannel.py -u -xml'

OUTPUT_PREV_CHANNEL_PATH=.

CHANNEL_DIR_INCREMENT_SYMBOL="_"

PYTHON_TO_USE="$(which python)"

# If using 'virtualenv' with python, specify the local virtualenv dir.
VIRTUAL_ENV_DIR="env"

#----END EDITABLE VARS-------

# If virtualenv specified & exists, using that version of python instead.
if [ -d "$VIRTUAL_ENV_DIR" ]; then

	PYTHON_TO_USE="$VIRTUAL_ENV_DIR/bin/python"

fi

# If virtualenv specified & exists at root of project, using that version of python instead.
if [ -d "../$VIRTUAL_ENV_DIR" ]; then

	PYTHON_TO_USE="../$VIRTUAL_ENV_DIR/bin/python"

fi

# If the file exists b

# Scan the dir to see how many channels there are, store them in an arr.
CHANNEL_DIR_ARR=( $(find . -maxdepth 1 -type d -name '*'"$CHANNEL_DIR_INCREMENT_SYMBOL"'[[:digit:]]*' -printf "%P\n" | sort -t"$CHANNEL_DIR_INCREMENT_SYMBOL" -n) )

# If this script see's there are multiple channels, 
# then loop through each channel and run the updates
if [ "${#CHANNEL_DIR_ARR[@]}" -gt 0 ]; then

	# If virtualenv specified & exists, using that version of python instead.
	if [ -d "./$channel/$VIRTUAL_ENV_DIR" ]; then

		PYTHON_TO_USE=./"$channel"/"$VIRTUAL_ENV_DIR/bin/python"

	fi

	echo "+++++ There are ${#CHANNEL_DIR_ARR[@]} channels detected."

	for channel in "${CHANNEL_DIR_ARR[@]}"
	do
		
		echo "+++++ Trying to update: $PYTHON_TO_USE $channel/$SCRIPT_TO_EXECUTE_PLUS_ARGS"
		# If the running.pid file doesn't exists, create it, start PseudoChannel.py and add the PID to it.
		"$PYTHON_TO_USE" "$channel"/$SCRIPT_TO_EXECUTE_PLUS_ARGS

		sleep 1

	done
	
fi

exit 0