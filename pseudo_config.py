#!/usr/bin/python
"""
	1) Create a file outside of this proj dir called "plex_token.py":

	touch ../plex_token.py
	
	2) add this line to the newly created file:

	token = 'your plex token'

	3) Edit the "basurl" variable below to point to your Plex server

	4) Edit the "plexClients" variable to include the name of your plex client(s) this app will control.

	5) Edit the "plexLibraries" variable to remap your specific library names to the app specific names. 
	...for instance, if your Plex "Movies" are located in your Plex library as "Films", update that
	line so it looks like: 

	"Movies" : ["Films"],
	
"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import ../plex_token.py
import plex_token as plex_token

baseurl = 'http://media.home:32400'
token = plex_token.token

'''
*
* List of plex clients to use (add multiple clients to control multiple TV's)
*
'''
plexClients = ['RasPlex']

plexLibraries = {
	"TV Shows" : ["TV Shows"],
	"Movies"   : ["Movies"],
	"Music"    : ["Music"],
	"Commercials" : ["Commercials"],
}
