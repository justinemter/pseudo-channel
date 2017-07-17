#!/usr/bin/python

from plexapi.server import PlexServer
from datetime import datetime
import sqlite3
from HTMLParser import HTMLParser

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
* Get HTML from Scheduled Content to save to file
*
'''
def get_html_from_daily_schedule(currentTime):

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

									timeB = datetime.strptime(row[8], '%I:%M %p')

									if currentTime.hour == timeB.hour:

										if currentTime.minute == timeB.minute:
								
											with tag('td', klass='bg-info'):

												text(row[8])

									else:

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


'''
*
* Play Media
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
* Check DB / current time. If that matches a scheduled shows startTime then trigger play via Plex API
*
'''
def tv_controller():

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

				write_schedule_to_file(get_html_from_daily_schedule(timeB))

				my_logger.debug('Trying to play: ' + row[3])

				break




tv_controller()

#showConnectedClients()

#playMovie()
#play_media("TV Shows", "The Office (US)", "Garage Sale")