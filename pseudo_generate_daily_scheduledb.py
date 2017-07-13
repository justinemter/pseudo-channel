#!/usr/bin/python

import sqlite3
import time
import os, sys
#import Image
import string
import argparse
import datetime

conn = sqlite3.connect('pseudo-tv.db')
c = conn.cursor()

def create_table():
	c.execute('DROP TABLE IF EXISTS daily_schedule')
	c.execute('CREATE TABLE daily_schedule(id INTEGER PRIMARY KEY AUTOINCREMENT, unix INTEGER, mediaID INTEGER, title TEXT, episodeNumber INTEGER, seasonNumber INTEGER, showTitle TEXT, duration INTEGER, startTime INTEGER, endTime INTEGER, dayOfWeek TEXT)')

def add_daily_schedule_to_db(mediaID, title, episodeNumber, seasonNumber, showTitle, duration, startTime, endTime, dayOfWeek):
	unix = int(time.time())
	try:
		c.execute("INSERT OR REPLACE INTO daily_schedule (unix, mediaID, title, episodeNumber, seasonNumber, showTitle, duration, startTime, endTime, dayOfWeek) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (unix, mediaID, title, episodeNumber, seasonNumber, showTitle, duration, startTime, endTime, dayOfWeek))
		conn.commit()
	# Catch the exception
	except Exception as e:
	    # Roll back any change if something goes wrong
	    conn.rollback()
	    raise e

def get_end_time_from_duration(startTime, duration):
	#time = datetime.datetime.strptime(startTime, '%I:%M %p')
	show_time_plus_duration = time + datetime.timedelta(milliseconds=duration)
	#print(show_time_plus_duration.minute)
	return show_time_plus_duration

#sql1 = "SELECT * FROM "+media+" WHERE (episodeNumber = 10 AND showTitle LIKE ?) COLLATE NOCASE"

#def get_next_episode_title():


def update_shows_table_with_last_episode(showTitle, lastEpisodeTitle):
	sql1 = "UPDATE shows SET lastEpisodeTitle = ? WHERE title = ?"
	c.execute(sql1, (lastEpisodeTitle, showTitle, ))
	conn.commit()

def get_first_episode_title(tvshow):
	print("Getting first episode of "+tvshow)
	sql1 = "SELECT title, MIN(episodeNumber), MIN(seasonNumber) FROM episodes WHERE ( showTitle LIKE ?) COLLATE NOCASE"
	c.execute(sql1, (tvshow, ))
	datalist = list(c.fetchone())
	if datalist > 0:
		print("first episode of tvshow series: "+datalist[0])
		return datalist[0]
	else:
		print("No entry found in DB to add to schedule.")

def generate_daily_schedule():
	create_table()
	c.execute("SELECT * FROM schedule ORDER BY datetime(startTimeUnix) ASC") 
	datalist = list(c.fetchall())
	prev_row = ''
	for row in datalist:
		first_episode_title = ''
		c.execute("SELECT lastEpisodeTitle FROM shows WHERE title = ?", (row[3], )) 
		lastTitleList = list(c.fetchone())
		if lastTitleList[0] == '':
			first_episode_title = get_first_episode_title(row[3])
			update_shows_table_with_last_episode(row[3], first_episode_title)
		else:
			print("First episode already set in shows")
			c.execute("SELECT lastEpisodeTitle FROM shows WHERE title = ?", (row[3], )) 
		# if prev_row != '':
		# 	print(prev_row)
		# else:
		# 	update_shows_table_with_last_episode()
		prev_row = row

generate_daily_schedule()