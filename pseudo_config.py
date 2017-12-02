#!/usr/bin/env python

"""
    1) Create a file outside of this proj dir called "plex_token.py":

    touch ../plex_token.py
    
    2) add these lines to the newly created file:

    baseurl = 'the url to your server'
    token = 'your plex token'

    3) Edit the "basurl" variable below to point to your Plex server

    4) Edit the "plexClients" variable to include the name of your plex client(s) this app will control.

    5) Edit the "plexLibraries" variable to remap your specific library names to the app specific names. 
    ...for instance, if your Plex "Movies" are located in your Plex library as "Films", update that
    line so it looks like: 

    "Movies" : ["Films"],

    6) *Skip this feature for now* 

    For Google Calendar integration add your "gkey" to the "plex_token.py" file 
    ...(https://docs.simplecalendar.io/find-google-calendar-id/):

    gkey = "the key"

    7) If using the Google Calendar integration exclusively, set this to true below:

    useGoogleCalendar
    
"""

'''
*
* List of plex clients to use (add multiple clients to control multiple TV's)
*
'''
plexClients = ['RasPlex']

plexLibraries = {
    "TV Shows" : ["TV"],
    "Movies"   : ["Films"],
    "Commercials" : ["Commercials", "Smashing Pumpkins - Videos"],
}

useCommercialInjection = True

"""How many seconds to pad commercials between each other / other media"""
commercialPadding = 5

"""
Specify the path to this controller on the network (i.e. 'http://192.168.1.28' - no trailing slash).
Also specify the desired port to run the simple http webserver. The daily generated
schedule will be served at "http://<your-ip>:<your-port>/" (i.e. "http://192.168.1.28:8000/"). 

You can also leave the below controllerServerPath empty if you'd like to run your own webserver.
"""
controllerServerPath = "http://192.168.1.28"
controllerServerPort = "8000"

"""
When the schedule updates every 24 hours, it's possible that it will interrupt any shows / movies that were 
playing from the previous day. To fix this, the app saves a "cached" schedule from the previous day to 
override any media that is trying to play while the previous day is finishing.
"""
useDailyOverlapCache = True

dailyUpdateTime = "12:00 AM"

"""When to delete / remake the pseudo-channel.log - right at midnight, (i.e. 'friday') """
rotateLog = "friday"

"""Debug mode will give you more output in your terminal to help problem solve issues."""
debug_mode = True

"""This squeezes in one last commercial to fill up the empty gaps even if the last commercial gets cutoff
Set this to false if you don't want your commercials to get cutoff/don't mind the gap.
"""
useDirtyGapFix = False

"""
##### Do not edit below this line---------------------------------------------------------------

Below is logic to grab your Plex 'token' & Plex 'baseurl'. If you are following along and have created a 'plex_token.py'
file as instructed, you do not need to edit below this line. 

"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import ../plex_token.py

try:
    import plex_token as plex_token
except ImportError as e:
    print "+++++ Cannot find plex_token file. Make sure you create a plex_token.py file with the appropriate data."
    raise e

baseurl = plex_token.baseurl
token = plex_token.token
gkey = '' #plex_token.gkey