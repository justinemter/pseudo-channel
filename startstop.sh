#!/bin/bash

# file: startstop.sh

#----
# Simple script to start / stop a python script in the background.
#----

#---- 
# To Use:
# Just run: "./startstop.sh". If the process is running it will stop it or it will start it if not.
#----

#----BEGIN EDITABLE VARS----

SCRIPT_TO_EXECUTE_PLUS_ARGS='PseudoChannel.py -m -r'

OUTPUT_PID_FILE=running.pid

OUTPUT_PID_PATH=.

PYTHON_TO_USE="$(which python)"

# If using 'virtualenv' with python, specify the local virtualenv dir.
VIRTUAL_ENV_DIR="env"

#----END EDITABLE VARS-------

# If virtualenv specified & exists, using that version of python instead.
if [ -d "$VIRTUAL_ENV_DIR" ]; then

	PYTHON_TO_USE="$VIRTUAL_ENV_DIR/bin/python"

fi

# If the .pid file doesn't exist (let's assume no processes are running)...
if [ ! -e "$OUTPUT_PID_PATH/$OUTPUT_PID_FILE" ]; then

	# If the running.pid file doesn't exists, create it, start PseudoChannel.py and add the PID to it.
	"$PYTHON_TO_USE" ./$SCRIPT_TO_EXECUTE_PLUS_ARGS > /dev/null 2>&1 & echo $! > "$OUTPUT_PID_PATH/$OUTPUT_PID_FILE"

	echo "Started $SCRIPT_TO_EXECUTE_PLUS_ARGS @ Process: $!"

	sleep .7

	echo "Created $OUTPUT_PID_FILE file in $OUTPUT_PID_PATH dir"

else

	# If the running.pid exists, read it & try to kill the process if it exists, then delete it.
	the_pid=$(<$OUTPUT_PID_PATH/$OUTPUT_PID_FILE)

	rm "$OUTPUT_PID_PATH/$OUTPUT_PID_FILE"

	echo "Deleted $OUTPUT_PID_FILE file in $OUTPUT_PID_PATH dir"

	kill "$the_pid"

	COUNTER=1

	while [ -e /proc/$the_pid ]
	
	do

	    echo "$SCRIPT_TO_EXECUTE_PLUS_ARGS @: $the_pid is still running"

	    sleep .7

	    COUNTER=$[$COUNTER +1]

	    if [ $COUNTER -eq 20 ]; then

	    	kill -9 "$the_pid"

	    fi

	    if [ $COUNTER -eq 40 ]; then

	    	exit 1

	    fi

	done

	echo "$SCRIPT_TO_EXECUTE_PLUS_ARGS @: $the_pid has finished"

fi

exit 0