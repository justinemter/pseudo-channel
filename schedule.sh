#!/usr/bin/env bash

## 
##
## This is a bash script to run in order to update the "schedule" table in the 
## ..."pseudo-tv.db". It's best to only have to set this once and forget it. If you
## ...want to make edits / rerun this, I recommed deleting the data in the "schedule" table
## ...or just deleting the local "pseudo-tv.db" and starting the process again. So basically, 
## ...when you are ready to schedule your autonomous channel, start by ironing out your show times here.
## When you are satisfied with the general layout of your repeating schedule, then move forward with 
## ...the other steps. 
##
## Currently as of 07/17/2017 only the "-n" & "-t" flags work & only work for TV Shows. If you 
## are looking forward to being able to take advantage of "movies" / days of the week & commerical injection, 
## ...I should have that working very soon. Enjoy. 
##
##

python pseudo_channel.py -a "shows" -n "looney tunes" -t "6:00 AM" -d "weekdays"
python pseudo_channel.py -a "shows" -n "looney tunes" -t "6:30 AM" -d "weekdays"
python pseudo_channel.py -a "shows" -n "looney tunes" -t "7:00 AM" -d "weekdays"
python pseudo_channel.py -a "shows" -n "looney tunes" -t "7:30 AM" -d "weekdays"

python pseudo_channel.py -a "shows" -n "Garfield & Friends" -t "8:00 AM" -d "weekdays"
python pseudo_channel.py -a "shows" -n "Garfield & Friends" -t "8:30 AM" -d "weekdays"

python pseudo_channel.py -a "shows" -n "talespin" -t "9:00 AM" -d "weekdays"
python pseudo_channel.py -a "shows" -n "talespin" -t "9:30 AM" -d "weekdays"

python pseudo_channel.py -a "shows" -n "macgyver" -t "10:00 AM" -d "weekdays"
python pseudo_channel.py -a "shows" -n "macgyver" -t "11:00 AM" -d "weekdays"

python pseudo_channel.py -a "shows" -n "boy meets world" -t "12:00 PM" -d "weekdays"
python pseudo_channel.py -a "shows" -n "boy meets world" -t "12:30 PM" -d "weekdays"

python pseudo_channel.py -a "shows" -n "full house" -t "1:00 PM" -d "weekdays"
python pseudo_channel.py -a "shows" -n "full house" -t "1:30 PM" -d "weekdays"
python pseudo_channel.py -a "shows" -n "full house" -t "2:00 PM" -d "weekdays"

python pseudo_channel.py -a "shows" -n "the it crowd" -t "2:30 PM" -d "weekdays"
python pseudo_channel.py -a "shows" -n "the it crowd" -t "3:00 PM" -d "weekdays"

python pseudo_channel.py -a "shows" -n "strangers with candy" -t "3:30 PM" -d "weekdays"

python pseudo_channel.py -a "shows" -n "the office (us)" -t "4:00 PM" -d "weekdays"
python pseudo_channel.py -a "shows" -n "the office (us)" -t "4:30 PM" -d "weekdays"

python pseudo_channel.py -a "shows" -n "friends" -t "5:00 PM" -d "weekdays"
python pseudo_channel.py -a "shows" -n "friends" -t "5:30 PM" -d "weekdays"

python pseudo_channel.py -a "shows" -n "seinfeld" -t "6:00 PM" -d "weekdays"
python pseudo_channel.py -a "shows" -n "seinfeld" -t "6:30 PM" -d "weekdays"

python pseudo_channel.py -a "shows" -n "daria" -t "7:00 PM" -d "weekdays"
python pseudo_channel.py -a "shows" -n "daria" -t "7:30 PM" -d "weekdays"

python pseudo_channel.py -a "shows" -n "Futurama" -t "8:00 PM" -d "weekdays"
python pseudo_channel.py -a "shows" -n "Futurama" -t "8:30 PM" -d "weekdays"

python pseudo_channel.py -a "shows" -n "Saved by the Bell" -t "9:00 PM" -d "weekdays"
python pseudo_channel.py -a "shows" -n "Saved by the Bell" -t "9:30 PM" -d "weekdays"
