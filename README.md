# pseudo-channel - Plex Controller for Home-brewed TV Channel
This is a python based cli-app using the python-plex-api to control a plex-client and act like a real TV channel with show scheduling, commercial breaks, movie nights, etc.

Joined by the author of [Fake TV](https://medium.com/@Fake.TV), this project aims at tackling one issue: creating a fake tv channel experience with your own media library (movies, tv shows, commercials, etc.). The idea is super simple... when you turn on your TV, rather than hopping straight to Netflix, you can choose to watch your own channel of curated media like a real channel, with randomized movie time blocks, weekend morning cartoons, 90's commercials to fill up gaps and more. We aim to add a ton of neat features but the basic idea is to have something that feels like a real TV channel. That being said it isn't supposed to "pause" nor are you supposed to intervene too much. Just like a real channel you are presented with a channel that you define once and let it go as it advances in series episodes, playing random movies where specified (defined by various parameters like genre, "Kevin Bacon", etc.). Think: weekday movie nights @ 8:00 PM. Or perhpas you want to further specify your weekly Wednesday evening movie be a movie in your Plex library that stars "Will Smith". Currently the latter feature among many others are being developed but this is the goal. PseudoChannel is built to interface with the Plex media server. So if you want to have your very own PseudoChannel, you first need to set up your home server using [Plex](https://www.plex.tv/). After that you can come back here to learn how to setup everything else. Please note that we just started this project so everything is evolving rapidly. Check back often. We aim to have a decent working "alpha" version within a week or so. This readme / the how-to guide will all be very user friendly. Although this app runs using Python and the command line, we aim to make all of it as easy as possible to understand for those who are intimidated by this sort of technology. 

![Generated HTML schedule](http://i.imgur.com/uTGRYIp.png)

## Features So Far:

- [x] Generate Daily Schedule of TV Show episodes based on user defined TV Shows.
- [x] Add a controller to query the local generated pseudo_tv.db to see when to trigger the next media.
- [x] Add episode duration checking & adjust daily generated schedule based on these results...
- [x] Generate daily html schedule (saved in ./schedules directory). Can be served via webserver.
- [ ] Add Google Calendar integration to easily schedule your PseudoChannel.
- [ ] Add "commercial injection" & user defined "defaults" to fill up gaps between content. 
- [ ] Bug fixes.
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

Features are being added to the xml but as of now there are a few. Within the XML `<time>` entry you are able to pass in various attributes to set certain values. As of now, aside from "title" and "type" which are mandatory, you can take advantage of "time-shift". This parameter accepts values in minutes and can be no lower than "1". If the attribute, "strict-time" is set to "false", then this `<time>` entry will be shifted to a new time based on the previous time with a smaller gap calculated according to the value in "time-shift". Basically, if you do not want any gaps in your schedule you would leave "strict-time" false and set "time-shift" to "1" for all `<time>` entries. However, this will create a schedule with weird start times like, "1:57 PM". Taking advantage of the "time-shift" perameter will correct this. If you set it to a value of "5", all media is shifted and hooked on to a "pretty" time that is a multiple of 5. So if used, rather then having a "Seinfeld" episode being set to "1:57 PM" it may be recalculated and scheduled for "2:00 PM". However, if you would like to make sure that "The Simpsons" will always start every weekday at "6:00 PM" then you can simply set that `<time>` entry to `srtict-time="true"`. This will ensure that despite other non-strict times shifting around, "The Simpsons" will air every weekday at the desired "6:00 PM" as scheduled. currently this functionality will result in unintended empty gaps in the schedule. Soon there will be an option for using user specified "default" media to be injected into the gaps or "commercial" injection - or both.

To run the app in a 'poor-mans-daemon-mode' using [screen](https://www.gnu.org/software/screen/manual/screen.html), run this:

```bash
% screen -d -m bash -c 'python PseudoChannel.py -r; exec sh'
```
[cli flag info](https://explainshell.com/explain?cmd=screen+-d+-m)

...the previous command will keep the clock / app running in the background via the screen utility - kinda like a daemon process. 

Stay tuned for a polished version / bug fixes / features and commercial injection. 




