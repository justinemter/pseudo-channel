# pseudo-channel - Plex Controller for Home-brewed TV Channel
This is a python based cli-app using the python-plex-api to control a plex-client and act like a real TV channel with show scheduling, commercial breaks, movie nights, etc.

This project is inspired by the [Fake TV](https://medium.com/@Fake.TV/installation-and-setup-of-faketv-e21340fbf1d4) blog post I came across on reddit a while ago. In his really cool project, the author uses a feature rich controller script called 'Python Plex Controller', located here: [https://github.com/MoeFwacky/Python-Plex-Controller](https://github.com/MoeFwacky/Python-Plex-Controller) to handle his "Fake TV" channel. I spent a few hours playing with this script and really had fun with it. It pretty much does everything you need and a lot more. There was however one thing missing that turned out to be pretty important to me: some kind of episode / movie duration calculation to shift a daily generated TV schedule so no media gets cutoff. Basically with that script, you can set a repeatable "weekday" schedule for a TV show... So every weekday the next episode in say, the 'Seinfeld' series will play at the specified time (i.e. "6:30 PM"). The problem I was having with this script is that if an episode happens to be longer than usual (say 1 hour versus the usual 30 minutes as scheduled), it won't adjust for that but will cut it off if you have something scheduled at say, "7:00 PM". It's very possible that this feature exists in that script and I missed it, but after playing with the awesome Plex API library over at: [https://github.com/pkkid/python-plexapi](https://github.com/pkkid/python-plexapi), I realized just how easy it is to control the playback of Plex media on my RasPlex client via my command line using Python and I decided to try and roll my own very simple script that does one thing really well: generate a daily TV schedule based on user defined TV Shows, time ranges, and random movies during specified movie time - injecting commercials where needed. 

This script, like the one above uses crontab to both generate the daily schedule & check the current schedule every ~10 seconds to see when to trigger the next scheduled content (TV Show, Movie or Commercial).

![Generated HTML schedule](http://i.imgur.com/Lf5Dgyq.png)

## Features So Far:

- [x] Generate Daily Schedule of TV Show episodes based on user defined TV Shows.
- [x] Add a controller to query the local generated pseudo_tv.db to see when to trigger the next media - for use with crontab.
- [x] Add episode duration checking & adjust daily generated schedule based on these results...
- [x] Generate daily html schedule from schedule.
- [ ] Add movie / commercial support. 

## How to use:
For the controller, use a linux VM (Debian installed w/ minimal resources), or an old laptop w/ Ubuntu or a raspberry pi w/ Jessie...or something similar. You also may need to login to your Plex server and add the IP of the controller in Settings -> Server -> Advanced Settings -> Network, under "List of IP addresses and networks that are allowed without auth". Then download this repo to your users home folder and follow this guide:

1. Install [python plex api](https://github.com/pkkid/python-plexapi)
2. Move the "pseudo_config-sample.py" file to "pseudo_config.py" and edit it to add your server URL / Plex token ([how to find it](https://support.plex.tv/hc/en-us/articles/204059436-Finding-an-authentication-token-X-Plex-Token)). Also add the client host to the "plexClients" variable. The default for a RasPlex client is "RasPlex".
3. Run the database loader to gather the necessary information about your Plex library and generate local DB (run as many times as needed. May take a while.):
```
python pseudo_updatedb.py
```
4. Edit the schedule.sh bash file to define your daily schedule information (use my schedule.sh / boilerplate commands as a guide to how to input the schedule - it's pretty self-explanatory). The media title needs to match the media title in your Plex library (i.e. "the office" needs to be "the office (us)" if that's what it says in your library). This needs to be run only once to tell the script what shows / movies it will be using when generating its daily schedule:
```
bash ./schedule.sh
```
5. Setup a crontab to run `pseudo_generate_daily_scheduledb.py` everyday at say, midnight. This will generate a schedule for the day based on media inputed by the above bash script.
```
crontab -e

0 0 * * * cd /home/justin/pseudo-channel/ && /usr/bin/python /home/justin/pseudo-channel/pseudo_generate_daily_scheduledb.py
```
6. Create another crontab to fire at least every minute to see when to trigger to play scheduled media generated in the script above:
```
crontab -e

* * * * * cd /home/justin/pseudo-channel/ && /usr/bin/python /home/justin/pseudo-channel/pseudo_tv_controller.py
```
7. Pop some popcorn. 

Commercial / movie support & enabling / disabling various features pending. 
