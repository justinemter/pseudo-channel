#!/usr/bin/env python

"""
*** Inherited by Commercial, Episode & Movie
"""
class Media(object):

    plex_server_url = ''
    plex_server_token = ''
    media_image = ''

    """A base class for media objects.

    Attributes:
        section_type: The type of library this is (i.e. "TV Shows")
        title: The title of the media item
        natural_start_time: The scheduled start time before any shifting happens.
        natural_end_time: The end time of the scheduled content.
        duration: The duration of the media item.
        day_of_week: When the content is scheduled to play
        is_strict_time: If strict time, then anchor to "natural_start_time"
    """

    def __init__(
            self, 
            section_type, 
            title, 
            natural_start_time, 
            natural_end_time, 
            duration, 
            day_of_week,
            is_strict_time,
            time_shift, 
            overlap_max
            ):

        self.section_type = section_type
        self.title = title
        self.natural_start_time = natural_start_time
        self.natural_end_time = natural_end_time
        self.duration = duration
        self.day_of_week = day_of_week
        self.is_strict_time = is_strict_time
        self.time_shift = time_shift
        self.overlap_max = overlap_max

        self.start_time = natural_start_time
        self.end_time = natural_end_time

