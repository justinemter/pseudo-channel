#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import signal
import datetime
from datetime import time
from time import mktime as mktime
import logging
import calendar
import itertools
import argparse
import textwrap
import os, sys
from xml.dom import minidom
import xml.etree.ElementTree as ET
import json
from pprint import pprint
import random
import re
from plexapi.server import PlexServer
import schedule
from time import sleep
from src import PseudoChannelDatabase
from src import Movie
from src import Commercial
from src import Episode
from src import Music
from src import Video
from src import PseudoDailyScheduleController
from src import PseudoChannelCommercial
from src import PseudoChannelRandomMovie
import pseudo_config as config

reload(sys)
sys.setdefaultencoding('utf-8')

class PseudoChannel():

    PLEX = PlexServer(config.baseurl, config.token)
    MEDIA = []
    GKEY = config.gkey
    USING_COMMERCIAL_INJECTION = config.useCommercialInjection
    DAILY_UPDATE_TIME = config.dailyUpdateTime
    APP_TIME_FORMAT_STR = '%I:%M:%S %p'
    COMMERCIAL_PADDING_IN_SECONDS = config.commercialPadding
    CONTROLLER_SERVER_PATH = config.controllerServerPath
    CONTROLLER_SERVER_PORT = config.controllerServerPort
    USE_OVERRIDE_CACHE = config.useDailyOverlapCache
    DEBUG = config.debug_mode
    ROTATE_LOG = config.rotateLog
    USE_DIRTY_GAP_FIX = config.useDirtyGapFix

    def __init__(self):

        logging.basicConfig(filename="pseudo-channel.log", level=logging.INFO)
        self.db = PseudoChannelDatabase("pseudo-channel.db")
        self.controller = PseudoDailyScheduleController(
            config.baseurl, 
            config.token, 
            config.plexClients,
            self.CONTROLLER_SERVER_PATH,
            self.CONTROLLER_SERVER_PORT,
            self.DEBUG
        )

        self.movieMagic = PseudoChannelRandomMovie()

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
        libs_dict = config.plexLibraries
        sections = self.PLEX.library.sections()
        for section in sections:
            for correct_lib_name, user_lib_name in libs_dict.items():
                if section.title.lower() in [x.lower() for x in user_lib_name]:
                    if correct_lib_name == "Movies":
                        sectionMedia = self.PLEX.library.section(section.title).all()
                        for i, media in enumerate(sectionMedia):
                            self.db.add_movies_to_db(1, media.title, media.duration, media.key, section.title)
                            self.print_progress(
                                    i + 1, 
                                    len(sectionMedia), 
                                    prefix = 'Progress '+section.title+":     ", 
                                    suffix = 'Complete', 
                                    bar_length = 40
                                )
                    elif correct_lib_name == "TV Shows":
                        sectionMedia = self.PLEX.library.section(section.title).all()
                        for i, media in enumerate(sectionMedia):
                            backgroundImagePath = self.PLEX.library.section(section.title).get(media.title)
                            backgroundImgURL = ''
                            if isinstance(backgroundImagePath.art, str):
                                backgroundImgURL = config.baseurl+backgroundImagePath.art+"?X-Plex-Token="+config.token
                            self.db.add_shows_to_db(2, media.title, media.duration, '', backgroundImgURL, media.key, section.title)
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
                                            media.title,
                                            episode.key,
                                            section.title
                                        )
                                else:
                                    self.db.add_episodes_to_db(
                                            4, 
                                            episode.title, 
                                            0, 
                                            episode.index, 
                                            episode.parentIndex, 
                                            media.title,
                                            episode.key,
                                            section.title
                                        )
                    elif correct_lib_name == "Commercials":
                        print "user_lib_name", section.title
                        sectionMedia = self.PLEX.library.section(section.title).all()
                        media_length = len(sectionMedia)
                        for i, media in enumerate(sectionMedia):
                            self.db.add_commercials_to_db(3, media.title, media.duration, media.key, section.title)
                            self.print_progress(
                                i + 1, 
                                media_length, 
                                prefix = 'Progress '+section.title+":", 
                                suffix = 'Complete', 
                                bar_length = 40
                            )

    def update_schedule(self):

        """Changing dir to the schedules dir."""
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)
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
            "TV Shows" : ["series", "shows", "tv", "episodes", "tv shows", "show"],
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
                            title = time.attrib['title'] if 'title' in time.attrib else ''
                            natural_start_time = self.translate_time(time.text)
                            natural_end_time = 0
                            section = key
                            day_of_week = child.tag
                            strict_time = time.attrib['strict-time'] if 'strict-time' in time.attrib else 'false'
                            time_shift = time.attrib['time-shift'] if 'time-shift' in time.attrib else '1'
                            overlap_max = time.attrib['overlap-max'] if 'overlap-max' in time.attrib else ''
                            seriesOffset = time.attrib['series-offset'] if 'series-offset' in time.attrib else ''
                            xtra = time.attrib['xtra'] if 'xtra' in time.attrib else ''
                            
                            # start_time_unix = self.translate_time(time.text)

                            now = datetime.datetime.now()

                            start_time_unix = mktime(
                                datetime.datetime.strptime(
                                    self.translate_time(natural_start_time), 
                                    self.APP_TIME_FORMAT_STR).replace(day=now.day, month=now.month, year=now.year).timetuple()
                                )


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
                                xtra, # xtra kargs (i.e. 'director=director')
                            )

    def drop_db(self):

        self.db.drop_db()

    def drop_schedule(self):

        self.db.drop_schedule()

    def remove_all_scheduled_items():

        self.db.remove_all_scheduled_items()

    def translate_time(self, timestr):

        try:
            return datetime.datetime.strptime(timestr, '%I:%M %p').strftime(self.APP_TIME_FORMAT_STR)
        except ValueError as e:
            pass
        try:
            return datetime.datetime.strptime(timestr, '%I:%M:%S %p').strftime(self.APP_TIME_FORMAT_STR)
        except ValueError as e:
            pass
        try:
            return datetime.datetime.strptime(timestr, '%H:%M').strftime(self.APP_TIME_FORMAT_STR)
        except ValueError as e:
            pass
        return timestr

    def time_diff(self, time1,time2):
        '''
        *
        * Getting the offest by comparing both times from the unix epoch time and getting the difference.
        *
        '''
        timeA = datetime.datetime.strptime(time1, '%I:%M:%S %p')
        timeB = datetime.datetime.strptime(time2, '%I:%M:%S %p')
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
        time1 = prevEndTime.strftime('%I:%M:%S %p')
        timeB = datetime.datetime.strptime(intendedStartTime, '%I:%M:%S %p').strftime(self.APP_TIME_FORMAT_STR)
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
            #hourToUse = self.DAILY_UPDATE_TIME.split(':')[0]
            #minuteToUse = self.DAILY_UPDATE_TIME.split(':')[1]
            #now = datetime.datetime(1900, 1, 1, int(hourToUse), int(minuteToUse))
            #timeset = [(now + datetime.timedelta(minutes=int(self.OVERLAP_GAP)*n)).strftime('%H:%M') for n in range((60*24)/int(self.OVERLAP_GAP))]
            timeset=[datetime.time(h,m).strftime("%H:%M") for h,m in itertools.product(xrange(0,24),xrange(0,60,int(self.OVERLAP_GAP)))]
            #print timeset
            timeSetToUse = None
            for time in timeset:
                theTimeSetInterval = datetime.datetime.strptime(time, '%H:%M')
                if theTimeSetInterval >= prevEndTime:
                    print "++++ There is overlap. Setting new time-interval:", theTimeSetInterval
                    newStartTime = theTimeSetInterval
                    break
        elif (timeDiff >= 0) and (self.TIME_GAP != -1):
            '''
            *
            * If this value is configured, then the timeGap var in config will determine the next increment. 
            * If it is set to "15", then the show will will bump up to the next 15 minute interval past the hour.
            *
            '''
            #hourToUse = self.DAILY_UPDATE_TIME.split(':')[0]
            #minuteToUse = self.DAILY_UPDATE_TIME.split(':')[1]
            #now = datetime.datetime(1900, 1, 1, int(hourToUse), int(minuteToUse))
            #timeset = [(now + datetime.timedelta(minutes=int(self.OVERLAP_GAP)*n)).strftime('%H:%M') for n in range((60*24)/int(self.OVERLAP_GAP))]
            timeset=[datetime.time(h,m).strftime("%H:%M") for h,m in itertools.product(xrange(0,24),xrange(0,60,int(self.TIME_GAP)))]
            #print timeset
            for time in timeset:
                theTimeSetInterval = datetime.datetime.strptime(time, '%H:%M')
                tempTimeTwoStr = datetime.datetime.strptime(time1, self.APP_TIME_FORMAT_STR).strftime('%H:%M')
                formatted_time_two = datetime.datetime.strptime(tempTimeTwoStr, '%H:%M')
                if theTimeSetInterval >= formatted_time_two:
                    print "++++ Setting new time-interval:", theTimeSetInterval
                    newStartTime = theTimeSetInterval
                    break
        else:
            print("Not sure what to do here")
        return newStartTime.strftime('%I:%M:%S %p')

    def get_end_time_from_duration(self, startTime, duration):

        time = datetime.datetime.strptime(startTime, '%I:%M:%S %p')
        show_time_plus_duration = time + datetime.timedelta(milliseconds=duration)
        return show_time_plus_duration

    def generate_daily_schedule(self):

        print("#### Generating Daily Schedule")
        logging.info("##### Dropping previous daily_schedule database")
        """A fix for the duplicate entries problem that comes up occasionally."""
        self.db.drop_daily_schedule_table()
        sleep(1)
        self.db.create_daily_schedule_table()
        sleep(1)
        if self.USING_COMMERCIAL_INJECTION:
            self.commercials = PseudoChannelCommercial(
                self.db.get_commercials(),
                self.COMMERCIAL_PADDING_IN_SECONDS,
                self.USE_DIRTY_GAP_FIX
            )
        schedule = self.db.get_schedule()
        weekday_dict = {
            "0" : ["mondays", "weekdays", "everyday"],
            "1" : ["tuesdays", "weekdays", "everyday"],
            "2" : ["wednesdays", "weekdays", "everyday"],
            "3" : ["thursdays", "weekdays", "everyday"],
            "4" : ["fridays", "weekdays", "everyday"],
            "5" : ["saturdays", "weekends", "everyday"],
            "6" : ["sundays", "weekends", "everyday"],
        }
        weekno = datetime.datetime.today().weekday()
        schedule_advance_watcher = 0
        for entry in schedule:
            schedule_advance_watcher += 1
            section = entry[9]
            for key, val in weekday_dict.iteritems(): 
                if str(entry[7]) in str(val) and int(weekno) == int(key):
                    if section == "TV Shows":
                        if str(entry[3]).lower() == "random":
                            next_episode = self.db.get_random_episode()
                        else:
                            next_episode = self.db.get_next_episode(entry[3])
                        if next_episode != None:
                            try:
                                print "next_episode[9]", next_episode[9]
                            except:
                                pass
                            try:
                                customSectionName = next_episode[9]
                            except:
                                customSectionName = "TV Shows"
                            episode = Episode(
                                section, # section_type
                                next_episode[3], # title
                                entry[5], # natural_start_time
                                self.get_end_time_from_duration(self.translate_time(entry[5]), next_episode[4]), # natural_end_time
                                next_episode[4], # duration
                                entry[7], # day_of_week
                                entry[10], # is_strict_time
                                entry[11], # time_shift
                                entry[12], # overlap_max
                                next_episode[8] if len(next_episode) >= 9 else '', # plex id
                                customSectionName, # custom lib name
                                entry[3], # show_series_title
                                next_episode[5], # episode_number
                                next_episode[6], # season_number
                                )
                            self.MEDIA.append(episode)
                        else:
                            print("Cannot find TV Show Episode, {} in the local db".format(entry[3]))
                    elif section == "Movies":
                        if str(entry[3]).lower() == "random":
                            if(entry[13] != ''): # xtra params

                                """
                                Using specified Movies library names
                                """
                                movies_list = []
                                libs_dict = config.plexLibraries

                                sections = self.PLEX.library.sections()
                                for theSection in sections:
                                    for correct_lib_name, user_lib_name in libs_dict.items():
                                        if theSection.title.lower() in [x.lower() for x in user_lib_name]:
                                            print "correct_lib_name", correct_lib_name
                                            if correct_lib_name == "Movies":

                                                print "entry[13]", entry[13]
                                                movies = self.PLEX.library.section(theSection.title)
                                                
                                                try:
                                                    thestr = entry[13]
                                                    regex = re.compile(r"\b(\w+)\s*:\s*([^:]*)(?=\s+\w+\s*:|$)")
                                                    d = dict(regex.findall(thestr))
                                                    # turn values into list
                                                    for key, val in d.iteritems():
                                                        d[key] = val.split(',')
                                                    for movie in movies.search(None, **d):
                                                        movies_list.append(movie)

                                                    """the_movie = self.db.get_movie(self.movieMagic.get_random_movie_xtra(
                                                            self.db.get_movies(),# Movies DB
                                                            movies_list # XTRA List
                                                        )
                                                    )"""

                                                except:

                                                    pass

                                if (len(movies_list) > 0):

                                    the_movie = self.db.get_movie(random.choice(movies_list).title)

                                    """Updating movies table in the db with lastPlayedDate entry"""
                                    self.db.update_movies_table_with_last_played_date(the_movie[3])

                                else:
                                    
                                    print "movies_list", movies_list

                                    print("For some reason, I've failed getting movie with xtra args.")
                                    the_movie = self.db.get_random_movie()

                                    """Updating movies table in the db with lastPlayedDate entry"""
                                    self.db.update_movies_table_with_last_played_date(the_movie[3])

                            else:

                                """the_movie = self.db.get_movie(self.movieMagic.get_random_movie(
                                        self.db.get_movies(),# Movies DB
                                    )
                                )"""

                                the_movie = self.db.get_random_movie()

                                """Updating movies table in the db with lastPlayedDate entry"""
                                self.db.update_movies_table_with_last_played_date(the_movie[3])

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
                            entry[12], # overlap_max
                            the_movie[6], # plex id
                            the_movie[7] # custom lib name
                            )
                            self.MEDIA.append(movie)
                        else:
                            print str("Cannot find Movie, {} in the local db".format(entry[3])).encode('UTF-8')
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
                            entry[12], # overlap_max
                            the_music[6], # plex id
                            the_music[7], # custom lib name
                            )
                            self.MEDIA.append(music)
                        else:
                            print str("Cannot find Music, {} in the local db".format(entry[3])).encode('UTF-8')
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
                            entry[12], # overlap_max
                            the_video[6], # plex id
                            the_video[7], # custom lib name
                            )
                            self.MEDIA.append(video)
                        else:
                            print str("Cannot find Video, {} in the local db".format(entry[3])).encode('UTF-8')
                    else:
                        pass
            """If we reached the end of the scheduled items for today, add them to the daily schedule

            """
            if schedule_advance_watcher >= len(schedule):
                print "+++++ Finished processing time entries, recreating daily_schedule"
                previous_episode = None
                for entry in self.MEDIA:
                    if previous_episode != None:
                        natural_start_time = datetime.datetime.strptime(entry.natural_start_time, self.APP_TIME_FORMAT_STR)
                        natural_end_time = entry.natural_end_time
                        if entry.is_strict_time.lower() == "true":
                            print "++++ Strict-time: {}".format(str(entry.title))
                            entry.end_time = self.get_end_time_from_duration(
                                    self.translate_time(entry.start_time), 
                                    entry.duration
                                )
                            """Get List of Commercials to inject"""
                            if self.USING_COMMERCIAL_INJECTION:
                                list_of_commercials = self.commercials.get_commercials_to_place_between_media(
                                    previous_episode,
                                    entry
                                )
                                for commercial in list_of_commercials:
                                    self.db.add_media_to_daily_schedule(commercial)
                            self.db.add_media_to_daily_schedule(entry)
                            previous_episode = entry
                        else:
                            try:
                                print "++++ NOT strict-time: {}".format(str(entry.title).encode(sys.stdout.encoding, errors='replace'))
                            except:
                                pass
                            try:
                                new_starttime = self.calculate_start_time(
                                    previous_episode.end_time,
                                    entry.natural_start_time,  
                                    previous_episode.time_shift, 
                                    ""
                                )
                            except:
                                print("Error in calculate_start_time")
                            print "++++ New start time:", new_starttime
                            entry.start_time = datetime.datetime.strptime(new_starttime, self.APP_TIME_FORMAT_STR).strftime('%I:%M:%S %p')
                            entry.end_time = self.get_end_time_from_duration(entry.start_time, entry.duration)
                            """Get List of Commercials to inject"""
                            if self.USING_COMMERCIAL_INJECTION:
                                list_of_commercials = self.commercials.get_commercials_to_place_between_media(
                                    previous_episode,
                                    entry
                                )
                                for commercial in list_of_commercials:
                                    self.db.add_media_to_daily_schedule(commercial)
                            self.db.add_media_to_daily_schedule(entry)
                            previous_episode = entry
                    else:
                        self.db.add_media_to_daily_schedule(entry)
                        previous_episode = entry
                #self.make_xml_schedule()

    def run_commercial_injection(self):

        pass

    def make_xml_schedule(self):

        self.controller.make_xml_schedule(self.db.get_daily_schedule())

    def show_clients(self):

        print "##### Connected Clients:"
        for i, client in enumerate(self.PLEX.clients()):
            print "+++++", str(i + 1)+".", "Client:", client.title

    def show_schedule(self):

        print "##### Daily Pseudo Schedule:"
        daily_schedule = self.db.get_daily_schedule()
        for i , entry in enumerate(daily_schedule):
            print str("+++++ {} {} {} {} {} {}".format(str(i + 1)+".", entry[8], entry[11], entry[6], " - ", entry[3])).encode(sys.stdout.encoding, errors='replace')

    def write_json_to_file(self, data):

        fileName = "pseudo-queue.json"
        writepath = './'
        if os.path.exists(writepath+fileName):
            os.remove(writepath+fileName)
        mode = 'a' if os.path.exists(writepath) else 'w'
        with open(writepath+fileName, mode) as f:
            f.write(data)

    def export_queue(self):

        shows_table = self.db.get_shows_table()
        json_string = json.dumps(shows_table)
        print "+++++ Exporting queue "
        self.write_json_to_file(json_string)
        print "+++++ Done."

    def import_queue(self):

        """Dropping previous shows table before adding the imported data"""
        self.db.clear_shows_table()
        with open('pseudo-queue.json') as data_file:    
            data = json.load(data_file)
        #pprint(data)
        for row in data:
            print row
            self.db.import_shows_table_by_row(row[2], row[3], row[4], row[5], row[6], row[7])
        print "+++++ Done. Imported queue."

    def get_daily_schedule_cache_as_json(self):

        data = []
        try:
            with open('../.pseudo-cache/daily-schedule.json') as data_file:    
                data = json.load(data_file)
            #pprint(data)
        except IOError:
            print ("----- Having issues opening the pseudo-cache file.")
        return data

    def save_daily_schedule_as_json(self):

        daily_schedule_table = self.db.get_daily_schedule()
        json_string = json.dumps(daily_schedule_table)
        print "+++++ Saving Daily Schedule Cache "
        self.save_file(json_string, 'daily-schedule.json', '../.pseudo-cache/')

    def save_file(self, data, filename, path="./"):

        fileName = filename
        writepath = path
        if not os.path.exists(writepath):
            os.makedirs(writepath)
        if os.path.exists(writepath+fileName):
            os.remove(writepath+fileName)
        mode = 'a' if os.path.exists(writepath) else 'w'
        with open(writepath+fileName, mode) as f:
            f.write(data)

    def rotate_log(self):

        try:
            os.remove('../pseudo-channel.log')
        except OSError:
            pass
        try:
            os.remove('./pseudo-channel.log')
        except OSError:
            pass

    def signal_term_handler(self, signal, frame):

        logging.info('+++++ got SIGTERM')
        self.controller.stop_media()
        self.exit_app()
        sys.exit(0)

    def exit_app(self):

        logging.info(' - Exiting Pseudo TV & cleaning up.')
        for i in self.MEDIA:
            del i
        self.MEDIA = None
        self.controller = None
        self.db = None
        sleep(1)

