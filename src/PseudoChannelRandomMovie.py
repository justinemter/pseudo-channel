"""
PseudoChannelRandomMovie

In order to get a better randomization by avoiding movie repeates,
this class helps get a random movie based on its "lastPlayedDate".
A list of all the movies are passed into this class ordered by
"lastPlayedDate". The function then runs through the array to 
find the first movie that satisfies the delta of "lastPlayedDate"
and "TIME_GAP_MONTHS". Then a new array with the rest of the movies
that satisfy the condition is created. From there a random movie
is picked and returned. If however, the function hits the end of the
array of movies and the condition is not satisfied (all movies have
been played more recently than the "TIME_GAP_MONTHS"), a random movie 
is then returned.

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