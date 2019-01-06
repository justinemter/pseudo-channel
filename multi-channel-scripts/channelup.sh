#!/bin/bash

# file: channelup.sh

#----
# Simple script to cycle through multiple pseudo-channel instances - triggering start / stop.
#----

#---- 
# To Use:
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
# --channelup.sh <--- on the same level as the 3 channels. 
#----

# Make sure that each channel dir ends with a "_" + an incrementing number as seen above.

#----BEGIN EDITABLE VARS----

SCRIPT_TO_EXECUTE='startstop.sh'

OUTPUT_PREV_CHANNEL_PATH=.

OUTPUT_PREV_CHANNEL_FILE=".prevplaying"

CHANNEL_DIR_INCREMENT_SYMBOL="_"

#----END EDITABLE VARS-------

FIRST_RUN=false

# If the previous channel txt file doesn't exist already create it (first run?)
if [ ! -e "$OUTPUT_PREV_CHANNEL_PATH/$OUTPUT_PREV_CHANNEL_FILE" ]; then

	echo 1 > "$OUTPUT_PREV_CHANNEL_PATH/$OUTPUT_PREV_CHANNEL_FILE"

	FIRST_RUN=true

fi

# If the file exists b

# Scan the dir to see how many channels there are, store them in an arr.
CHANNEL_DIR_ARR=( $(find . -maxdepth 1 -type d -name '*'"$CHANNEL_DIR_INCREMENT_SYMBOL"'[[:digit:]]*' -printf "%P\n" | sort -t"$CHANNEL_DIR_INCREMENT_SYMBOL" -n) )

# If this script see's there are multiple channels, 
# then read file, get prevchannel, increment, and trigger next channel:
if [ "${#CHANNEL_DIR_ARR[@]}" -gt 1 ]; then

	NEXT_CHANNEL=""

	PREV_CHANNEL_FOUND=false

	PREV_CHANNEL_DIR=""

	echo "+++++ There are ${#CHANNEL_DIR_ARR[@]} channels detected."

	PREV_CHANNEL=$(<$OUTPUT_PREV_CHANNEL_PATH/$OUTPUT_PREV_CHANNEL_FILE)

	echo "+++++ It looks like the previous channel was: $PREV_CHANNEL"

	# Now that the prevchannel is stored in a var, loop through channels and find prev channel & increment
	for channel in "${CHANNEL_DIR_ARR[@]}"
	do
		if [[ $channel == *"$PREV_CHANNEL"* ]]; then
  			echo "+++++ Found previous channel, incrementing by 1."
  			PREV_CHANNEL_FOUND=true
  			PREV_CHANNEL_DIR=$channel
  			continue
		fi

		if [ "$PREV_CHANNEL_FOUND" = true ] ; then
		    
		    NEXT_CHANNEL=$channel

			break
		
		fi

	done

	# If the next channel is an empty string, then we need to start the cycle over.
	if [ -z "$NEXT_CHANNEL" ]; then

		NEXT_CHANNEL=${CHANNEL_DIR_ARR[0]}

	fi

	echo "+++++ The next channel is: $NEXT_CHANNEL"

	# Write next channel to previous channel file to reference later
	echo "$NEXT_CHANNEL" | cut -d "_" -f2  > "$OUTPUT_PREV_CHANNEL_PATH/$OUTPUT_PREV_CHANNEL_FILE"

	# Finally let's trigger the startstop script in both the previous channel and the next channel dirs.
	# This will stop the previous channels playback & trigger the next channels playback

	if [ "$FIRST_RUN" = false ]; then
		cd "$OUTPUT_PREV_CHANNEL_PATH"/"$PREV_CHANNEL_DIR" && ./"$SCRIPT_TO_EXECUTE"
		cd ../"$NEXT_CHANNEL" && ./"$SCRIPT_TO_EXECUTE"
	else

		cd "$OUTPUT_PREV_CHANNEL_PATH"/"$NEXT_CHANNEL" && ./"$SCRIPT_TO_EXECUTE"

	fi

	sleep 1
	

fi

exit 0