if __name__ == '__main__':

    pseudo_channel = PseudoChannel()
    banner = textwrap.dedent('''\
#   __              __                        
#  |__)_ _    _| _ /  |_  _  _  _  _|    _    
#  |  _)(-|_|(_|(_)\__| )(_|| )| )(-|.  |_)\/ 
#                                       |  /  

            A Custom TV Channel for Plex
''')
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description = banner)
    '''
    * 
    * Primary arguments: "python PseudoChannel.py -u -xml -g -r"
    *
    '''
    parser.add_argument('-u', '--update',
                         action='store_true',
                         help='Update the local database with Plex libraries.')
    parser.add_argument('-xml', '--xml',
                         action='store_true', 
                         help='Update the local database with the pseudo_schedule.xml.')
    parser.add_argument('-g', '--generate_schedule',
                         action='store_true', 
                         help='Generate the daily schedule.')
    parser.add_argument('-r', '--run',
                         action='store_true', 
                         help='Run this program.')
    '''
    * 
    * Show connected clients: "python PseudoChannel.py -c"
    *
    '''
    parser.add_argument('-c', '--show_clients',
                         action='store_true',
                         help='Show Plex clients.')
    '''
    * 
    * Show schedule (daily): "python PseudoChannel.py -s"
    *
    '''
    parser.add_argument('-s', '--show_schedule',
                         action='store_true',
                         help='Show scheduled media for today.')
    '''
    * 
    * Make XML / HTML Schedule: "python PseudoChannel.py -m"
    *
    '''
    parser.add_argument('-m', '--make_html',
                         action='store_true',
                         help='Makes the XML / HTML schedule based on the daily_schedule table.')
    '''
    * 
    * Export queue: "python PseudoChannel.py -e"
    *
    '''
    parser.add_argument('-e', '--export_queue',
                         action='store_true',
                         help='Exports the current queue for episodes.')
    '''
    * 
    * Import queue: "python PseudoChannel.py -i"
    *
    '''
    parser.add_argument('-i', '--import_queue',
                         action='store_true',
                         help='Imports the current queue for episodes.')
    globals().update(vars(parser.parse_args()))
    args = parser.parse_args()
    if args.update:
        pseudo_channel.update_db()
    if args.xml:
        pseudo_channel.update_schedule()
    if args.generate_schedule:
        if pseudo_channel.DEBUG:
            pseudo_channel.generate_daily_schedule()
        else:
            try:
                pseudo_channel.generate_daily_schedule()
            except:
                print("----- Recieved error when running generate_daily_schedule()")
    if args.show_clients:
        pseudo_channel.show_clients()
    if args.show_schedule:
        pseudo_channel.show_schedule()
    if args.make_html:
        pseudo_channel.make_xml_schedule()
    if args.export_queue:
        pseudo_channel.export_queue()
    if args.import_queue:
        pseudo_channel.import_queue()
    if args.run:
        print banner
        print "+++++ To run this in the background:"
        print "+++++", "screen -d -m bash -c 'python PseudoChannel.py -r; exec sh'"
        """Every minute on the minute check the DB startTimes of all media to 
           determine whether or not to play. Also, check the now_time to
           see if it's midnight (or 23.59), if so then generate a new daily_schedule
            
        """
        """Every <user specified day> rotate log"""
        dayToRotateLog = pseudo_channel.ROTATE_LOG.lower()
        schedule.every().friday.at("00:00").do(pseudo_channel.rotate_log)
        logging.info("+++++ Running PseudoChannel.py -r")
        def trigger_what_should_be_playing_now():

            def nearest(items, pivot):
                return min(items, key=lambda x: abs(x - pivot))

            daily_schedule = pseudo_channel.db.get_daily_schedule()
            dates_list = [datetime.datetime.strptime(''.join(str(date[8])), "%I:%M:%S %p") for date in daily_schedule]
            now = datetime.datetime.now()
            now = now.replace(year=1900, month=1, day=1)
            closest_media = nearest(dates_list, now)
            print closest_media
            prevItem = None

            for item in daily_schedule:
                item_time = datetime.datetime.strptime(''.join(str(item[8])), "%I:%M:%S %p")

                if item_time == closest_media:
                    #print "Line 1088, Here", item
                    elapsed_time = closest_media - now
                    print elapsed_time.total_seconds()
                    try:
                        endTime = datetime.datetime.strptime(item[9], '%Y-%m-%d %H:%M:%S.%f')
                    except ValueError:
                        endTime = datetime.datetime.strptime(item[9], '%Y-%m-%d %H:%M:%S')
                    # we need to play the content and add an offest
                    if elapsed_time.total_seconds() < 0 and \
                       endTime > now:
                        print str("+++++ Queueing up {} to play right away.".format(item[3])).encode('UTF-8')
                        offset = int(abs(elapsed_time.total_seconds() * 1000))
                        pseudo_channel.controller.play(item, daily_schedule, offset)
                        break
                    elif elapsed_time.total_seconds() >= 0:
                        for itemTwo in daily_schedule:
                            item_timeTwo = datetime.datetime.strptime(''.join(str(itemTwo[8])), "%I:%M:%S %p")
                            try:
                                endTime = datetime.datetime.strptime(itemTwo[9], '%Y-%m-%d %H:%M:%S.%f')
                            except ValueError:
                                endTime = datetime.datetime.strptime(itemTwo[9], '%Y-%m-%d %H:%M:%S')
                            if item_timeTwo == closest_media and prevItem != None and \
                               endTime > now:
                                prevItem_time = datetime.datetime.strptime(''.join(str(prevItem[8])), "%I:%M:%S %p")
                                elapsed_timeTwo = prevItem_time - now
                                offsetTwo = int(abs(elapsed_timeTwo.total_seconds() * 1000))
                                if pseudo_channel.DEBUG:
                                    print "+++++ Closest media was the next media " \
                                          "but we were in the middle of something so triggering that instead."
                                print str("+++++ Queueing up '{}' to play right away.".format(prevItem[3])).encode('UTF-8')
                                pseudo_channel.controller.play(prevItem, daily_schedule, offsetTwo)
                                break
                            prevItem = itemTwo

        def job_that_executes_once(item, schedulelist):

            print str("##### Readying media: '{}'".format(item[3])).encode('UTF-8')
            next_start_time = datetime.datetime.strptime(item[8], "%I:%M:%S %p")
            now = datetime.datetime.now()
            now = now.replace(year=1900, month=1, day=1)
            time_diff = next_start_time - now

            if time_diff.total_seconds() > 0:
                print "+++++ Sleeping for {} seconds before playing: '{}'".format(time_diff.total_seconds(), item[3])
                sleep(int(time_diff.total_seconds()))
                if pseudo_channel.DEBUG:
                    print "+++++ Woke up!"
                pseudo_channel.controller.play(item, schedulelist)
            else:
                pseudo_channel.controller.play(item, schedulelist)
            return schedule.CancelJob
        def generate_memory_schedule(schedulelist, isforupdate=False):

            print "##### Generating Memory Schedule."
            now = datetime.datetime.now()
            now = now.replace(year=1900, month=1, day=1)
            pseudo_cache = pseudo_channel.get_daily_schedule_cache_as_json()
            prev_end_time_to_watch_for = None
            if pseudo_channel.USE_OVERRIDE_CACHE and isforupdate:
                for cached_item in pseudo_cache:
                    prev_start_time = datetime.datetime.strptime(cached_item[8], "%I:%M:%S %p")
                    try:
                        prev_end_time = datetime.datetime.strptime(cached_item[9], '%Y-%m-%d %H:%M:%S.%f')
                    except ValueError:
                        prev_end_time = datetime.datetime.strptime(cached_item[9], '%Y-%m-%d %H:%M:%S')
                    """If update time is in between the prev media start / stop then there is overlap"""
                    if prev_start_time < now and prev_end_time > now:
                        try:
                            print "+++++ It looks like there is update schedule overlap", cached_item[3]
                        except:
                            pass
                        prev_end_time_to_watch_for = prev_end_time
            for item in schedulelist:
                trans_time = datetime.datetime.strptime(item[8], "%I:%M:%S %p").strftime("%H:%M")
                new_start_time = datetime.datetime.strptime(item[8], "%I:%M:%S %p")
                if prev_end_time_to_watch_for == None:
                    schedule.every().day.at(trans_time).do(job_that_executes_once, item, schedulelist).tag('daily-tasks')
                else:
                    """If prev end time is more then the start time of this media, skip it"""
                    if prev_end_time_to_watch_for > new_start_time:
                        try:
                            print "Skipping scheduling item do to cached overlap.", item[3]
                        except:
                            pass
                        continue
                    else:
                        schedule.every().day.at(trans_time).do(job_that_executes_once, item, schedulelist).tag('daily-tasks')
            print "+++++ Done."
        generate_memory_schedule(pseudo_channel.db.get_daily_schedule())
        daily_update_time = datetime.datetime.strptime(
            pseudo_channel.translate_time(
                pseudo_channel.DAILY_UPDATE_TIME
            ),
            pseudo_channel.APP_TIME_FORMAT_STR
        ).strftime('%H:%M')

        def go_generate_daily_sched():

            """Saving current daily schedule as cached .json"""
            pseudo_channel.save_daily_schedule_as_json()

            schedule.clear('daily-tasks')

            sleep(1)

            try:
                pseudo_channel.generate_daily_schedule()
            except:
                print("----- Recieved error when running generate_daily_schedule()")
            generate_memory_schedule(pseudo_channel.db.get_daily_schedule(), True)

        schedule.every().day.at(daily_update_time).do(
            go_generate_daily_sched
        ).tag('daily-update')
        sleep_before_triggering_play_now = 1

        '''When the process is killed, stop any currently playing media & cleanup'''
        signal.signal(signal.SIGTERM, pseudo_channel.signal_term_handler)

        try:
            while True:
                schedule.run_pending()
                sleep(1)
                if sleep_before_triggering_play_now:
                    logging.info("+++++ Successfully started PseudoChannel.py")
                    trigger_what_should_be_playing_now()
                    sleep_before_triggering_play_now = 0
        except KeyboardInterrupt:
            print(' Manual break by user')