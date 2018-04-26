# PseudoChannel.py - Your Home-Brewed TV Channels

*Update 12/03/2017 - Enabled Support for Custom Library Names - If already running PseudoChannel.py, the local DB must be deleted & then rebuilt running the "-u" option. The TV Shows queue can be preserved by using the "-e" & "-i" options, all together: `python PseudoChannel.py -e -u -i`*

Joined by the author of [Fake TV](https://medium.com/@Fake.TV), this project aims at tackling one issue: creating a fake tv channel experience with your own media library (movies, tv shows, commercials, etc.). The idea is super simple... when you turn on your TV, rather than hopping straight to Netflix, you can choose to watch your own channel of curated media like a real channel, with randomized movie time blocks, weekend morning cartoons, 90's commercials to fill up gaps and more. We aim to add a ton of neat features but the basic idea is to have something that feels like a real TV channel. That being said it isn't supposed to "pause" nor are you supposed to intervene too much. Just like a real channel you are presented with a channel that you define once and let it go as it advances in series episodes, playing random movies where specified (defined by various parameters like genre, "Kevin Bacon", etc.). Think: weekday movie nights @ 8:00 PM. Or perhaps you want to further specify your weekly Wednesday evening movie be a movie in your Plex library that stars "Will Smith". PseudoChannel is built to interface with the Plex media server. So if you want to have your very own PseudoChannel, you first need to set up your home server using [Plex](https://www.plex.tv/). After that you can come back here to learn how to setup everything else. Although this app runs using Python and the command line, we aim to make all of it as easy as possible to understand for those who are intimidated by this sort of technology. If you have a question, are troubleshooting or have feature ideas, just leave an 'issue' here in this repository.


![Generated HTML schedule](http://i.imgur.com/uTGRYIp.png)

## How to Use:

- The instructions below are all for configuring the **"controller"** device (i.e. a laptop or raspberry pi running linux). This is the device this app runs on to control the Plex client. The **"client"** device should be a Raspberry Pi running Rasplex hooked up to your TV via HDMI - although I'm sure other devices work great too (never tried). 

1. PseudoChannel uses Python 2.7. The recommended method of setting up most python environments is to use [virtualenv](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/). This keeps all your pip packages / python versions separated on a per project basis. I find this method extremely useful but also somewhat unintuitive, especially at first. Whether you choose to use "virtualenv" to isolate your project environment or not, you can install all the PseudoChannel.py dependencies by running the following command after downloading this repository:

```bash
% pip install -r requirements.txt
```
*You need to run the previous command using `sudo` if not in a virtualenv.*

2. In order to tell PseudoChannel.py how to connect to your Plex server, create an empty file named, `plex_token.py` just outside of the project directory. Within that file add your plex server url / [plex token](https://support.plex.tv/hc/en-us/articles/204059436-Finding-an-authentication-token-X-Plex-Token) like so:

```bash
token = '<your token>'
baseurl = 'http://192.168.1.28:32400'
```
*This file is important as it tells PseudoChannel.py how/where to connect to your Plex server. It should sit just outside of this /pseudo-channel/ directory.*

3. Edit the `pseudo_config.py` / `the pseudo_schedule.xml` to your liking. You can specify your plex media library names within the `pseudo_config.py` file... If you do not intend on using commercials just set the `useCommercialInjection` flag to `False`. There are a few other experimental options like using Google Calendar rather than an XML. It is an arduous process to initially set up and I've found the XML method to be the easiest method for organizing your schedule - so stick with that for now. Finally, setup your schedule in the xml file. There are some detailed instructions commented at the top of that file.

4. Run the `PseudoChannel.py` file with the following flags:

```bash
% python PseudoChannel.py -u -xml -g -m -r
```
*You can also run `-h` to view all the options. Use `-c` to find the name(s) of your Plex client(s) to add to the config.*

- The `-u` flag will prepare & update (& create if not exists) the local `pseudo-channel.db`, you only need to run this once in the beginning or later when you have added new media to your Plex libraries. 
- The `-xml` flag will update the newly created local db with your schedule from the xml file - you  should run this everytime you make changes to the xml. 
- The `-g` file will generate the daily schedule (for today) based on the xml. This is useful for the first run or testing (or manually advancing the daily queue forward). Running this flag say, 15 times will advance the play queue forward 15 days. It is automatically run every night at midnight to generate the daily schedule.
- The `-m` flag makes both the .html/.xml files and starts a simple html web server in the `./schedules` directory.
- Finally, the `-r` flag will run the app, checking the time / triggering the playstate of any media that is scheduled. It will also update the daily schedule when the clock hits 11.59 (or whatever time you've configured in the config file). If you see errors, check your entries in the xml first. Check your times, check for overlaps & make sure your are using ascii characters to replace foreign characters like umlauts and '&' characters, etc. Make sure all of your movie names / TV Series names are correct. 

You can run `% python PseudoChannel.py` with the following options. The order is important depending on what you are doing (i.e. `% python PseudoChannel.py -u -xml -g -m -r`):

| Flag                    | Description   | 
| ------------------------|--------------| 
| -u, --update            | Manually update (or create if not exists) the local db when new media is added to your Plex server. |
| -xml, --xml             | After making any edits your .xml schedule. Run this to populate the local db. |  
| -g, --generate_schedule | Manually generate the daily schedule. This is useful for testing / first run. |
| -r, --run               | Run PsuedoChannel.py. |
| -c, --show_clients      | Show connected Plex clients. |
| -s, --show_schedule     | Output the generated "Daily Schedule" to your terminal. |
| -m, --make_html         | Manually generate both html / xml docs based on the "Daily Schedule". |
| -e, --export            | Export the current queue of your "TV Shows" episodes. Useful when redoing your local DB. |
| -i, --import            | Import the previously exported queue of your "TV Shows" episodes. |
| -eds, --export_daily_schedule | Export the daily schedule. |
| -ids, --import_daily_schedule | Import the daily schedule. |

## `startstop.sh` - Alternative Way of Running the Application:

Within the app directory, there is a file named, `startstop.sh`. This bash script is a convenient way to start/stop the application. When run, it will start the application and save the "pid" of the process to the application directory. When run again, it will check to see if that process is running, if so it will stop it. All you have to do is run:

```bash
% ./startstop.sh
```

When you start the application with this bash script, you can close your terminal as it will keep running in the background. Later, when you come back and want to stop it... you can just execute that file once more and it will stop the running process. Please note: It's good to test the application and your configurations using the manual process above before running this bash script. Although there is a `pseudo-channel.log` that is created within the application directory, it is easier to just view the output in your terminal window - something that won't happen when using the bash script. 

## Setting Up the Generate-Daily-Schedule Cron Task

Every day (usually at midnight) PseudoChannel needs to generate a new schedule. It will not do this automatically if the app is already running. This task triggers the `-g` flag which generates the new schedule for the following day. This method, as described below, only works when using the `startstop.sh` script. How it works is, it looks for a `running.pid` file in the channel directory which the `startstop.sh` script creates when the channel is run. If it exists, the script will stop the channel, run the `-g` flag, then restart the channel. If it doesn't exist, then the script will just run the `-g` flag without doing anything else. In both cases, the channel generates a new schedule for the upcoming day. Feel free to change the update times, just be sure to choose a time past midnight - so that the app knows if it is a weekend, or what weekday to generate a schedule for. If you usually watch PseudoChannel until 2:00am, set the update time to 3:00am in the crontab task. 

Setup a cron task:
```bash
crontab -e
```

...then setup your new task to trigger the included `generate_daily_sched.sh` file:
```bash
0 0 * * * cd /home/pi/channel_01 && ./generate_daily_sched.sh > /dev/null 2>&1
```

This will trigger the `generate_daily_sched.sh` bash script every day at midnight. Be sure to alter the paths in the above crontab task to match your PseudoChannel's paths. 



## Futher Info:

Features are being added to the xml but as of now there are a few. Within the XML `<time>` entry you are able to pass in various attributes to set certain values. As of now, aside from "title" and "type" which are mandatory, you can take advantage of "time-shift". This parameter accepts values in minutes and can be no lower than "1". If the attribute, "strict-time" is set to "false", then this `<time>` entry will be shifted to a new time based on the previous time with a smaller gap calculated according to the value in "time-shift". Basically, if you do not want any gaps in your daily generated schedule you would leave "strict-time" false and set "time-shift" to "1" for all `<time>` entries. However, this will create a schedule with weird start times like, "1:57 PM". Taking advantage of the "time-shift" perameter will correct this. If you set it to a value of "5", all media is shifted and hooked on to a "pretty" time that is a multiple of 5. So if used, rather then having a "Seinfeld" episode being set to "1:57 PM" it may be recalculated and scheduled for "2:00 PM". However, if you would like to make sure that "The Simpsons" will always start every weekday at "6:00 PM" then you can simply set that `<time>` entry to `srtict-time="true"`. This will ensure that despite other non-strict times shifting around, "The Simpsons" will air every weekday at the desired "6:00 PM" as scheduled (be sure that you haven't accidentally made two time entries "strict-time" for the same day/time - this sort of thing will cause weird scheduling errors). When using "strict-time" or having the "time-shift" value > than 1 (minute), this will result in empty gaps in the schedule. Currently I have a flag in the config for "commercial injection" to fill up the gaps as much as possible with commercials from commercials in your Plex server "Commercials" library. If you do not want to use this feature or if you don't have any commercials in your Plex server, just open up that `pseudo_config.py` file and set `useCommercialInjection` to `False`. Please check the `pseudo-channel.xml` for more information.

## Specifying Random Movies in Your Schedule:

You are able to specify random movies in your XML schedule by adding a `<time>` entry as follows:

```xml
<time title="random" type="movie" strict-time="false" time-shift="5"  xtra='actor:mike myers genre:comedy contentRating:PG-13'>9:00 PM</time>
```
I have placed this time entry in the `<weekdays>` block of the XML. You can only specify `title="random"` for movie time blocks... however, you can further define parameters in the `xtra=` attribute. The `xtra` params are passed-in separated by a `:` as the delimiter as seen above. As I am using the Python Plex API to handle that logic, you can view their list of options: http://python-plexapi.readthedocs.io/en/latest/modules/library.html#plexapi.library.LibrarySection.search

Furthermore, if you'd like to specify multiple values in the `xtra` params, say to schedule saturday morning kid-friendly movies, you could do something like: `xtra="contentRating:G,PG"`. This works for other parameters, like `genre`: `xtra="genre:comedy,romance"`. Just beware that if the app cannot find a single movie in your library that matches your parameters, it will just give you a random movie dismissing all the params. 

## The Automatically Generated .HTML Daily Schedule / Server

To view the automatically generated "Daily Pseudo Schedule" index.html as seen in the image above, find it in the generated `./schedules/` directory within the project folder. The html file is generated both when the daily schedule is updated and whenever a media item from the schedule plays or ends (you can manually generate it with the `-m` flag). 

If you configured your `controllerServerPath` variable in the `pseudo_config.py` file, you can view your schedule by pointing your browser here:

```bash
http://192.168.1.28:8000
```
*Where `192.168.1.28` is the IP of your controller & `8000` is the port - both perameters are configured in the `pseudo_config.py` file.*

## Adding New TV/Movies/Commercials to Your Channel:

Whenever you add new content to your Plex library, you need to run: `python PseudoChannel.py -u`. This will tell the app to check the Plex library and update the local database with new media.

## Multi-Channel Support:

You can have multpile instances of this app, specify different schedules for each instance and control it via a USB remote. Let's say you choose to have 3 channels, an all day movie channel, a 'cartoon network' channel, and a 90's channel. You would simply create a directory named something like `/channels`. Then within your `/channels` dir you would have your `plex_token.py` file and your channels named something like: `/channel_1`, `channel_2` & `channel_3`. Note: the only important naming convention here is that `_01`, `_02`, etc. is contained at the end of each directory title. Each channel directory will contain the contents of this repository, set up just as if you had a single channel. So your directory structure would look like this:

```bash
-channels/
--plex_token.py
--channel_01/
---pseudo-channel.db
---PseudoChannel.py
---...etc.
--channel_02/
---pseudo-channel.db
---PseudoChannel.py
---...etc.
--channel_03/
---pseudo-channel.db
---PseudoChannel.py
---...etc.
```

In order to get this working with a usb remote hooked up to your Raspberry Pi, you need to configure the remotes channel buttons to trigger the corresponding bash scripts. I have placed a `channelup.sh` and a `channeldown.sh` within the projects `bash-scripts/` dir. You need to move these files to the `channels/` directory to make it work. When everything is setup properly and you have configured your remote, your channel up/channel down buttons should trigger the corresponding scripts triggering the channel to change. Lastly you need to configure a crontab so your controller automatically triggers each channel to generate a new daily schedule when the clock hits, `12:00 AM`. If you are running a single channel the the app knows to update when the clock strikes mid-night. However, if you are using this multi-channel method, the bash scripts will start / stop the corresponding channels depending on what channel you are watching. There is another bash script that you configure a crontab to trigger that will generate a new daily schedule for each channel that isn't currently running. 

*This is a work in progress.*

## Known Issues/Workarounds

By far, the most issues result from XML errors. It's important to make sure that all XML `<time>` entries are properly formatted and that you do not squeeze in too many `<time>` entries in your daily schedule. A good example of too many time entries is when you try and fill up a full 24 hours with daily content. Since PseudoChannel.py generates a new daily scedule every 24 hours, it will overwrite the previous 24 hours with the new content. So, if you were watching a movie that was scheduled to start at `11:00 PM`, the app will generate a new daily schedule when the clock hits `12:00 AM`. However, I added some logic that should allow any previous playing media to finish before beginning the next days schedule. It's best to try and avoid overfilling your schedule. 

### Problem Solving 

The best way to pinpoint errors and wonky-ness is to run the app in your console using: `python PseudoChannel.py -r`. Although there is a `.log` file that is generated in the working directory, the output from running the app manually is more verbose. Also, it is important to open up `psuedo_config.py` and change, `debug_mode` from `False` to `True`. This will not only show more verbose output when running PseudoChannel.py, but will also show all scheduled content (including commercials) in the generated daily schedule .html. 

#### Inspecting the Database. 

If you'd like to dig deeper I recommend using a database inspector utility like, [sqlitebrowser](http://sqlitebrowser.org/). The app generates a local sqlite db called, `psuedo-channel.db` located in the root of the project directory. There are a few tables to look at, the `daily_schedule` table and the `schedule` table. The former is the where all the daily generated time entries are placed and the latter is where the XML time entries are stored. 

#### Don't Be Afraid to Delete Your Local Database/Start Over:

If for some reason you want to delete your old DB but don't want to lose your TV queue you can do the following...

1) Export the TV queue by running `python PseudoChannel.py -e`. This exports the queue to a json file. 

2) Delete the pseudo-channel.db file. 

3) Re-generate the fresh database by running: `python PseudoChannel.py -u`

4) Import the old TV queue: `python PseudoChannel.py -i`.

*...this has been helpful mostly when debugging/developing, but it may be helpful for others too. Of course if you don't care about your TV queue you can skip steps, 1 & 4.*

## Contact Mark Or Me 

We set up [discord](https://discord.gg/7equn68) channel where you can ping Mark and I with any issues you may run into. You can find us there or file an "issue" here in this repo. 

Stay tuned for a polished version / bug fixes.  

## Special Thanks

Special thanks to Mark @ [Fake TV](https://medium.com/@Fake.TV). Without his creative ideas and love for TV, this "PseudoChannel" wouldn't be as cool as it is. I look forward to tinkering with this project and seeing others "unplugging" and creating their own home network. Mark has some excellent ideas in regard to making this thing much more usable as a "pseudo-cable" network - I think this will be in the next version as it is the 'icing on the cake' sort of feature. Anyway, enjoy! 
