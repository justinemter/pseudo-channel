# pseudo-channel - Plex Controller for Home-brewed TV Channel
This is a python based cli-app using the python-plex-api to control a plex-client and act like a real TV channel with show scheduling, commercial breaks, movie nights, etc.

## This really isn't usable for anyone else yet, but I'm adding a Readme to inspire me to keep on with it. It's almost usable...

This project is inspired by the [Fake TV](https://medium.com/@Fake.TV/installation-and-setup-of-faketv-e21340fbf1d4) blog post I came across on reddit a while ago. In his really cool project, the author uses a feature rich controller script called 'Python Plex Controller', located here: [https://github.com/MoeFwacky/Python-Plex-Controller](https://github.com/MoeFwacky/Python-Plex-Controller) to handle his "Fake TV" channel. I spent a few hours playing with this script and really had fun with it. It pretty much does everything you need and a lot more. There was however one thing missing that turned out to be pretty important to me: some kind of episode / movie duration calculation to shift a daily generated TV schedule so no media gets cutoff. Basically with that script, you can set a repeatable "weekday" schedule for a TV show... So every weekday the next episode in say, the 'Seinfeld' series will play at the specified time (i.e. "6:30 PM"). The problem I was having with this script is that if an episode happens to be longer than usual (say 1 hour versus the usual 30 minutes as scheduled), it won't adjust for that but will cut it off if you have something scheduled at say, "7:00 PM". It's very possible that this feature exists in that script and I missed it, but after playing with the awesome Plex API library over at: [https://github.com/pkkid/python-plexapi](https://github.com/pkkid/python-plexapi), I realized just how easy it is to control the playback of Plex media on my RasPlex client via my command line using Python and I decided to try and roll my own very simple script that does one thing really well: generate a daily TV schedule based on user defined TV Shows, time ranges, and random movies during specified movie time - injecting commercials where needed. 

This script, like the one above uses crontab to both generate the daily schedule & check the current schedule every ~10 seconds to see when to trigger the next scheduled content (TV Show, Movie or Commercial).

## Features So Far:

- [x] Generate Daily Schedule of TV Show episodes based on user defined TV Shows.
- [ ] Add a controller to query the local generated pseudo_tv.db to see when to trigger the next media - for use with crontab.
- [ ] Add episode / movie /commercial duration checking & adjust daily generated schedule based on these results...
- [ ] Add movie / commercial support. 

## How to use:
1. Edit the pseudo_config.py file adding your server URL / Plex token (google how to find it).
2. Run the database loader to gather the necessary information about your Plex library and generate local DB (run as many times as needed. May take a while.):
```
python pseudo_updatedb.py
```
3. Edit the schedule.sh bash file to contain your daily schedule information. This needs to be run only once to tell the script what shows / movies it will be using when generating its daily schedule:
```
bash ./schedule.sh
```
4. Setup a crontab to run `pseudo_generate_daily_scheduledb.py` everyday at say, midnight. This will generate a schedule for the day based on media inputed by the about bash script.
```
crontab -e
0 0 * * * python /home/justin/this-repo-folder/pseudo_generate_daily_scheduledb.py
```
5. Create another crontab to fire at least every minute to see when to trigger to play scheduled media generated in the script above (TODO):
```
* * * * * python /home/justin/this-repo-folder/[TODO]
```
