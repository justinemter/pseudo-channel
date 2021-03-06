"""Commercial Functionality
"""
from random import shuffle
import random
import copy
from datetime import datetime
from datetime import timedelta
from src import Commercial

class PseudoChannelCommercial():

    MIN_DURATION_FOR_COMMERCIAL = 10 #seconds
    COMMERCIAL_PADDING_IN_SECONDS = 0
    daily_schedule = []

    def __init__(self, commercials, commercialPadding, useDirtyGapFix):

        self.commercials = commercials
        self.COMMERCIAL_PADDING_IN_SECONDS = commercialPadding
        self.USE_DIRTY_GAP_FIX = useDirtyGapFix

    def get_random_commercial(self):

        random_commercial = random.choice(self.commercials)
        random_commercial_dur_seconds = (int(random_commercial[4])/1000)%60
        while random_commercial_dur_seconds < self.MIN_DURATION_FOR_COMMERCIAL:
             random_commercial = random.choice(self.commercials)
             random_commercial_dur_seconds = (int(random_commercial[4])/1000)%60
        return random_commercial

    def timedelta_milliseconds(self, td):

        return td.days*86400000 + td.seconds*1000 + td.microseconds/1000

    def pad_the_commercial_dur(self, commercial):

        commercial_as_list = list(commercial)
        commercial_as_list[4] = int(commercial_as_list[4]) + (self.COMMERCIAL_PADDING_IN_SECONDS * 1000)
        commercial = tuple(commercial_as_list)
        return commercial

    def get_commercials_to_place_between_media(self, last_ep, now_ep):

        prev_item_end_time = datetime.strptime(last_ep.end_time.strftime('%Y-%m-%d %H:%M:%S.%f'), '%Y-%m-%d %H:%M:%S.%f')
        curr_item_start_time = datetime.strptime(now_ep.start_time, '%I:%M:%S %p')
        time_diff = (curr_item_start_time - prev_item_end_time)
        count = 0
        commercial_list = []
        commercial_dur_sum = 0
        time_diff_milli = self.timedelta_milliseconds(time_diff)
        last_commercial = None
        time_watch = prev_item_end_time 
        new_commercial_start_time = prev_item_end_time 
        while curr_item_start_time > new_commercial_start_time:
            random_commercial_without_pad = self.get_random_commercial()
            """
            Padding the duration of commercials as per user specified padding.
            """
            random_commercial = self.pad_the_commercial_dur(random_commercial_without_pad)
            new_commercial_milli = int(random_commercial[4])
            if last_commercial != None:
                new_commercial_start_time = last_commercial.end_time
                new_commercial_end_time = new_commercial_start_time + \
                                          timedelta(milliseconds=int(new_commercial_milli))
            else:
                new_commercial_start_time = prev_item_end_time
                new_commercial_end_time = new_commercial_start_time + \
                                          timedelta(milliseconds=int(new_commercial_milli))
            commercial_dur_sum += new_commercial_milli
            formatted_time_for_new_commercial = new_commercial_start_time.strftime('%I:%M:%S %p')
            new_commercial = Commercial(
                "Commercials",
                random_commercial[3],
                formatted_time_for_new_commercial, # natural_start_time
                new_commercial_end_time,
                random_commercial[4],
                "everyday", # day_of_week
                "true", # is_strict_time
                "1", # time_shift 
                "0", # overlap_max
                "", # plex_media_id
                random_commercial[6], # custom lib name
            )
            last_commercial = new_commercial
            if new_commercial_end_time > curr_item_start_time:

                # Fill up gap with commercials even if the last commercial gets cutoff
                if self.USE_DIRTY_GAP_FIX:
                    
                    commercial_list.append(new_commercial)
                # Find the best fitting final commercial and break
                else:

                    # If the gap is smaller than the shortest commercial, break.
                    gapToFill = curr_item_start_time - datetime.strptime(new_commercial.natural_start_time, '%I:%M:%S %p')
                    if int(self.commercials[0][4]) > self.timedelta_milliseconds(gapToFill):

                        break
                    else:

                        print "===== Finding correct FINAL commercial to add to List."

                        last_comm = None
                        for comm in self.commercials:

                            if int(comm[4]) >= self.timedelta_milliseconds(gapToFill) and last_comm != None:

                                random_final_comm = last_comm

                                formatted_time_for_final_commercial = datetime.strptime(new_commercial.natural_start_time, '%I:%M:%S %p').strftime('%I:%M:%S %p')

                                final_commercial_end_time = datetime.strptime(new_commercial.natural_start_time, '%I:%M:%S %p') + \
                                              timedelta(milliseconds=int(random_final_comm[4])) 

                                final_commercial = Commercial(
                                    "Commercials",
                                    random_final_comm[3],
                                    formatted_time_for_final_commercial, # natural_start_time
                                    final_commercial_end_time,
                                    random_final_comm[4],
                                    "everyday", # day_of_week
                                    "true", # is_strict_time
                                    "1", # time_shift 
                                    "0", # overlap_max
                                    "", # plex_media_id
                                    random_final_comm[6], # custom lib name
                                )
                                commercial_list.append(final_commercial)
                                break
                            last_comm = comm
                break
            commercial_list.append(new_commercial)
        return commercial_list