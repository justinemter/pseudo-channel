#!/usr/bin/python

from plexapi.server import PlexServer
import sqlite3
import time
import os, sys
import string
import argparse
import datetime

from pseudo_config import *

plex = PlexServer(baseurl, token)

conn = sqlite3.connect('pseudo-tv.db', timeout=10)
c = conn.cursor()

def create_table():

	c.execute('DROP TABLE IF EXISTS schedule')

	c.execute('CREATE TABLE IF NOT EXISTS schedule(id INTEGER PRIMARY KEY AUTOINCREMENT, unix INTEGER, mediaID INTEGER, title TEXT, duration INTEGER, startTime INTEGER, endTime INTEGER, dayOfWeek TEXT, startTimeUnix INTEGER)')

def add_schedule_to_db(mediaID, title, duration, startTime, endTime, dayOfWeek):
	unix = int(time.time())
	startTimeUnix = str(datetime.datetime.strptime(startTime, '%I:%M %p'))
	try:

		c.execute("INSERT OR REPLACE INTO schedule (unix, mediaID, title, duration, startTime, endTime, dayOfWeek, startTimeUnix) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (unix, mediaID, title, duration, startTime, endTime, dayOfWeek, startTimeUnix))
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

def remove_all_scheduled_items():

	sql = "DELETE FROM schedule WHERE id > -1"

	c.execute(sql1)

	conn.commit()

	c.close()
	
	conn.close()


def show_connected_clients():

	for client in plex.clients():

    		print(client.title)

def play_show(mediaType, mediaParentTitle, mediaTitle):

	mediaItems = plex.library.section(mediaType).get(mediaParentTitle).episodes()

	for item in mediaItems:

		# print(part.title)

		if item.title == mediaTitle:

			for client in plexClients:

				clientItem = plex.client(client)

				clientItem.playMedia(item)
				
				break


parser = argparse.ArgumentParser()

parser.add_argument('-a', '--add', dest='add_variable')
parser.add_argument('-n', '--name', dest='name_variable')
parser.add_argument('-t', '--time', dest='time_variable')
parser.add_argument('-d', '--day', dest='day_variable')

'''
* 
* Play specific show: "python pseudo_channel.py -ps 'Garage Sale' -st 'The Office (US)' "

* This is useful for debugging. Set your Plex clients in the config and try the above command to see if it works.
*
'''
parser.add_argument('-ps', dest='play_show_variable')
parser.add_argument('-st', dest='play_show_series_title_variable')

'''
* 
* Show connected clients: "python pseudo_channel.py -sc"
*
'''
parser.add_argument('-sc', action='store_true')

globals().update(vars(parser.parse_args()))

args = parser.parse_args()

if add_variable:

	add_schedule(add_variable, name_variable, time_variable, day_variable)

if args.sc == True:
	
	show_connected_clients()

if play_show_variable:

	play_show("TV Shows", play_show_series_title_variable, play_show_variable)

# python pseudo-channel.py -a "shows" -n "curb your enthusiasm" -t "7:30 PM" -d "weekdays"


# create_tables()
# update_db_with_media()
