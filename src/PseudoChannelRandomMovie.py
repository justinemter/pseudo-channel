"""
PseudoChannelRandomMovie

In order to get a better randomization by avoiding movie repeats,
this class helps get a random movie based on its "lastPlayedDate".
A list of all the movies are passed into this class ordered by
"lastPlayedDate". The function then runs through the array to 
find the first movie that satisfies the delta of "lastPlayedDate"
and "TIME_GAP_DAYS". Then a new array with the rest of the movies
that satisfy the condition is created. From there a random movie
is picked and returned. If however, the function hits the end of the
array of movies and the condition is not satisfied (all movies have
been played more recently than the "TIME_GAP_DAYS"), a random movie 
is then returned.

For smaller movie libraries it'll be useful to calculate a reasonable
"TIME_GAP_DAYS".
"""
import datetime
import random
from random import shuffle

class PseudoChannelRandomMovie():

    MOVIES_DB = []
    TIME_GAP_DAYS = 182
    MOVIES_XTRA_LIST = []

    def __init__(self):

        pass

    """
    If not using "xtra" params
    """
    def get_random_movie(self, moviesDB):

        self.MOVIES_DB = moviesDB

        shuffle(self.MOVIES_DB)

        for movie in self.MOVIES_DB:

            if(movie[5] is not None): #lastPlayedDate is recorded

                print movie[5]

                now = datetime.datetime.now()
                lastPlayedDate = datetime.datetime.strptime(movie[5], '%Y-%m-%d')

                timeDelta = lastPlayedDate - now

                if(timeDelta.days >= self.TIME_GAP_DAYS): 

                    return movie[3]

                else:

                    break
            else:

                return movie[3] # No lastPlayedDate is recorded so lets use this movie

    """
    If using "xtra" args, expect a list from the Python PLEX API.
    Loop over list titles and lookup the title against the 
    MOVIES_DB to see the lastPlayedDate, etc.

    @Returns: Movie Title (String)
    """
    def get_random_movie_xtra(self, moviesDB, moviesXTRAList):

        self.MOVIES_DB = moviesDB
        self.MOVIES_XTRA_LIST = moviesXTRAList

        shuffle(self.MOVIES_DB)

        print("get_random_movie_xtra")

        for movieOne in self.MOVIES_XTRA_LIST:

            print("while i < len(self.MOVIES_XTRA_LIST):")

            movieTitle = movieOne.title

            print("movieTitle", movieTitle)

            for movie in self.MOVIES_DB:

                print("for movie in self.MOVIES_DB:")

                if movie[3] == movieTitle: #title match found

                    if(movie[5] is not None): #lastPlayedDate is recorded

                        print("I am here")

                        now = datetime.datetime.now()
                        lastPlayedDate = datetime.datetime.strptime(movie[5], '%Y-%m-%d')

                        timeDelta = lastPlayedDate - now

                        if(timeDelta.days >= self.TIME_GAP_DAYS): 

                            print("if(timeDelta.months >= self.TIME_GAP_DAYS):")

                            return movieTitle

                        else:

                            break

                    else:

                        return movieTitle # No lastPlayedDate recorded

                else:

                    pass

        return random.choice(self.MOVIES_XTRA_LIST).title # Everything has been played, choosing something.

        pass