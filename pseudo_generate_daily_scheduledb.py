#!/usr/bin/python

'''
*
* This script is for generating a daily schedule using a crontab as the clock. 
* It queries the "schedule" table and the "shows" table to determine the next episode in a TV Series.
* A time will be generated based on the scheduled time and the duration of the previous episode (or movie).
* After the data has been generated, an entry will be made in the "daily_schedule" table. 
* This should be run every day at midnight:
* 
* crontab -e
* 0 0 * * * python /home/justin/this-repo-folder/pseudo_generate_daily_scheduledb.py
*
'''

import sqlite3
import time
import os, sys
import string
import argparse
import datetime
import calendar
import itertools
from yattag import Doc

from pseudo_config import *

conn = sqlite3.connect('pseudo-tv.db')

c = conn.cursor()

'''
*
* Get HTML from Scheduled Content to save to file
*
'''
def get_html_from_daily_schedule():

    doc, tag, text, line = Doc(

    ).ttl()

    doc.asis('<!DOCTYPE html>')

    with tag('html'):

    	with tag('head'):

			doc.asis('<link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" rel="stylesheet">')

        with tag('body'):

        	with tag('div', klass='container mt-3'):

				now = datetime.datetime.now()

				time = now.strftime("%B %d, %Y")

				with tag('div'):

					with tag('div', klass='row'):

						line('h1', "Daily Schedule", klass='col-12 pl-0')

					with tag('div', klass='row'):

						line('h3', time, klass='col-12 pl-0')

	            # with tag('div', klass = 'description'):
	            #     text(data['article']['description'])

				with tag('div', klass='row'):

					with tag('table', klass='col-12 table table-bordered table-hover'):

						with tag('thead', klass='table-info'):
							with tag('tr'):
								with tag('th'):
									text('#')
								with tag('th'):
									text('Series')
								with tag('th'):
									text('Title')
								with tag('th'):
									text('Start Time')

						c.execute("SELECT * FROM daily_schedule ORDER BY datetime(startTimeUnix) ASC")

						datalist = list(c.fetchall())

						numberIncrease = 0

						for row in datalist:

							numberIncrease += 1

							with tag('tbody'):
								with tag('tr'):
									with tag('th', scope='row'):
										text(numberIncrease)
									with tag('td'):
										text(row[6])
									with tag('td'):
										text(row[3])
									with tag('td'):
										text(row[8])

    return doc.getvalue()

def write_schedule_to_file(data):

	now = datetime.datetime.now()

	fileName = "pseudo-tv_todays-schedule.html"

	writepath = './schedules/'

	if not os.path.exists(writepath):

		os.makedirs(writepath)

	if os.path.exists(writepath+fileName):
		
		os.remove(writepath+fileName)

	mode = 'a' if os.path.exists(writepath) else 'w'

	with open(writepath+fileName, mode) as f:

		f.write(data)

def create_table():

	c.execute('DROP TABLE IF EXISTS daily_schedule')

	c.execute('CREATE TABLE daily_schedule(id INTEGER PRIMARY KEY AUTOINCREMENT, unix INTEGER, mediaID INTEGER, title TEXT, episodeNumber INTEGER, seasonNumber INTEGER, showTitle TEXT, duration INTEGER, startTime INTEGER, endTime INTEGER, dayOfWeek TEXT, startTimeUnix INTEGER)')

