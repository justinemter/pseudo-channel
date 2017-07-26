"""Commercial Functionality
"""
from random import shuffle
import random
import copy
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from src import Commercial

class PseudoChannelCommercial():

    MIN_DURATION_FOR_COMMERCIAL = 10 #seconds
    daily_schedule = []

    def __init__(self, commercials):

        self.commercials = commercials

    def get_commercials_to_inject(self):

        self.go()

        return None

    def get_random_commercial(self):

        random_commercial = random.choice(self.commercials)

        random_commercial_dur_seconds = (int(random_commercial[4])/1000)%60

        while random_commercial_dur_seconds < self.MIN_DURATION_FOR_COMMERCIAL:

             random_commercial = random.choice(self.commercials)

             random_commercial_dur_seconds = (int(random_commercial[4])/1000)%60

        return random_commercial

    def go(self):

        shuffled_commercial_list = copy.deepcopy(self.commercials)

        random.shuffle(self.commercials, random.random)

        #print shuffled_commercial_list

        prev_item = None

        for entry in self.daily_schedule:

            """First Episode"""
            if prev_item == None:

                prev_item = entry

            else:

                prev_item_end_time = datetime.datetime.strptime(prev_item[9], '%Y-%m-%d %H:%M:%S.%f')

                curr_item_start_time = datetime.datetime.strptime(entry[8], '%I:%M:%S %p')

                time_diff = (curr_item_start_time - prev_item_end_time)

                days, hours, minutes = time_diff.days, time_diff.seconds // 3600, time_diff.seconds // 60 % 60

                count = 0

                commercial_list = []

                commercial_dur_sum = 0

                while int(time_diff.total_seconds()) >= commercial_dur_sum and count < len(self.commercials):


                    random_commercial = self.get_random_commercial()

                    commercial_list.append(random_commercial)

                    commercial_dur_sum += int(random_commercial[4])

                print commercial_list

                prev_item = entry

    def timedelta_milliseconds(self, td):
        return td.days*86400000 + td.seconds*1000 + td.microseconds/1000

    def get_commercials_to_place_between_media(self, last_ep, now_ep):

        print last_ep.end_time, now_ep.start_time

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

        print "here", time_diff.seconds

        while curr_item_start_time > new_commercial_start_time and (count) < len(self.commercials):

            random_commercial = self.get_random_commercial()

            #new_commercial_seconds = (int(random_commercial[4])/1000)%60

            new_commercial_milli = int(random_commercial[4])

            if last_commercial != None:

                #print last_commercial[3]

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
            )

            last_commercial = new_commercial

            if new_commercial_end_time > curr_item_start_time:

                break

            commercial_list.append(new_commercial)

            #print "here!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

        return commercial_list