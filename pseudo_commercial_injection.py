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


def get_all_commercials_in_order_from_shortest_to_longest():

	ascendingCommercialsSQL = "SELECT * FROM commercials ORDER BY duration ASC"

	c.execute(ascendingCommercialsSQL)

	ascendingCommercialsList = list(c.fetchall())

	return ascendingCommercialsList


def get_random_commercial():

	'''
	*
	* Getting a random commercial that will be the commercial we use to find the best fit for the remaining gap.
	*
	'''
	randomCommercialSQL = "SELECT * FROM commercials WHERE id IN (SELECT id FROM commercials ORDER BY RANDOM() LIMIT 1)"

	c.execute(randomCommercialSQL)

	randomCommercial = list(c.fetchone())

	print("Random commercial " + str(randomCommercial))

	return randomCommercial

def get_commercials_to_fill_up_gap(gapToFill):

	print("Looping through commercials to find good fits for the gap")

	randomCommercial = get_random_commercial()

	randomCommercialDuration = randomCommercial[4]

	'''
	*
	* Get all commercials ordered from shortest to longest to use second.
	*
	'''
	ascendingCommercialsList = 	get_all_commercials_in_order_from_shortest_to_longest()

	firstAscendingCommercialsList = ascendingCommercialsList[0]

	print("gapToFill - randomCommercialDuration")
	print(str(gapToFill - randomCommercialDuration))
	print(str(gapToFill - randomCommercialDuration))

	'''
	*
	* If gapToFill is shorter than the shortest commercial then return empty list
	*
	'''

	if gapToFill < firstAscendingCommercialsList[4]:

		print("firstAscendingCommercialsList[4] < gapToFill:")
		print(firstAscendingCommercialsList[4])

		return [-1, -1]

	# print(ascendingCommercialsList)

	if gapToFill - randomCommercialDuration < 0:

		print("the random commercial is longer than the gap")

	if (gapToFill - randomCommercialDuration) > ascendingCommercialsList[0][4]:

		print(ascendingCommercialsList[0][4])

		print("Gap to fill minus the random commercial is still more than at least the shortest commercial in the library.")

		usableCommercialist = []

		usableCommercial = None

		for row in ascendingCommercialsList:

			# print(gapToFill - randomCommercialDuration)

			if (gapToFill - randomCommercialDuration) <= row[4]:

				# usableCommercialist.append(row)

				# usableCommercial = row


				# print("assigning usable commercial to var")
				print(row)

				

			else:

				pass

	else:

		print("Random commercial duration: "+str(randomCommercialDuration))
		print("Gap to fill duration: "+str(gapToFill))
		print("gapToFill - randomCommercialDuration: "+str(gapToFill - randomCommercialDuration))
		print("Gap to fill minus random commercial is not more than the shortest commercial")


get_commercials_to_fill_up_gap(20000)