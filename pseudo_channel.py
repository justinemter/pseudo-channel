#!/usr/bin/python

from plexapi.server import PlexServer
import sqlite3
import time
import os, sys
#import Image
import string
import argparse
import datetime

from pseudo_config import *

plex = PlexServer(baseurl, token)

conn = sqlite3.connect('pseudo-tv.db', timeout=10)
c = conn.cursor()

def add_schedule_to_db(mediaID, title, duration, startTime, endTime, dayOfWeek):
	unix = int(time.time())
	startTimeUnix = str(datetime.datetime.strptime(startTime, '%I:%M %p'))
	try:
		c.execute("INSERT INTO schedule (unix, mediaID, title, duration, startTime, endTime, dayOfWeek, startTimeUnix) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (unix, mediaID, title, duration, startTime, endTime, dayOfWeek, startTimeUnix))
		conn.commit()
		c.close()
		conn.close()
	# Catch the exception
	except Exception as e:
	    # Roll back any change if something goes wrong
		conn.rollback()
		c.close()
		conn.close()
		raise e
	

def convertMillis(millis):
 	seconds=(millis/1000)%60
 	minutes=(millis/(1000*60))%60
 	hours=(millis/(1000*60*60))%24
 	return str(hours)+':'+str(minutes)+':'+str(seconds)

# Example 8: Get a URL to stream a movie or show in another client
def getMediaDuration():
	movie = plex.library.section('Movies').get('Dumb and Dumber')
	print('The movie is this long:')
	print(convertMillis(movie.duration));

def showConnectedClients():
	for client in plex.clients():
    		print(client.title)

def playMovie():
	cars = plex.library.section('Movies').get('Dumb and Dumber')
	client = plex.client("RasPlex")
	client.playMedia(cars)

def stopMovie():
	client = plex.client("RasPlex")
	client.stop(mtype='video')

def getIsPlayingMedia():
	client = plex.client("RasPlex")
	return client.isPlayingMedia(includePaused=False)

def getEpisodeDuration():
	movie = plex.library.section('TV Shows').get('Seinfeld')
	print('The movie is this long:')
	print(movie);
	for show in movie:
    		print(show.title)
	
# Example 7: List files for the latest episode of Friends.
#episodes = plex.library.section('TV Shows').get('Friends').episodes()
#for episode in episodes:
#    print(episode.parentIndex)

def getSections():
	sections = plex.library.sections()
	for section in sections:
		print(section.title)
		return section

def getAllTVShows():
	shows = plex.library.section('TV Shows').all()
	for show in shows:
		print(show.title)

def getAllMedia():
	sections = plex.library.sections()
	for section in sections:
		sectionMedia = plex.library.section(section.title).all()
		for media in sectionMedia:
			print(media.title)



def get_end_time_from_duration(startTime, duration):
	time = datetime.datetime.strptime(startTime, '%I:%M %p')
	show_time_plus_duration = time + datetime.timedelta(milliseconds=duration)
	#print(show_time_plus_duration.minute)
	return show_time_plus_duration

#sql1 = "SELECT * FROM "+media+" WHERE (episodeNumber = 10 AND showTitle LIKE ?) COLLATE NOCASE"

def add_schedule(media, name, time, day):
	print("Adding the following schedule: -Type: "+media+" -Name: "+name+" -Time: "+time+" -Day: "+day)

	sql1 = "SELECT * FROM "+media+" WHERE (title LIKE ?) COLLATE NOCASE"
	c.execute(sql1, (name, ))
	datalist = list(c.fetchone())
	if datalist > 0:
		print(datalist)
		add_schedule_to_db(0, datalist[3], 0, time, 0, day)
		#get_end_time_from_duration(time, datalist[3])
	else:
		print("No entry found in DB to add to schedule.")



parser = argparse.ArgumentParser()

parser.add_argument('-a', '--add', dest='add_variable', required=True)
parser.add_argument('-n', '--name', dest='name_variable', required=True)
parser.add_argument('-t', '--time', dest='time_variable', required=True)
parser.add_argument('-d', '--day', dest='day_variable', required=True)

globals().update(vars(parser.parse_args()))


if add_variable:
	add_schedule(add_variable, name_variable, time_variable, day_variable)


# python pseudo-channel.py -a "shows" -n "curb your enthusiasm" -t "7:30 PM" -d "weekdays"


# create_tables()
# update_db_with_media()
