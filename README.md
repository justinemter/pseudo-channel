# pseudo-channel - Plex Controller for Home-brewed TV Channel
This is a python based cli-app using the python-plex-api to control a plex-client and act like a real TV channel with show scheduling, commercial breaks, movie nights, etc.

This project is inspired by the [Fake TV](https://medium.com/@Fake.TV/installation-and-setup-of-faketv-e21340fbf1d4) blog post I came across on reddit a while ago. In his really cool project, the author uses a feature rich controller script called 'Python Plex Controller', located here: [https://github.com/MoeFwacky/Python-Plex-Controller](https://github.com/MoeFwacky/Python-Plex-Controller) to handle his "Fake TV" channel. I spent a few hours playing with this script and really had fun with it. It pretty much does everything you need and a lot more. There was however one thing missing that turned out to be pretty important to me: some kind of episode / movie duration calculation to shift a daily generated TV schedule so no media gets cutoff. Basically with that script, you can set a repeatable "weekday" schedule for a TV show... So every weekday the next episode in say, the 'Seinfeld' series will play at the specified time (i.e. "6:30 PM"). The problem I was having with this script is that if an episode happens to be longer than usual (say 1 hour versus the usual 30 minutes as scheduled), it won't adjust for that but will cut it off if you have something scheduled at say, "7:00 PM". It's very possible that this feature exists in that script and I missed it, but after playing with the awesome Plex API library over at: [https://github.com/pkkid/python-plexapi](https://github.com/pkkid/python-plexapi), I realized just how easy it is to control the playback of Plex media on my RasPlex client via my command line using Python and I decided to try and roll my own very simple script that does one thing really well: generate a daily TV schedule based on user defined TV Shows, time ranges, and random movies during specified movie time - injecting commercials where needed. 

![Generated HTML schedule](http://i.imgur.com/SQaUpYM.png)

## Features So Far:

- [x] Generate Daily Schedule of TV Show episodes based on user defined TV Shows.
- [x] Add a controller to query the local generated pseudo_tv.db to see when to trigger the next media.
- [x] Add episode duration checking & adjust daily generated schedule based on these results...
- [x] Generate daily html schedule (saved in ./schedules directory). Can be served via webserver.
- [ ] Add "commercial injection" to fill up gaps between content. 
- [ ] Bug fixes
- [ ] List of features from reddit. 

If interested in this project, check back very soon when the beta is up. It's close and a tiny bit more user friendly. :)

## How to Use (in the case someone stumbles across this and wants to try it before its polished):

- The instructions below are all for configuring the "controller" device (i.e. a laptop or raspberry pi running linux). The "client" device should be a Raspberry Pi running Rasplex hooked up to your TV via HDMI - although I'm sure other devices work great too (never tried). 

1. Download the [Python Plex API](https://github.com/pkkid/python-plexapi) & their dependencies. Also get [yattag](http://www.yattag.org/). All these dependencies can be installed via pip.

2. Download this repository & edit the `pseudo_config.py` / `the pseudo_schedule.xml` to your liking. Find your Plex token [here](https://support.plex.tv/hc/en-us/articles/204059436-Finding-an-authentication-token-X-Plex-Token)

3. Run the `PseudoChannel.py` file with the following flags:

```bash
% python PseudoChannel.py -u -xml -g -r
```

The `-u` flag will prepare & update (& create if not exists) the local `pseudo-channel.db`. The `-xml` flag will update the newly created local db with your schedule from the xml file. The `-g` file will generate the daily schedule (for today). Finally, the `-r` file will run a while loop checking the time / triggering the playstate of any media that is scheduled. It will also update the daily schedule when the clock hits 11.59. The xml schedule is a bit tempermental at the moment so if you see errors, check your entries there first. Make sure all of your movie names / TV Series names are correct. 

To run the app in a 'poor-mans-daemon-mode' using [screen](https://www.gnu.org/software/screen/manual/screen.html), run this:

```bash
% screen -d -m bash -c 'python PseudoChannel.py -r; exec sh'
```
[cli flag info](https://explainshell.com/explain?cmd=screen+-d+-m)

...the previous command will keep the clock / app running in the background via the screen utility - kinda like a daemon process. 

Stay tuned for a polished version / bug fixes / features and commercial injection. 




