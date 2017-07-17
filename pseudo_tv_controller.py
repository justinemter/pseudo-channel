#!/usr/bin/python

'''
*
* This script is to be run every ~minute or so to check the "now" time from the schedule media time. 
* When there is a match (i.e. now() time == startTime of scheduled content), then trigger play and
* ...generate the html schedule / save it to "./schedules" dir.
*
* 

Below is my recommended "crontab" setting to trigger this script every minute:

"crontab -e"

"* * * * * cd /home/justin/pseudo-channel/ && /usr/bin/python /home/justin/pseudo-channel/pseudo_tv_controller.py"

*
'''

from plexapi.server import PlexServer
from datetime import datetime
import sqlite3

from yattag import Doc
import os, sys

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

'''
*
* Get the keys / values of any python object for debugginh - helper
* @param obj: any object
* @return null
*
'''
def dump(obj):

  for attr in dir(obj):

    print "obj.%s = %s" % (attr, getattr(obj, attr))

'''
*
* Get the full image url (including plex token) from the local db.
* @param seriesTitle: case-unsensitive string of the series title
* @return string: full path of to the show image
*
'''
def get_show_photo(seriesTitle):

	c.execute("SELECT fullImageURL FROM shows WHERE title = ? COLLATE NOCASE", (seriesTitle, ))

	datalist = list(c.fetchone())

	backgroundImgURL = ''

	if len(datalist):
		backgroundImgURL = datalist[0]

	return backgroundImgURL

'''
*
* Get the generated html for the .html file that is the schedule. 
* ...This is used whenever a show starts or stops in order to add and remove various styles.
* @param currentTime: datetime object 
* @param bgImageURL: str of the image used for the background
* @return string: the generated html content
*
'''
def get_html_from_daily_schedule(currentTime, bgImageURL):

	now = datetime.now()

	time = now.strftime("%B %d, %Y")

	doc, tag, text, line = Doc(

    ).ttl()

	doc.asis('<!DOCTYPE html>')

	with tag('html'):

		with tag('head'):

			with tag('title'):

				text(time + " - Daily Pseudo Schedule")

			doc.asis('<link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" rel="stylesheet">')
			doc.asis('<script>setTimeout(function() {location.reload();}, 30000);</script>')

			if bgImageURL != None:
				doc.asis('<style>body{ background:transparent!important; } html { background: url('+bgImageURL+') no-repeat center center fixed; -webkit-background-size: cover;-moz-background-size: cover;-o-background-size: cover;background-size: cover;}.make-white { padding: 24px; background:rgba(255,255,255, 0.9); }</style>')

        with tag('body'):

        	with tag('div', klass='container mt-3'):

				with tag('div', klass='row make-white'):

					with tag('div'):

						with tag('div'):

							line('h1', "Daily Pseudo Schedule", klass='col-12 pl-0')

						with tag('div'):

							line('h3', time, klass='col-12 pl-1')

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

								timeB = datetime.strptime(row[8], '%I:%M %p')

								if currentTime == None:

									with tag('tr'):
										with tag('th', scope='row'):
											text(numberIncrease)
										with tag('td'):
											text(row[6])
										with tag('td'):
											text(row[3])
										with tag('td'):
											text(row[8])

								elif currentTime.hour == timeB.hour and currentTime.minute == timeB.minute:

										with tag('tr', klass='bg-info'):

											with tag('th', scope='row'):
												text(numberIncrease)
											with tag('td'):
												text(row[6])
											with tag('td'):
												text(row[3])
											with tag('td'):
												text(row[8])

								else:

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

'''
*
* Create 'schedules' dir & write the generated html to .html file.
* @param data: html string
* @return null
*
'''
def write_schedule_to_file(data):

	now = datetime.now()

	fileName = "pseudo-tv_todays-schedule.html"

	writepath = './schedules/'

	if not os.path.exists(writepath):

		os.makedirs(writepath)

	if os.path.exists(writepath+fileName):
		
		os.remove(writepath+fileName)

	mode = 'a' if os.path.exists(writepath) else 'w'

	with open(writepath+fileName, mode) as f:

		f.write(data)	


'''
*
* Trigger "playMedia()" on the Python Plex API for specified media.
* @param mediaType: str: "TV Shows"
* @param mediaParentTitle: str: "Seinfeld"
* @param mediaTitle: str: "The Soup Nazi"
* @return null
*
'''
def play_media(mediaType, mediaParentTitle, mediaTitle):

	mediaItems = plex.library.section(mediaType).get(mediaParentTitle).episodes()

	for item in mediaItems:

		# print(part.title)

		if item.title == mediaTitle:

			for client in plexClients:

				clientItem = plex.client(client)

				clientItem.playMedia(item)
				
				break

'''
*
* If tv_controller() does not find a "startTime" for scheduled media, search for an "endTime" match for now time.
* ...This is usefule for clearing the generated html schedule when media ends and there is a gap before the next media.
* @param null
* @return null
*
'''
def check_for_end_time():

	currentTime = datetime.now()

	c.execute("SELECT * FROM daily_schedule")

	datalist = list(c.fetchall())

	for row in datalist:

		endTime = datetime.strptime(row[9], '%Y-%m-%d %H:%M:%S.%f')

		if currentTime.hour == endTime.hour:

			if currentTime.minute == endTime.minute:

				print("Ok end time found")

				write_schedule_to_file(get_html_from_daily_schedule(None, None))

				break
'''
*
* Check DB / current time. If that matches a scheduled shows startTime then trigger play via Plex API
* @param null
* @return null
*
'''
def tv_controller():

	datalistLengthMonitor = 0;

	currentTime = datetime.now()

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

				write_schedule_to_file(get_html_from_daily_schedule(timeB, get_show_photo(row[6])))

				my_logger.debug('Trying to play: ' + row[3])

				break

		datalistLengthMonitor += 1

		if datalistLengthMonitor >= len(datalist):

			check_for_end_time()


tv_controller()

# print(get_show_photo("the office"))