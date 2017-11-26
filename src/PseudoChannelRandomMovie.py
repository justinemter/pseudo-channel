"""
PseudoChannelRandomMovie

In order to get a better randomization by avoiding movie repeates,
this class helps get a random movie based on its "lastPlayedDate".
The function keeps grabbing random movies, checking the "lastPlayedDate", 
comparing it with todays date, and checking the delta against 
the user specified "TIME_GAP_MONTHS" (which defaults at 6 [months]).
It stops and returns the first random movie that satisfies the condition.
However, if it runs through every movie and no movie satifies the condition, 
it then simply returns any movie.

For smaller movie libraries it'll be useful to calculate a reasonable
"TIME_GAP_MONTHS".
"""
class PseudoChannelRandomMovie():

    MOVIES = []
    TIME_GAP_MONTHS = 6

    def __init__(self):

        pass

    def get_random_movie(self, movies):

    	self.MOVIES = movies

    	pass