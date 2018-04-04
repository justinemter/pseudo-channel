#!/usr/bin/env python

import sqlite3
import datetime
import time

class PseudoChannelDatabase():

    def __init__(self, db):

        self.db = db
        self.conn = sqlite3.connect(self.db, check_same_thread=False)
        self.cursor = self.conn.cursor()

    """Database functions.
        Utilities, etc.
    """
    def create_tables(self):

        self.cursor.execute('CREATE TABLE IF NOT EXISTS '
                  'movies(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                  'unix INTEGER, mediaID INTEGER, title TEXT, duration INTEGER, '
                  'lastPlayedDate TEXT, plexMediaID TEXT, customSectionName Text)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS '
                  'videos(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                  'unix INTEGER, mediaID INTEGER, title TEXT, duration INTEGER, plexMediaID TEXT, customSectionName Text)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS '
                  'music(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                  'unix INTEGER, mediaID INTEGER, title TEXT, duration INTEGER, plexMediaID TEXT, customSectionName Text)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS '
                  'shows(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                  'unix INTEGER, mediaID INTEGER, title TEXT, duration INTEGER, '
                  'lastEpisodeTitle TEXT, fullImageURL TEXT, plexMediaID TEXT, customSectionName Text)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS '
                  'episodes(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                  'unix INTEGER, mediaID INTEGER, title TEXT, duration INTEGER, '
                  'episodeNumber INTEGER, seasonNumber INTEGER, showTitle TEXT, plexMediaID TEXT, customSectionName Text)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS '
                  'commercials(id INTEGER PRIMARY KEY AUTOINCREMENT, unix INTEGER, '
                  'mediaID INTEGER, title TEXT, duration INTEGER, plexMediaID TEXT, customSectionName Text)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS '
                  'schedule(id INTEGER PRIMARY KEY AUTOINCREMENT, unix INTEGER, '
                  'mediaID INTEGER, title TEXT, duration INTEGER, startTime TEXT, '
                  'endTime TEXT, dayOfWeek TEXT, startTimeUnix INTEGER, section TEXT, '
                  'strictTime TEXT, timeShift TEXT, overlapMax TEXT, xtra TEXT)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS '
                  'daily_schedule(id INTEGER PRIMARY KEY AUTOINCREMENT, unix INTEGER, '
                  'mediaID INTEGER, title TEXT, episodeNumber INTEGER, seasonNumber INTEGER, '
                  'showTitle TEXT, duration INTEGER, startTime TEXT, endTime TEXT, '
                  'dayOfWeek TEXT, sectionType TEXT, plexMediaID TEXT, customSectionName TEXT)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS '
                  'app_settings(id INTEGER PRIMARY KEY AUTOINCREMENT, version TEXT)')
        #index
        self.cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_episode_title ON episodes (title);')
        self.cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_movie_title ON movies (title);')
        self.cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_shows_title ON shows (title);')
        self.cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_video_title ON videos (title);')
        self.cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_music_title ON music (title);')
        self.cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_commercial_title ON commercials (title);')
        self.cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_settings_version ON app_settings (version);')
        """Setting Basic Settings
        """
        try:
            self.cursor.execute("INSERT OR REPLACE INTO app_settings "
                      "(version) VALUES (?)", 
                      ("0.1",))
            self.conn.commit()
        # Catch the exception
        except Exception as e:
            # Roll back any change if something goes wrong
            self.conn.rollback()
            raise e

    def drop_db(self):

        pass

    def drop_schedule(self):

        pass

    def drop_daily_schedule_table(self):

        sql = "DROP TABLE IF EXISTS daily_schedule"
        self.cursor.execute(sql)
        self.conn.commit()

    def create_daily_schedule_table(self):

        self.cursor.execute('CREATE TABLE IF NOT EXISTS '
                  'daily_schedule(id INTEGER PRIMARY KEY AUTOINCREMENT, unix INTEGER, '
                  'mediaID INTEGER, title TEXT, episodeNumber INTEGER, seasonNumber INTEGER, '
                  'showTitle TEXT, duration INTEGER, startTime TEXT, endTime TEXT, '
                  'dayOfWeek TEXT, sectionType TEXT, plexMediaID TEXT, customSectionName TEXT)')
        self.conn.commit()

    def remove_all_scheduled_items(self):

        sql = "DELETE FROM schedule WHERE id > -1"
        self.cursor.execute(sql)
        self.conn.commit()

    def remove_all_daily_scheduled_items(self):

        sql = "DELETE FROM daily_schedule"
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def clear_shows_table(self):

        sql = "DELETE FROM shows"
        self.cursor.execute(sql)
        self.conn.commit()

    """Database functions.
        Setters, etc.
    """
    def add_movies_to_db(
        self, 
        mediaID, 
        title, 
        duration, 
        plexMediaID, 
        customSectionName):

        unix = int(time.time())
        try:
            self.cursor.execute("REPLACE INTO movies "
                      "(unix, mediaID, title, duration, plexMediaID, customSectionName) VALUES (?, ?, ?, ?, ?, ?)", 
                      (unix, mediaID, title, duration, plexMediaID, customSectionName))
            self.conn.commit()
        # Catch the exception
        except Exception as e:
            # Roll back any change if something goes wrong
            self.conn.rollback()
            raise e

    def add_videos_to_db(
        self, 
        mediaID, 
        title, 
        duration, 
        plexMediaID, 
        customSectionName):

        unix = int(time.time())
        try:
            self.cursor.execute("REPLACE INTO videos "
                      "(unix, mediaID, title, duration, plexMediaID, customSectionName) VALUES (?, ?, ?, ?, ?, ?)", 
                      (unix, mediaID, title, duration, plexMediaID, customSectionName))

            self.conn.commit()
        # Catch the exception
        except Exception as e:
            # Roll back any change if something goes wrong
            self.conn.rollback()
            raise e

    def add_shows_to_db(
        self, 
        mediaID, 
        title, 
        duration, 
        lastEpisodeTitle, 
        fullImageURL, 
        plexMediaID, 
        customSectionName):

        unix = int(time.time())
        try:
            self.cursor.execute("INSERT OR IGNORE INTO shows "
                      "(unix, mediaID, title, duration, lastEpisodeTitle, fullImageURL, plexMediaID, customSectionName) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                      (unix, mediaID, title, duration, lastEpisodeTitle, fullImageURL, plexMediaID, customSectionName))
            self.conn.commit()
        # Catch the exception
        except Exception as e:
            # Roll back any change if something goes wrong
            self.conn.rollback()
            raise e

    def add_episodes_to_db(
        self, 
        mediaID, 
        title, 
        duration, 
        episodeNumber, 
        seasonNumber, 
        showTitle, 
        plexMediaID, 
        customSectionName):

        unix = int(time.time())
        try:
            self.cursor.execute("REPLACE INTO episodes "
                "(unix, mediaID, title, duration, episodeNumber, seasonNumber, showTitle, plexMediaID, customSectionName) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                (unix, mediaID, title, duration, episodeNumber, seasonNumber, showTitle, plexMediaID, customSectionName)) 
            self.conn.commit()
        # Catch the exception
        except Exception as e:
            # Roll back any change if something goes wrong
            self.conn.rollback()
            raise e

    def add_commercials_to_db(
        self, 
        mediaID, 
        title, 
        duration, 
        plexMediaID, 
        customSectionName):

        unix = int(time.time())
        try:
            self.cursor.execute("REPLACE INTO commercials "
                      "(unix, mediaID, title, duration, plexMediaID, customSectionName) VALUES (?, ?, ?, ?, ?, ?)", 
                      (unix, mediaID, title, duration, plexMediaID, customSectionName))
            self.conn.commit()
        # Catch the exception
        except Exception as e:
            print plexMediaID
            # Roll back any change if something goes wrong
            self.conn.rollback()
            raise e

    def add_schedule_to_db(self, 
                           mediaID, 
                           title, 
                           duration, 
                           startTime, 
                           endTime, 
                           dayOfWeek, 
                           startTimeUnix, 
                           section, 
                           strictTime, 
                           timeShift, 
                           overlapMax,
                           xtra):
        unix = int(time.time())
        try:
            self.cursor.execute("REPLACE INTO  schedule "
                "(unix, mediaID, title, duration, startTime, endTime, dayOfWeek, startTimeUnix, section, strictTime, timeShift, overlapMax, xtra) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                (unix, mediaID, title, duration, startTime, endTime, dayOfWeek, startTimeUnix, section, strictTime, timeShift, overlapMax, xtra))
            self.conn.commit()
        # Catch the exception
        except Exception as e:
            # Roll back any change if something goes wrong
            self.conn.rollback()
            raise e

    def add_daily_schedule_to_db(
            self,
            mediaID, 
            title, 
            episodeNumber, 
            seasonNumber, 
            showTitle, 
            duration, 
            startTime, 
            endTime, 
            dayOfWeek, 
            sectionType,
            plexMediaID,
            customSectionName
            ):

        print "sectionType", sectionType
        print "customSectionName", customSectionName
        unix = int(time.time())
        try:
            self.cursor.execute("INSERT OR REPLACE INTO daily_schedule "
                      "(unix, mediaID, title, episodeNumber, seasonNumber, "
                      "showTitle, duration, startTime, endTime, dayOfWeek, sectionType, plexMediaID, customSectionName) "
                      "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                      (
                        unix, 
                        mediaID, 
                        title, 
                        episodeNumber, 
                        seasonNumber, 
                        showTitle, 
                        duration, 
                        startTime, 
                        endTime, 
                        dayOfWeek, 
                        sectionType,
                        plexMediaID,
                        customSectionName
                        ))
            self.conn.commit()
        # Catch the exception
        except Exception as e:
            # Roll back any change if something goes wrong
            self.conn.rollback()
            raise e

    def add_media_to_daily_schedule(self, media):

        try:
            print str("#### Adding media to db: {} {}".format(media.title, media.start_time)).encode('UTF-8')
        except:
            print "----- Not outputting media info due to ascii code issues."

        print "media.custom_section_name", media.custom_section_name
        self.add_daily_schedule_to_db(
                0,
                media.title,
                media.episode_number if media.__class__.__name__ == "Episode" else 0,
                media.season_number if media.__class__.__name__ == "Episode" else 0,
                media.show_series_title if media.__class__.__name__ == "Episode" else '',
                media.duration,
                media.start_time,
                media.end_time,
                media.day_of_week,
                media.section_type,
                media.plex_media_id,
                media.custom_section_name
            )

    def import_shows_table_by_row(
            self, 
            mediaID, 
            title, 
            duration, 
            lastEpisodeTitle, 
            fullImageURL, 
            plexMediaID):

        unix = int(time.time())
        try:
            self.cursor.execute('UPDATE shows SET lastEpisodeTitle = ? WHERE title = ?', (lastEpisodeTitle, title))
            self.conn.commit()
        # Catch the exception
        except Exception as e:
            # Roll back any change if something goes wrong
            self.conn.rollback()
            raise e

    def import_daily_schedule_table_by_row(
            self, 
            mediaID, 
            title, 
            episodeNumber, 
            seasonNumber, 
            showTitle, 
            duration,
            startTime,
            endTime,
            dayOfWeek,
            sectionType,
            plexMediaID,
            customSectionName):

        unix = int(time.time())
        try:
            self.cursor.execute("REPLACE INTO daily_schedule "
                      '''(unix, 
                          mediaID, 
                          title, 
                          episodeNumber, 
                          seasonNumber, 
                          showTitle, 
                          duration,
                          startTime,
                          endTime,
                          dayOfWeek,
                          sectionType,
                          plexMediaID,
                          customSectionName
                         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                      (unix, 
                       mediaID, 
                       title, 
                       episodeNumber, 
                       seasonNumber, 
                       showTitle, 
                       duration,
                       startTime,
                       endTime,
                       dayOfWeek,
                       sectionType,
                       plexMediaID,
                       customSectionName))
            self.conn.commit()
        # Catch the exception
        except Exception as e:
            # Roll back any change if something goes wrong
            self.conn.rollback()
            raise e

    """Database functions.
        Updaters, etc.
    """
    def update_shows_table_with_last_episode(self, showTitle, lastEpisodeTitle):

        sql1 = "UPDATE shows SET lastEpisodeTitle = ? WHERE title LIKE ? COLLATE NOCASE"
        self.cursor.execute(sql1, (lastEpisodeTitle, showTitle, ))
        self.conn.commit()

    def update_movies_table_with_last_played_date(self, movieTitle):

        now = datetime.datetime.now()
        lastPlayedDate = now.strftime('%Y-%m-%d')
        sql = "UPDATE movies SET lastPlayedDate = ? WHERE title LIKE ? COLLATE NOCASE"
        self.cursor.execute(sql, (lastPlayedDate, movieTitle, ))
        self.conn.commit()

    """Database functions.
        Getters, etc.
    """
    def get_shows_table(self):

        sql = "SELECT * FROM shows"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_media(self, title, mediaType):

        print "+++++ title:", title
        if(title is not None):
            media = mediaType
            sql = "SELECT * FROM "+media+" WHERE (title LIKE ?) COLLATE NOCASE"
            self.cursor.execute(sql, ("%"+title+"%", ))
            media_item = self.cursor.fetchone()
            return media_item
        else:
            pass

    def get_schedule(self):

        self.cursor.execute("SELECT * FROM schedule ORDER BY datetime(startTimeUnix) ASC")
        datalist = list(self.cursor.fetchall())
        return datalist

    def get_daily_schedule(self):

        print "##### Getting Daily Schedule from DB."
        self.cursor.execute("SELECT * FROM daily_schedule ORDER BY datetime(startTime) ASC")
        datalist = list(self.cursor.fetchall())
        print "+++++ Done."
        return datalist

    def get_movie(self, title):

        media = "movies"
        return self.get_media(title, media)

    def get_shows(self, title):

        media = "shows"
        return self.get_media(title, media)

    def get_music(self, title):

        media = "music"
        return self.get_media(title, media)

    def get_video(self, title):

        media = "videos"
        return self.get_media(title, media)

    def get_episodes(self, title):

        media = "episodes"
        return self.get_media(title, media)

    def get_commercials(self):

        self.cursor.execute("SELECT * FROM commercials ORDER BY duration ASC")
        datalist = list(self.cursor.fetchall())
        return datalist

    def get_movies(self):

        self.cursor.execute("SELECT * FROM movies ORDER BY date(lastPlayedDate) ASC")
        datalist = list(self.cursor.fetchall())
        return datalist

    def get_first_episode(self, tvshow):

        sql = ("SELECT id, unix, mediaID, title, duration, MIN(episodeNumber), MIN(seasonNumber), "
                "showTitle, plexMediaID, customSectionName FROM episodes WHERE ( showTitle LIKE ?) COLLATE NOCASE")
        self.cursor.execute(sql, (tvshow, ))
        first_episode = self.cursor.fetchone()
        return first_episode

    '''
    *
    * When incrementing episodes in a series I am advancing by "id" 
    *
    '''
    def get_episode_id(self, episodeTitle):

        sql = "SELECT id FROM episodes WHERE ( title LIKE ?) COLLATE NOCASE"
        self.cursor.execute(sql, (episodeTitle, ))
        episode_id = self.cursor.fetchone()
        return episode_id

    def get_random_episode(self):

        sql = "SELECT * FROM episodes WHERE id IN (SELECT id FROM episodes ORDER BY RANDOM() LIMIT 1)"
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def get_random_movie(self):

        sql = "SELECT * FROM movies WHERE id IN (SELECT id FROM movies ORDER BY RANDOM() LIMIT 1)"
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def get_next_episode(self, series):

        '''
        *
        * As a way of storing a "queue", I am storing the *next episode title in the "shows" table so I can 
        * determine what has been previously scheduled for each show
        *
        '''
        self.cursor.execute("SELECT lastEpisodeTitle FROM shows WHERE title LIKE ?  COLLATE NOCASE", (series, ))
        last_title_list = self.cursor.fetchone()
        '''
        *
        * If the last episode stored in the "shows" table is empty, then this is probably a first run...
        *
        '''
        if last_title_list and last_title_list[0] == '':

            '''
            *
            * Find the first episode of the series
            *
            '''
            first_episode = self.get_first_episode(series)
            first_episode_title = first_episode[3]
            '''
            *
            * Add this episdoe title to the "shows" table for the queue functionality to work
            *
            '''
            self.update_shows_table_with_last_episode(series, first_episode_title)
            return first_episode

        elif last_title_list:
            '''
            *
            * The last episode stored in the "shows" table was not empty... get the next episode in the series
            *
            '''
            """
            *
            * If this isn't a first run, then grabbing the next episode by incrementing id
            *
            """
            sql = ("SELECT * FROM episodes WHERE ( id > "+str(self.get_episode_id(last_title_list[0])[0])+
                   " AND showTitle LIKE ? ) ORDER BY seasonNumber LIMIT 1 COLLATE NOCASE")
            self.cursor.execute(sql, (series, ))
            '''
            *
            * Try and advance to the next episode in the series, if it returns None then that means it reached the end...
            *
            '''
            next_episode = self.cursor.fetchone()
            if next_episode != None:
                self.update_shows_table_with_last_episode(series, next_episode[3])
                return next_episode
            else:
                print("+++++ Not grabbing next episode restarting series, series must be over. Restarting from episode 1.")
                first_episode = self.get_first_episode(series)
                self.update_shows_table_with_last_episode(series, first_episode[3])
            return first_episode
                
    def get_commercial(self, title):

        media = "commercials"
        sql = "SELECT * FROM "+media+" WHERE (title LIKE ?) COLLATE NOCASE"
        self.cursor.execute(sql, (title, ))
        datalist = list(self.cursor.fetchone())
        if datalist > 0:
            print(datalist)
            return datalist
        else:
            return None