def add_daily_schedule_to_db(mediaID, title, episodeNumber, seasonNumber, showTitle, duration, startTime, endTime, dayOfWeek, startTimeUnix):

	unix = int(time.time())

	try:

		c.execute("INSERT OR REPLACE INTO daily_schedule (unix, mediaID, title, episodeNumber, seasonNumber, showTitle, duration, startTime, endTime, dayOfWeek, startTimeUnix) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (unix, mediaID, title, episodeNumber, seasonNumber, showTitle, duration, startTime, endTime, dayOfWeek, startTimeUnix))

		conn.commit()

	# Catch the exception
	except Exception as e:

	    # Roll back any change if something goes wrong

	    conn.rollback()

	    raise e

'''
*
* Returns time difference in minutes
*
'''
def time_diff(time1,time2):
	'''
	*
	* Getting the offest by comparing both times from the unix epoch time and getting the difference.
	*
	'''
	timeA = datetime.datetime.strptime(time1, "%I:%M %p")
	timeB = datetime.datetime.strptime(time2, "%I:%M %p")
	
	timeAEpoch = calendar.timegm(timeA.timetuple())
	timeBEpoch = calendar.timegm(timeB.timetuple())

	tdelta = abs(timeAEpoch) - abs(timeBEpoch)

	return int(tdelta/60)


'''
*
* Passing in the endtime from the prev episode and desired start time of this episode, calculate the best start time 

* Returns time - for new start time
*
'''
def calculate_start_time_offset_from_prev_episode_endtime(prevEndTime, intendedStartTime, duration, prevEpDuration):

	time1 = prevEndTime.strftime('%I:%M %p')

	timeB = datetime.datetime.strptime(intendedStartTime, '%Y-%m-%d %H:%M:%S').strftime('%I:%M %p')

	timeDiff = time_diff(time1, timeB)

	print("timeDiff "+ str(timeDiff))
	print("startTimeUNIX: "+ str(intendedStartTime))

	newTimeObj = datetime.datetime.strptime(intendedStartTime, "%Y-%m-%d %H:%M:%S")

	newStartTime = datetime.datetime.strptime(intendedStartTime, '%Y-%m-%d %H:%M:%S')

	'''
	*
	* If time difference is negative, then we know there is overlap
	*
	'''
	if timeDiff < 0:

		print("There is overlap ")

		'''
		*
		* If there is an overlap, then the overlapGap var in config will determine the next increment. If it is set to "15", then the show will will bump up to the next 15 minute interval past the hour.
		*
		'''
		timeset=[datetime.time(h,m).strftime("%H:%M") for h,m in itertools.product(xrange(0,24),xrange(0,60,int(overlapGap)))]
		
		print(timeset)

		timeSetToUse = None

		for time in timeset:

			#print(time)
			theTimeSetInterval = datetime.datetime.strptime(time, '%H:%M')

			# print(theTimeSetInterval)

			# print(prevEndTime)

			if theTimeSetInterval >= prevEndTime:

				print("Setting new time by interval... " + time)
				print("made it!")

				newStartTime = theTimeSetInterval

				break

			#newStartTime = newTimeObj + datetime.timedelta(minutes=abs(timeDiff + overlapGap))

	elif (timeDiff >= 0) and (timeGap != -1):

		'''
		*
		* If there this value is configured, then the timeGap var in config will determine the next increment. If it is set to "15", then the show will will bump up to the next 15 minute interval past the hour.
		*
		'''
		timeset=[datetime.time(h,m).strftime("%H:%M") for h,m in itertools.product(xrange(0,24),xrange(0,60,int(timeGap)))]
		
		# print(timeset)

		timeSetToUse = None

		for time in timeset:

			#print(time)
			theTimeSetInterval = datetime.datetime.strptime(time, '%H:%M')

			# print(theTimeSetInterval)

			# print(prevEndTime)

			if theTimeSetInterval >= prevEndTime:

				print("Setting new time by interval... " + time)
				print("made it!")

				newStartTime = theTimeSetInterval

				break


	else:

		print("Not sure what to do here")

		

	return newStartTime.strftime('%I:%M %p')

'''
*
* Using datetime to figure out when the media item will end based on the scheduled start time or the offset 
* generated by the previous media item. 

* Returns time 
*
'''
def get_end_time_from_duration(startTime, duration):

	time = datetime.datetime.strptime(startTime, '%I:%M %p')

	show_time_plus_duration = time + datetime.timedelta(milliseconds=duration)

	#print(show_time_plus_duration.minute)

	return show_time_plus_duration


def update_shows_table_with_last_episode(showTitle, lastEpisodeTitle):

	sql1 = "UPDATE shows SET lastEpisodeTitle = ? WHERE title = ?"

	c.execute(sql1, (lastEpisodeTitle, showTitle, ))

	conn.commit()

def get_first_episode(tvshow):

	sql1 = "SELECT id, unix, mediaID, title, duration, MIN(episodeNumber), MIN(seasonNumber), showTitle FROM episodes WHERE ( showTitle = ?) COLLATE NOCASE"

	c.execute(sql1, (tvshow, ))

	datalist = list(c.fetchone())

	if datalist > 0:
		
		return datalist

	else:

		print("No entry found in DB to add to schedule.")

'''
*
* When incrementing episodes in a series I am advancing by "id" 
*
'''
def get_episode_id(episodeTitle):

	sql1 = "SELECT id FROM episodes WHERE ( title = ?) COLLATE NOCASE"

	c.execute(sql1, (episodeTitle, ))

	datalist = list(c.fetchone())

	if datalist > 0:

		return datalist[0]

	else:

		print("No entry found in DB to add to schedule.")

def generate_daily_schedule():

	'''
	*
	* prevEpisodeEndTime will be used when calculating current episodes start time
	*
	'''
	prevEpisodeEndTime = None

	prevEpDuration = None
	'''
	*
	* Everytime this function is run it drops the previous "scheduled_shows" & table recreates it
	*
	'''
	create_table()
	'''
	*
	* Get all shows that have been entered into the "schedule" table ordered by the desired scheduled time
	*
	'''
	c.execute("SELECT * FROM schedule ORDER BY datetime(startTimeUnix) ASC")

	datalistLengthMonitor = 0;

	datalist = list(c.fetchall())

	for row in datalist:

		first_episode_title = ''
		'''
		*
		* As a way of storing a "queue", I am storing the *next episode title in the "shows" table so I can 
		* determine what has been previously scheduled for each show
		*
		'''
		c.execute("SELECT lastEpisodeTitle FROM shows WHERE title = ?", (row[3], ))

		lastTitleList = list(c.fetchone())
		'''
		*
		* If the last episode stored in the "shows" table is empty, then this is probably a first run...
		*
		'''
		if lastTitleList[0] == '':
			'''
			*
			* Find the first episode of the series
			*
			'''
			first_episode = get_first_episode(row[3])

			first_episode_title = first_episode[3]

			print(first_episode_title)
			'''
			*
			* Add this episdoe title to the "shows" table for the queue functionality to work
			*
			'''
			update_shows_table_with_last_episode(row[3], first_episode_title)

			newStartTime = row[5]

			if prevEpisodeEndTime != None:

				newStartTime = calculate_start_time_offset_from_prev_episode_endtime(prevEpisodeEndTime, row[8], first_episode[4], prevEpDuration)

			'''
			*
			* Generate a new end time from calculated new start time
			*
			'''
			endTime = get_end_time_from_duration(newStartTime, first_episode[4]);

			print("prevEpisodeEndTime: " + str(prevEpisodeEndTime)); 

			startTimeUnix = datetime.datetime.strptime(newStartTime, '%I:%M %p')

			add_daily_schedule_to_db(0, first_episode[3], first_episode[5], first_episode[6], row[3], first_episode[4], newStartTime, endTime, row[7], startTimeUnix)

			prevEpisodeEndTime = endTime

			prevEpDuration = first_episode[4]

			datalistLengthMonitor += 1

			if datalistLengthMonitor >= len(datalist):

				write_schedule_to_file(get_html_from_daily_schedule())
		
		else:
			'''
			*
			* The last episode stored in the "shows" table was not empty... get the next episode in the series
			*
			'''
			print("First episode already set in shows, advancing episodes forward")

			print(str(get_episode_id(lastTitleList[0])))
			"""
			*
			* If this isn't a first run, then grabbing the next episode by incrementing id
			*
			"""
			sql="SELECT * FROM episodes WHERE ( id > "+str(get_episode_id(lastTitleList[0]))+" AND showTitle LIKE ? ) ORDER BY seasonNumber LIMIT 1 COLLATE NOCASE"

			c.execute(sql, (row[3], ))
			'''
			*
			* Try and advance to the next episode in the series, if it errs then that means it reached the end...
			*
			'''
			try:

				next_episode = list(c.fetchone())

				if next_episode > 0:

					print(next_episode[3])

					update_shows_table_with_last_episode(row[3], next_episode[3])

					print("End time: " + str(endTime)); 

					'''
					*
					* Getting the previous episodes end time to calculate offset
					*
					'''

					newStartTime = row[5]

					if prevEpisodeEndTime != None:

						newStartTime = calculate_start_time_offset_from_prev_episode_endtime(prevEpisodeEndTime, row[8], next_episode[4], prevEpDuration)

					'''
					*
					* Generate a new end time from calculated new start time
					*
					'''
					endTime = get_end_time_from_duration(newStartTime, next_episode[4]);

					print("prevEpisodeEndTime: " + str(prevEpisodeEndTime)); 

					startTimeUnix = datetime.datetime.strptime(newStartTime, '%I:%M %p')

					add_daily_schedule_to_db(0, next_episode[3], next_episode[5], next_episode[6], row[3], next_episode[4], newStartTime, endTime, row[7], startTimeUnix)

					prevEpisodeEndTime = endTime

					prevEpDuration = next_episode[4]

					datalistLengthMonitor += 1

					if datalistLengthMonitor >= len(datalist):

						write_schedule_to_file(get_html_from_daily_schedule())

				else:

					print("Not grabbing next episode for some reason")

			except Exception as e:

				#raise e
				'''
				*
				* Let's assume that this error is always because we hit the end of the series and start over...
				*
				'''    
				first_episode = get_first_episode(row[3])

				first_episode_title = first_episode[3]

				print(first_episode_title)

				update_shows_table_with_last_episode(row[3], first_episode_title)

				newStartTime = row[5]

				if prevEpisodeEndTime != None:

					newStartTime = calculate_start_time_offset_from_prev_episode_endtime(prevEpisodeEndTime, row[8], first_episode[4], prevEpDuration)

				'''
				*
				* Generate a new end time from calculated new start time
				*
				'''
				endTime = get_end_time_from_duration(newStartTime, first_episode[4]);

				print("prevEpisodeEndTime: " + str(prevEpisodeEndTime)); 

				startTimeUnix = datetime.datetime.strptime(newStartTime, '%I:%M %p')

				add_daily_schedule_to_db(0, first_episode[3], first_episode[5], first_episode[6], row[3], first_episode[4], newStartTime, endTime, row[7], startTimeUnix)


				prevEpisodeEndTime = endTime

				prevEpDuration = next_episode[4]

				datalistLengthMonitor += 1

				if datalistLengthMonitor >= len(datalist):

					write_schedule_to_file(get_html_from_daily_schedule())


generate_daily_schedule()

#SELECT title, showTitle, episodeNumber, seasonNumber FROM episodes WHERE ( showTitle LIKE "seinfeld") ORDER BY seasonNumber COLLATE NOCASE