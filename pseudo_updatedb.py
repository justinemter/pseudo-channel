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

conn = sqlite3.connect('pseudo-tv.db')
c = conn.cursor()

'''
*
* Create the tables in the "pseudo-tv.db" that will be used for pseudo-channel. Notice the SQL command below says, "CREATE TABLE IF NOT EXISTS". This is useful to be able and run this as many times as possible to update & not overwrite tables. However if anything feels goofy, best thing to do is just delete the "pseudo-tv.db" and start over. 
* @use Run: "python ./pseudo_updatedb.py"
* @param null
* @return null
*
'''
def create_tables():
	c.execute('CREATE TABLE IF NOT EXISTS movies(id INTEGER PRIMARY KEY AUTOINCREMENT, unix INTEGER, mediaID INTEGER, title TEXT, duration INTEGER)')
	c.execute('CREATE TABLE IF NOT EXISTS shows(id INTEGER PRIMARY KEY AUTOINCREMENT, unix INTEGER, mediaID INTEGER, title TEXT, duration INTEGER, lastEpisodeTitle TEXT, fullImageURL TEXT)')
	c.execute('CREATE TABLE IF NOT EXISTS episodes(id INTEGER PRIMARY KEY AUTOINCREMENT, unix INTEGER, mediaID INTEGER, title TEXT, duration INTEGER, episodeNumber INTEGER, seasonNumber INTEGER, showTitle TEXT)')
	c.execute('CREATE TABLE IF NOT EXISTS commercials(id INTEGER PRIMARY KEY AUTOINCREMENT, unix INTEGER, mediaID INTEGER, title TEXT, duration INTEGER)')
	c.execute('CREATE TABLE IF NOT EXISTS schedule(id INTEGER PRIMARY KEY AUTOINCREMENT, unix INTEGER, mediaID INTEGER, title TEXT, duration INTEGER, startTime INTEGER, endTime INTEGER, dayOfWeek TEXT, startTimeUnix INTEGER)')
	c.execute('CREATE TABLE IF NOT EXISTS daily_schedule(id INTEGER PRIMARY KEY AUTOINCREMENT, unix INTEGER, mediaID INTEGER, title TEXT, episodeNumber INTEGER, seasonNumber INTEGER, showTitle TEXT, duration INTEGER, startTime INTEGER, endTime INTEGER, dayOfWeek TEXT)')
	#index
	c.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_episode_title ON episodes (title);')
	c.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_movie_title ON movies (title);')
	c.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_commercial_title ON commercials (title);')

def add_movies_to_db(mediaID, title, duration):
	unix = int(time.time())
	try:
		c.execute("INSERT OR REPLACE INTO movies (unix, mediaID, title, duration) VALUES (?, ?, ?, ?)", (unix, mediaID, title, duration))
		conn.commit()
	# Catch the exception
	except Exception as e:
	    # Roll back any change if something goes wrong
	    conn.rollback()
	    raise e

def add_shows_to_db(mediaID, title, duration, lastEpisodeTitle, fullImageURL):
	unix = int(time.time())
	try:
		c.execute("INSERT OR REPLACE INTO shows (unix, mediaID, title, duration, lastEpisodeTitle, fullImageURL) VALUES (?, ?, ?, ?, ?, ?)", (unix, mediaID, title, duration, lastEpisodeTitle, fullImageURL))
		conn.commit()
	# Catch the exception
	except Exception as e:
	    # Roll back any change if something goes wrong
	    conn.rollback()
	    raise e

def add_episodes_to_db(mediaID, title, duration, episodeNumber, seasonNumber, showTitle):
	unix = int(time.time())
	try:
		c.execute("INSERT OR REPLACE INTO episodes (unix, mediaID, title, duration, episodeNumber, seasonNumber, showTitle) VALUES (?, ?, ?, ?, ?, ?, ?)", (unix, mediaID, title, duration, episodeNumber, seasonNumber, showTitle)) 
		conn.commit()
	# Catch the exception
	except Exception as e:
	    # Roll back any change if something goes wrong
	    conn.rollback()
	    raise e

def add_commercials_to_db(mediaID, title, duration):
	unix = int(time.time())
	try:
		c.execute("INSERT OR REPLACE INTO commercials (unix, mediaID, title, duration) VALUES (?, ?, ?, ?)", (unix, mediaID, title, duration))
		conn.commit()
	# Catch the exception
	except Exception as e:
	    # Roll back any change if something goes wrong
	    conn.rollback()
	    raise e

def add_schedule_to_db(mediaID, title, duration, startTime, endTime, dayOfWeek):
	unix = int(time.time())
	try:
		c.execute("INSERT INTO schedule (unix, mediaID, title, duration, startTime, endTime, dayOfWeek) VALUES (?, ?, ?, ?, ?, ?, ?)", (unix, mediaID, title, duration, startTime, endTime, dayOfWeek))
		conn.commit()
	# Catch the exception
	except Exception as e:
	    # Roll back any change if something goes wrong
	    conn.rollback()
	    raise e

'''
*
* Connecting to the Plex library via the Python Plex API and gather the necessary information about your library / storing it all in a local "pseudo-tv.db" database.
* @param null
* @return null
*
'''
def update_db_with_media():

	sections = plex.library.sections()

	for section in sections:

		if section.title == "Movies":

			sectionMedia = plex.library.section(section.title).all()

			for media in sectionMedia:

				add_movies_to_db(1, media.title, media.duration)

		elif section.title == "TV Shows":

			sectionMedia = plex.library.section(section.title).all()

			for media in sectionMedia:

				backgroundImagePath = plex.library.section(section.title).get(media.title)

				backgroundImgURL = ''

				if isinstance(backgroundImagePath.art, str):

					backgroundImgURL = baseurl+backgroundImagePath.art+"?X-Plex-Token="+token

				add_shows_to_db(2, media.title, media.duration, '', backgroundImgURL)

				#add all episodes of each tv show to episodes table
				episodes = plex.library.section(section.title).get(media.title).episodes()

				for episode in episodes:

					duration = episode.duration

					if duration:

						add_episodes_to_db(4, episode.title, duration, episode.index, episode.parentIndex, media.title)

					else:

						add_episodes_to_db(4, episode.title, 0, episode.index, episode.parentIndex, media.title)

		elif section.title == "Commercials":

			sectionMedia = plex.library.section(section.title).all()

			for media in sectionMedia:

				add_commercials_to_db(3, media.title, media.duration)

	c.close()

	conn.close()

def update_db_with_media_test():
	sections = plex.library.sections()
	for section in sections:
		if section.title == "TV Shows":
			sectionMedia = plex.library.section(section.title).all()
			for media in sectionMedia:
				episodes = plex.library.section(section.title).get(media.title).episodes()
				for episode in episodes:
				    print(episode.parentKey)

create_tables()
update_db_with_media()