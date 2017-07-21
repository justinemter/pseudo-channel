# -*- coding: utf-8 -*-

from src import PseudoChannelDatabase
from src import Movie
from src import Commercial
from src import Episode
from src import Music
from src import Video
from src import PseudoDailyScheduleController
from pseudo_config import *

from plexapi.server import PlexServer

import sys
import datetime
import calendar
import itertools
from xml.dom import minidom
import xml.etree.ElementTree as ET

from time import sleep

class PseudoChannel():

	PLEX = PlexServer(baseurl, token)

	MEDIA = []

	def __init__(self):

		self.db = PseudoChannelDatabase("pseudo-channel.db")

		self.controller = PseudoDailyScheduleController()

	"""Database functions.

		update_db(): Grab the media from the Plex DB and store it in the local pseudo-channel.db.

		drop_db(): Drop the local database. Fresh start. 

		update_schedule(): Update schedule with user defined times.

		drop_schedule(): Drop the user defined schedule table. 

		generate_daily_schedule(): Generates daily schedule based on the "schedule" table.
	"""

	# Print iterations progress
	def print_progress(self, iteration, total, prefix='', suffix='', decimals=1, bar_length=100):
	    """
	    Call in a loop to create terminal progress bar
	    @params:
	        iteration   - Required  : current iteration (Int)
	        total       - Required  : total iterations (Int)
	        prefix      - Optional  : prefix string (Str)
	        suffix      - Optional  : suffix string (Str)
	        decimals    - Optional  : positive number of decimals in percent complete (Int)
	        bar_length  - Optional  : character length of bar (Int)
	    """
	    str_format = "{0:." + str(decimals) + "f}"
	    percents = str_format.format(100 * (iteration / float(total)))
	    filled_length = int(round(bar_length * iteration / float(total)))
	    bar = '█' * filled_length + '-' * (bar_length - filled_length)

	    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),

	    if iteration == total:
	        sys.stdout.write('\n')
	    sys.stdout.flush()

	def update_db(self):

		print("#### Updating Local Database")

		self.db.create_tables()

		sections = self.PLEX.library.sections()

		for section in sections:

			if section.title == "Movies":

				sectionMedia = self.PLEX.library.section(section.title).all()

				for i, media in enumerate(sectionMedia):

					self.db.add_movies_to_db(1, media.title, media.duration)

					self.print_progress(
							i + 1, 
							len(sectionMedia), 
							prefix = 'Progress '+section.title+":     ", 
							suffix = 'Complete', 
							bar_length = 40
						)


			elif section.title == "TV Shows":

				sectionMedia = self.PLEX.library.section(section.title).all()

				for i, media in enumerate(sectionMedia):

					backgroundImagePath = self.PLEX.library.section(section.title).get(media.title)

					backgroundImgURL = ''

					if isinstance(backgroundImagePath.art, str):

						backgroundImgURL = baseurl+backgroundImagePath.art+"?X-Plex-Token="+token

					self.db.add_shows_to_db(2, media.title, media.duration, '', backgroundImgURL)

					self.print_progress(
							i + 1, 
							len(sectionMedia),
							prefix = 'Progress '+section.title+":   ", 
							suffix = 'Complete', 
							bar_length = 40
						)

					#add all episodes of each tv show to episodes table
					episodes = self.PLEX.library.section(section.title).get(media.title).episodes()

					for episode in episodes:

						duration = episode.duration

						if duration:

							self.db.add_episodes_to_db(
									4, 
									episode.title, 
									duration, 
									episode.index, 
									episode.parentIndex, 
									media.title
								)

						else:

							self.db.add_episodes_to_db(
									4, 
									episode.title, 
									0, 
									episode.index, 
									episode.parentIndex, 
									media.title
								)

			elif section.title == "Commercials":

				sectionMedia = self.PLEX.library.section(section.title).all()

				media_length = len(sectionMedia)

				for i, media in enumerate(sectionMedia):

					self.db.add_commercials_to_db(3, media.title, media.duration)

					self.print_progress(
						i + 1, 
						media_length, 
						prefix = 'Progress '+section.title+":", 
						suffix = 'Complete', 
						bar_length = 40
					)

	def update_schedule(self):

		self.db.create_tables()

		self.db.remove_all_scheduled_items()

		scheduled_days_list = [
			"mondays",
			"tuesdays",
			"wednesdays",
			"thursdays",
			"fridays",
			"saturdays",
			"sundays",
			"weekdays",
			"weekends",
			"everyday"
		]

		section_dict = {
			"TV Shows" : ["series", "shows", "tv", "episodes", "tv shows"],
			"Movies"   : ["movie", "movies", "films", "film"],
			"Videos"   : ["video", "videos", "vid"],
			"Music"    : ["music", "songs", "song", "tune", "tunes"]
		}

		tree = ET.parse('pseudo_schedule.xml')

		root = tree.getroot()

		for child in root:

			if child.tag in scheduled_days_list:

				for time in child.iter("time"):

					for key, value in section_dict.items():

						if time.attrib['type'] == key or time.attrib['type'] in value:

							title = time.attrib['title']

							natural_start_time = time.text

							natural_end_time = 0

							section = key

							day_of_week = child.tag

							strict_time = time.attrib['strict-time']

							time_shift = time.attrib['time-shift']

							overlap_max = time.attrib['overlap-max']

							start_time_unix = datetime.datetime.strptime(time.text, '%I:%M %p')

							print "Adding: ", time.tag, section, time.text, time.attrib['title']

							self.db.add_schedule_to_db(
								0, # mediaID
								title, # title
								0, # duration
								natural_start_time, # startTime
								natural_end_time, # endTime
								day_of_week, # dayOfWeek
								start_time_unix, # startTimeUnix
								section, # section
								strict_time, # strictTime
								time_shift, # timeShift
								overlap_max, # overlapMax
							)

	def drop_db(self):

		self.db.drop_db()

	def drop_schedule(self):

		self.db.drop_schedule()

	def remove_all_scheduled_items():

		self.db.remove_all_scheduled_items()



	"""App functions.

		generate_daily_schedule(): Generate the daily_schedule table.
	"""

	'''
	*
	* Using datetime to figure out when the media item will end based on the scheduled start time or the offset 
	* generated by the previous media item. 

	* Returns time 
	*
	'''
	'''
	*
	* Returns time difference in minutes
	*
	'''
	def time_diff(self, time1,time2):
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
	def calculate_start_time(self, prevEndTime, intendedStartTime, timeGap, overlapMax):

		self.TIME_GAP = timeGap

		self.OVERLAP_GAP = timeGap

		self.OVERLAP_MAX = overlapMax

		time1 = prevEndTime.strftime('%-I:%M %p')

		timeB = datetime.datetime.strptime(intendedStartTime, '%I:%M %p').strftime('%-I:%M %p')

		print "++++ Previous End Time: ", time1, "Intended start time: ", timeB

		timeDiff = self.time_diff(time1, timeB)

		"""print("timeDiff "+ str(timeDiff))
		print("startTimeUNIX: "+ str(intendedStartTime))"""

		newTimeObj = timeB

		newStartTime = timeB

		'''
		*
		* If time difference is negative, then we know there is overlap
		*
		'''
		if timeDiff < 0:
			'''
			*
			* If there is an overlap, then the overlapGap var in config will determine the next increment. If it is set to "15", then the show will will bump up to the next 15 minute interval past the hour.
			*
			'''
			timeset=[datetime.time(h,m).strftime("%H:%M") for h,m in itertools.product(xrange(0,24),xrange(0,60,int(self.OVERLAP_GAP)))]
			
			#print(timeset)

			timeSetToUse = None

			for time in timeset:

				#print(time)
				theTimeSetInterval = datetime.datetime.strptime(time, '%H:%M')

				# print(theTimeSetInterval)

				# print(prevEndTime)

				if theTimeSetInterval >= prevEndTime:

					print "++++ There is overlap. Setting new time-interval:", theTimeSetInterval

					newStartTime = theTimeSetInterval

					break

				#newStartTime = newTimeObj + datetime.timedelta(minutes=abs(timeDiff + overlapGap))

		elif (timeDiff >= 0) and (self.TIME_GAP != -1):

			'''
			*
			* If there this value is configured, then the timeGap var in config will determine the next increment. If it is set to "15", then the show will will bump up to the next 15 minute interval past the hour.
			*
			'''
			timeset=[datetime.time(h,m).strftime("%H:%M") for h,m in itertools.product(xrange(0,24),xrange(0,60,int(self.TIME_GAP)))]
			
			# print(timeset)

			for time in timeset:

				theTimeSetInterval = datetime.datetime.strptime(time, '%H:%M')

				tempTimeTwoStr = datetime.datetime.strptime(time1, '%I:%M %p').strftime('%H:%M')

				formatted_time_two = datetime.datetime.strptime(tempTimeTwoStr, '%H:%M')

				if theTimeSetInterval >= formatted_time_two:

					print "++++ Setting new time-interval:", theTimeSetInterval

					newStartTime = theTimeSetInterval

					break

		else:

			print("Not sure what to do here")

		return newStartTime.strftime('%-I:%M %p')

	def get_end_time_from_duration(self, startTime, duration):

		time = datetime.datetime.strptime(startTime, '%I:%M %p')

		show_time_plus_duration = time + datetime.timedelta(milliseconds=duration)

		#print(show_time_plus_duration.minute)

		return show_time_plus_duration

	def generate_daily_schedule(self):

		print("#### Generating Daily Schedule")

		schedule = self.db.get_schedule()

		schedule_advance_watcher = 0

		for entry in schedule:

			schedule_advance_watcher += 1

			section = entry[9]

			if section == "TV Shows":

				if entry[3] == "random":

					next_episode = self.db.get_random_episode()

				else:

					next_episode = self.db.get_next_episode(entry[3])

				if next_episode != None:
				
					episode = Episode(
						section, # section_type
						next_episode[3], # title
						entry[5], # natural_start_time
						self.get_end_time_from_duration(entry[5], next_episode[4]), # natural_end_time
						next_episode[4], # duration
						entry[7], # day_of_week
						entry[10], # is_strict_time
						entry[11], # time_shift
						entry[12], # overlap_max
						entry[3], # show_series_title
						next_episode[5], # episode_number
						next_episode[6] # season_number
						)

					self.MEDIA.append(episode)

				else:

					print("Cannot find TV Show Episode, {} in the local db".format(entry[3]))

				#print(episode)

			elif section == "Movies":

				if entry[3] == "random":

					the_movie = self.db.get_random_movie()
					print("here")

				else:

					the_movie = self.db.get_movie(entry[3])

				if the_movie != None:

					movie = Movie(
					section, # section_type
					the_movie[3], # title
					entry[5], # natural_start_time
					self.get_end_time_from_duration(entry[5], the_movie[4]), # natural_end_time
					the_movie[4], # duration
					entry[7], # day_of_week
					entry[10], # is_strict_time
					entry[11], # time_shift
					entry[12] # overlap_max
					)

					#print(movie.natural_end_time)

					self.MEDIA.append(movie)

				else:

					print("Cannot find Movie, {} in the local db".format(entry[3]))

			elif section == "Music":

				the_music = self.db.get_music(entry[3])

				if the_music != None:

					music = Music(
					section, # section_type
					the_music[3], # title
					entry[5], # natural_start_time
					self.get_end_time_from_duration(entry[5], the_music[4]), # natural_end_time
					the_music[4], # duration
					entry[7], # day_of_week
					entry[10], # is_strict_time
					entry[11], # time_shift
					entry[12] # overlap_max
					)

					#print(music.natural_end_time)

					self.MEDIA.append(music)

				else:

					print("Cannot find Music, {} in the local db".format(entry[3]))

			elif section == "Video":

				the_video = self.db.get_video(entry[3])

				if the_music != None:

					video = Video(
					section, # section_type
					the_video[3], # title
					entry[5], # natural_start_time
					self.get_end_time_from_duration(entry[5], the_video[4]), # natural_end_time
					the_video[4], # duration
					entry[7], # day_of_week
					entry[10], # is_strict_time
					entry[11], # time_shift
					entry[12] # overlap_max
					)

					#print(music.natural_end_time)

					self.MEDIA.append(video)

				else:

					print("Cannot find Video, {} in the local db".format(entry[3]))

			else:

				pass

			"""If we reached the end of the schedule we are ready to kick off the daily_schedule

			"""
			if schedule_advance_watcher >= len(schedule):

				previous_episode = None

				self.db.remove_all_daily_scheduled_items()

				for entry in self.MEDIA:

					#print entry.natural_end_time

					if previous_episode != None:

						natural_start_time = datetime.datetime.strptime(entry.natural_start_time, '%I:%M %p')

						natural_end_time = entry.natural_end_time

						if entry.is_strict_time.lower() == "true":

							print "++++ Strict-time: {}".format(entry.title)

							entry.end_time = self.get_end_time_from_duration(entry.start_time, entry.duration)

							self.db.add_media_to_daily_schedule(entry)

							previous_episode = entry

						else:

							print "++++ NOT strict-time: {}".format(entry.title)

							new_starttime = self.calculate_start_time(
								previous_episode.end_time,
								entry.natural_start_time,  
								previous_episode.time_shift, 
								previous_episode.overlap_max
							)

							print "++++ New start time:", new_starttime

							entry.start_time = datetime.datetime.strptime(new_starttime, '%I:%M %p').strftime('%-I:%M %p')

							entry.end_time = self.get_end_time_from_duration(entry.start_time, entry.duration)

							self.db.add_media_to_daily_schedule(entry)

							previous_episode = entry

					else:

						self.db.add_media_to_daily_schedule(entry)

						previous_episode = entry

if __name__ == '__main__':

	pseudo_channel = PseudoChannel()

	#pseudo_channel.db.create_tables()

	#pseudo_channel.update_db()

	#pseudo_channel.update_schedule()

	#pseudo_channel.generate_daily_schedule()

	try:
		print "++++ Running TV Controller"
		while True:
			pseudo_channel.controller.tv_controller(pseudo_channel.db.get_daily_schedule())
			t = datetime.datetime.utcnow()
			sleeptime = 60 - (t.second + t.microsecond/1000000.0)
			sleep(sleeptime)
	except KeyboardInterrupt, e:
	    pass



