#!/usr/bin/env python

from Media import Media

class Commercial(Media):

    """Inherits Media.

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
            overlap_max,
            plex_media_id,
            custom_section_name
            ):

        super(Commercial, self).__init__(
                section_type, 
                title, 
                natural_start_time, 
                natural_end_time, 
                duration, 
                day_of_week,
                is_strict_time,
                time_shift, 
                overlap_max,
                plex_media_id,
                custom_section_name
                )
