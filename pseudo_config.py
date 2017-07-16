#!/usr/bin/python

baseurl = 'http://media.home:32400'
token = 'the-token' # find your token using this guide: https://support.plex.tv/hc/en-us/articles/204059436-Finding-an-authentication-token-X-Plex-Token

'''
*
* The increment value between scheduled shows. Let's say you want to reposition all shows to have a clean start time divisable by 15 (i.e. 12:30 or 12:45). Use the value "-1" to disregard.
* 
*
'''
timeGap = 15


timeBetweenShows = -1

'''
*
* If there is an overlap, then the overlapGap var in config will determine the next increment. If it is set to "15", then the show will will bump up to the next 15 minute interval past the hour. If it is set to 30, then it will find the next 30 minute interval past the hour to place the episode. Useful for keeping clean schedules.
*
'''
overlapGap = 15
