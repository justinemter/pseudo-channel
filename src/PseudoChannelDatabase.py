import sqlite3
import datetime
import time

class PseudoChannelDatabase():

	def __init__(self, db):

		self.db = db

		self.conn = sqlite3.connect(self.db)

		self.cursor = self.conn.cursor()

	"""Database functions.

		Utilities, etc.
	"""

	def create_tables(self):

		self.cursor.execute('CREATE TABLE IF NOT EXISTS '
				  'movies(id INTEGER PRIMARY KEY AUTOINCREMENT, '
				  'unix INTEGER, mediaID INTEGER, title TEXT, duration INTEGER)')

		self.cursor.execute('CREATE TABLE IF NOT EXISTS '
				  'videos(id INTEGER PRIMARY KEY AUTOINCREMENT, '
				  'unix INTEGER, mediaID INTEGER, title TEXT, duration INTEGER)')

		self.cursor.execute('CREATE TABLE IF NOT EXISTS '
				  'music(id INTEGER PRIMARY KEY AUTOINCREMENT, '
				  'unix INTEGER, mediaID INTEGER, title TEXT, duration INTEGER)')

		self.cursor.execute('CREATE TABLE IF NOT EXISTS '
				  'shows(id INTEGER PRIMARY KEY AUTOINCREMENT, '
				  'unix INTEGER, mediaID INTEGER, title TEXT, duration INTEGER, '
				  'lastEpisodeTitle TEXT, fullImageURL TEXT)')

		self.cursor.execute('CREATE TABLE IF NOT EXISTS '
				  'episodes(id INTEGER PRIMARY KEY AUTOINCREMENT, '
				  'unix INTEGER, mediaID INTEGER, title TEXT, duration INTEGER, '
				  'episodeNumber INTEGER, seasonNumber INTEGER, showTitle TEXT)')

		self.cursor.execute('CREATE TABLE IF NOT EXISTS '
				  'commercials(id INTEGER PRIMARY KEY AUTOINCREMENT, unix INTEGER, '
				  'mediaID INTEGER, title TEXT, duration INTEGER)')

		self.cursor.execute('CREATE TABLE IF NOT EXISTS '
				  'schedule(id INTEGER PRIMARY KEY AUTOINCREMENT, unix INTEGER, '
				  'mediaID INTEGER, title TEXT, duration INTEGER, startTime INTEGER, '
				  'endTime INTEGER, dayOfWeek TEXT, startTimeUnix INTEGER), section TEXT)')

		self.cursor.execute('CREATE TABLE IF NOT EXISTS '
				  'daily_schedule(id INTEGER PRIMARY KEY AUTOINCREMENT, unix INTEGER, '
				  'mediaID INTEGER, title TEXT, episodeNumber INTEGER, seasonNumber INTEGER, '
				  'showTitle TEXT, duration INTEGER, startTime INTEGER, endTime INTEGER, dayOfWeek TEXT)')

		self.cursor.execute('CREATE TABLE IF NOT EXISTS '
				  'app_settings(id INTEGER PRIMARY KEY AUTOINCREMENT, version TEXT')

		#index
		self.cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_episode_title ON episodes (title);')

		self.cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_movie_title ON movies (title);')

		self.cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_movie_title ON videos (title);')

		self.cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_music_title ON music (title);')

		self.cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_commercial_title ON commercials (title);')

		"""Setting Basic Settings
		
		"""
		try:
			self.cursor.execute("INSERT OR REPLACE INTO app_settings "
					  "(version) VALUES (?)", 
					  ("0.1"))

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

	def remove_all_scheduled_items():

		sql = "DELETE FROM schedule WHERE id > -1"

		self.cursor.execute(sql)

		self.conn.commit()

		self.cursor.close()
		
		self.conn.close()

	"""Database functions.

		Setters, etc.
	"""

	def add_movies_to_db(self, mediaID, title, duration):
		unix = int(time.time())
		try:
			self.cursor.execute("INSERT OR REPLACE INTO movies "
					  "(unix, mediaID, title, duration) VALUES (?, ?, ?, ?)", 
					  (unix, mediaID, title, duration))

			self.conn.commit()
		# Catch the exception
		except Exception as e:
		    # Roll back any change if something goes wrong
		    self.conn.rollback()
		    raise e

	def add_videos_to_db(self, mediaID, title, duration):
		unix = int(time.time())
		try:
			self.cursor.execute("INSERT OR REPLACE INTO videos "
					  "(unix, mediaID, title, duration) VALUES (?, ?, ?, ?)", 
					  (unix, mediaID, title, duration))

			self.conn.commit()
		# Catch the exception
		except Exception as e:
		    # Roll back any change if something goes wrong
		    self.conn.rollback()
		    raise e

	def add_shows_to_db(self, mediaID, title, duration, lastEpisodeTitle, fullImageURL):
		unix = int(time.time())
		try:
			self.cursor.execute("INSERT OR REPLACE INTO shows "
					  "(unix, mediaID, title, duration, lastEpisodeTitle, fullImageURL) VALUES (?, ?, ?, ?, ?, ?)", 
					  (unix, mediaID, title, duration, lastEpisodeTitle, fullImageURL))
			self.conn.commit()
		# Catch the exception
		except Exception as e:
		    # Roll back any change if something goes wrong
		    self.conn.rollback()
		    raise e

	def add_episodes_to_db(self, mediaID, title, duration, episodeNumber, seasonNumber, showTitle):
		unix = int(time.time())
		try:
			self.cursor.execute("INSERT OR REPLACE INTO episodes "
				"(unix, mediaID, title, duration, episodeNumber, seasonNumber, showTitle) VALUES (?, ?, ?, ?, ?, ?, ?)", 
				(unix, mediaID, title, duration, episodeNumber, seasonNumber, showTitle)) 
			self.conn.commit()
		# Catch the exception
		except Exception as e:
		    # Roll back any change if something goes wrong
		    self.conn.rollback()
		    raise e

	def add_commercials_to_db(self, mediaID, title, duration):
		unix = int(time.time())
		try:
			self.cursor.execute("INSERT OR REPLACE INTO commercials "
					  "(unix, mediaID, title, duration) VALUES (?, ?, ?, ?)", 
					  (unix, mediaID, title, duration))
			self.conn.commit()
		# Catch the exception
		except Exception as e:
		    # Roll back any change if something goes wrong
		    self.conn.rollback()
		    raise e

	def add_schedule_to_db(self, mediaID, title, duration, startTime, endTime, dayOfWeek, section):
		unix = int(time.time())
		try:
			self.cursor.execute("INSERT INTO schedule "
				"(unix, mediaID, title, duration, startTime, endTime, dayOfWeek) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
				(unix, mediaID, title, duration, startTime, endTime, dayOfWeek, section))
			self.conn.commit()
		# Catch the exception
		except Exception as e:
		    # Roll back any change if something goes wrong
		    self.conn.rollback()
		    raise e

	def add_daily_schedule_to_db(self, mediaID, title, duration, startTime, endTime, dayOfWeek):
		unix = int(time.time())
		startTimeUnix = str(datetime.datetime.strptime(startTime, '%I:%M %p'))
		try:

			self.cursor.execute("INSERT OR REPLACE INTO schedule "
					  "(unix, mediaID, title, duration, startTime, endTime, dayOfWeek, startTimeUnix) "
					  "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
					  (unix, mediaID, title, duration, startTime, endTime, dayOfWeek, startTimeUnix))
			self.conn.commit()
			self.cursor.close()
			self.conn.close()
		# Catch the exception
		except Exception as e:
		    # Roll back any change if something goes wrong
			self.conn.rollback()
			self.cursor.close()
			self.conn.close()
			raise e


	"""Database functions.

		Getters, etc.
	"""
	def get_media(self, title, mediaType):

		media = mediaType

		sql = "SELECT * FROM "+media+" WHERE (title LIKE ?) COLLATE NOCASE"
		self.cursor.execute(sql, ("%"+title+"%", ))
		media_item = self.cursor.fetchone()

		return media_item

	def get_schedule(self):

		self.cursor.execute("SELECT * FROM schedule ORDER BY datetime(startTimeUnix) ASC")

		datalist = list(self.cursor.fetchall())

		return datalist

	def get_daily_schedule(self):

		return None

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

	def update_shows_table_with_last_episode(self, showTitle, lastEpisodeTitle):

		sql1 = "UPDATE shows SET lastEpisodeTitle = ? WHERE title = ?"

		self.cursor.execute(sql1, (lastEpisodeTitle, showTitle, ))

		self.conn.commit()

	def get_first_episode(self, tvshow):

		sql = ("SELECT id, unix, mediaID, title, duration, MIN(episodeNumber), MIN(seasonNumber), "
				"showTitle FROM episodes WHERE ( showTitle = ?) COLLATE NOCASE")

		self.cursor.execute(sql, (tvshow, ))

		datalist = list(self.cursor.fetchone())

		if datalist > 0:
			
			return datalist

		else:

			print("No entry found in DB to add to schedule.")

			return None

	'''
	*
	* When incrementing episodes in a series I am advancing by "id" 
	*
	'''
	def get_episode_id(self, episodeTitle):

		sql = "SELECT id FROM episodes WHERE ( title = ?) COLLATE NOCASE"

		self.cursor.execute(sql, (episodeTitle, ))

		datalist = list(self.cursor.fetchone())

		if datalist > 0:

			return datalist[0]

		else:

			print("No entry found in DB to add to schedule.")

			return None

	def get_next_episode(self, series):

		#print(series)
		'''
		*
		* As a way of storing a "queue", I am storing the *next episode title in the "shows" table so I can 
		* determine what has been previously scheduled for each show
		*
		'''
		self.cursor.execute("SELECT lastEpisodeTitle FROM shows WHERE title = ?", (series, ))

		last_title_list = list(self.cursor.fetchone())
		'''
		*
		* If the last episode stored in the "shows" table is empty, then this is probably a first run...
		*
		'''
		if last_title_list[0] == '':

			'''
			*
			* Find the first episode of the series
			*
			'''
			first_episode = self.get_first_episode(series)

			first_episode_title = first_episode[3]

			#print(first_episode_title)
			'''
			*
			* Add this episdoe title to the "shows" table for the queue functionality to work
			*
			'''
			self.update_shows_table_with_last_episode(series, first_episode_title)

			return first_episode

		else:
			'''
			*
			* The last episode stored in the "shows" table was not empty... get the next episode in the series
			*
			'''
			#print("First episode already set in shows, advancing episodes forward")

			#print(str(self.get_episode_id(last_title_list[0])))

			"""
			*
			* If this isn't a first run, then grabbing the next episode by incrementing id
			*
			"""
			sql = ("SELECT * FROM episodes WHERE ( id > "
				   +str(self.get_episode_id(last_title_list[0]))+
				   " AND showTitle LIKE ? ) ORDER BY seasonNumber LIMIT 1 COLLATE NOCASE")

			self.cursor.execute(sql, (series, ))
			'''
			*
			* Try and advance to the next episode in the series, if it returns None then that means it reached the end...
			*
			'''
			next_episode = self.cursor.fetchone()

			if next_episode != None:

				#print(next_episode[3])

				self.update_shows_table_with_last_episode(series, next_episode[3])

				return next_episode

			else:

				print("Not grabbing next episode restarting series, series must be over. Restarting from episode 1.")

				first_episode = self.get_first_episode(series)

				self.update_shows_table_with_last_episode(series, first_episode[3])

			return first_episode
				
	def get_commercials(self, title):

		media = "commercials"

		sql = "SELECT * FROM "+media+" WHERE (title LIKE ?) COLLATE NOCASE"
		self.cursor.execute(sql, (title, ))
		datalist = list(self.cursor.fetchone())
		if datalist > 0:
			print(datalist)

			return datalist

		else:

			return None

