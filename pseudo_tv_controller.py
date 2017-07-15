#!/usr/bin/python

from plexapi.server import PlexServer
from datetime import datetime
import sqlite3

import logging
import logging.handlers

from pseudo_config import *

plex = PlexServer(baseurl, token)

conn = sqlite3.connect('pseudo-tv.db', timeout=10)
c = conn.cursor()

my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address = '/dev/log')

my_logger.addHandler(handler)

def showConnectedClients():
	for client in plex.clients():
    		print(client.title)

def playMovie():
	cars = plex.library.section('Movies').get('Dumb and Dumber')
	client = plex.client("RasPlex")
	print(cars)
	client.playMedia(cars)
'''
*
* Play Media
*
'''
def play_media(mediaType, mediaParentTitle, mediaTitle):
	media = plex.library.section(mediaType).get(mediaParentTitle).episodes()
	client = plex.client("RasPlex")
	last_episode = plex.library.section('TV Shows')
	for part in media:
		# print(part.title)
		if part.title == mediaTitle:
			client.playMedia(part)
			break

'''
*
* Check DB / current time. If that matches a scheduled shows startTime then trigger play via Plex API
*
'''
def tv_controller():

	currentTime = datetime.now()

	sql = """SELECT *
			FROM scheduled_shows
			WHERE datetime(startTimeUnix) = ? AND
			      datetime(startTimeUnix) = ? """
			      

	c.execute("SELECT * FROM daily_schedule ORDER BY datetime(startTimeUnix) ASC")

	datalist = list(c.fetchall())

	my_logger.debug('TV Controller')

	for row in datalist:

		timeB = datetime.strptime(row[8], '%I:%M %p')

		if currentTime.hour == timeB.hour:

			if currentTime.minute == timeB.minute:

				print("Starting Epsisode: " + row[3])
				print(row)

				play_media("TV Shows", row[6], row[3])

				my_logger.debug('Trying to play: ' + row[3])

				break




tv_controller()

#showConnectedClients()

#playMovie()
#play_media("TV Shows", "The Office (US)", "Garage Sale")