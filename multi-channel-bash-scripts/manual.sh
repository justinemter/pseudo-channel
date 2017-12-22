#!/bin/bash

# Credits: irodimus 

# file: manual.sh

#----
# Simple script to change to specific channel given - triggering start / stop. 
#----

#---- 
# To Use:
# Run script by including the channel you'd like to run as an argument: ex. ./manual.sh 2, ./manual.sh 9
#
# Configure something (a tv remote or alexa) to trigger this script. Make sure you move this script just 
# outside of the pseudo-channel directories:
# -------------------
# -channels/
# --pseudo-channel_1/
# ---startstop.sh
# --pseudo-channel_2/
# ---startstop.sh
# --pseudo-channel_3/
# ---startstop.sh
# --manual.sh <--- on the same level as the 3 channels. 
#----

# Make sure that each channel dir ends with a "_" + an incrementing number as seen above.

#----BEGIN EDITABLE VARS----

SCRIPT_TO_EXECUTE='startstop.sh'

OUTPUT_PREV_CHANNEL_PATH=.

OUTPUT_PREV_CHANNEL_FILE=".prevplaying"

CHANNEL_DIR_INCREMENT_SYMBOL="_"

#----END EDITABLE VARS-------

FIRST_RUN=false

# Scan the dir to see how many channels there are, store them in an arr.
CHANNEL_DIR_ARR=( $(find . -maxdepth 1 -type d -name '*'"$CHANNEL_DIR_INCREMENT_SYMBOL"'[[:digit:]]*' -printf "%P\n" | sort -t_ -n) )

# If the previous channel txt file doesn't exist already create it (first run?)
if [ ! -e "$OUTPUT_PREV_CHANNEL_PATH/$OUTPUT_PREV_CHANNEL_FILE" ]; then

	#FIRST_RUN_NUM=$((${#CHANNEL_DIR_ARR[@]}))
	echo 1 > "$OUTPUT_PREV_CHANNEL_PATH/$OUTPUT_PREV_CHANNEL_FILE"

	echo "First run: $FIRST_RUN_NUM"

	FIRST_RUN=true

fi

# If this script see's there are multiple channels, 
# then read file, get prevchannel and nextchannel, and trigger next channel:
if [ "${#CHANNEL_DIR_ARR[@]}" -gt 1 ]; then

	NEXT_CHANNEL=$1

	NEXT_CHANNEL_DIR=( $(find . -maxdepth 1 -type d -name '*'"$CHANNEL_DIR_INCREMENT_SYMBOL""$NEXT_CHANNEL" -printf "%P\n") )

	PREV_CHANNEL_FOUND=false

	echo "+++++ There are ${#CHANNEL_DIR_ARR[@]} channels detected."

	PREV_CHANNEL=$(<$OUTPUT_PREV_CHANNEL_PATH/$OUTPUT_PREV_CHANNEL_FILE)

	PREV_CHANNEL_DIR=( $(find . -maxdepth 1 -type d -name '*'"$CHANNEL_DIR_INCREMENT_SYMBOL""$PREV_CHANNEL" -printf "%P\n") )

	echo "+++++ It looks like the previous channel was: $PREV_CHANNEL"

	echo "+++++ The next channel is: $NEXT_CHANNEL"

	# Write next channel to previous channel file to reference later
	echo "$NEXT_CHANNEL"  > "$OUTPUT_PREV_CHANNEL_PATH/$OUTPUT_PREV_CHANNEL_FILE"

	# Finally let's trigger the startstop script in both the previous channel and the next channel dirs.
	# This will stop the previous channels playback & trigger the next channels playback

	if [ "$FIRST_RUN" = false ]; then
		cd "$OUTPUT_PREV_CHANNEL_PATH"/"$PREV_CHANNEL_DIR" && ./"$SCRIPT_TO_EXECUTE"
		cd ../"$NEXT_CHANNEL_DIR" && ./"$SCRIPT_TO_EXECUTE"
	else

		cd "$OUTPUT_PREV_CHANNEL_PATH"/"$NEXT_CHANNEL_DIR" && ./"$SCRIPT_TO_EXECUTE"

	fi

	sleep 1
	

fi

exit 0