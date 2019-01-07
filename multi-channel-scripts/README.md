![Multi-Channel Viewer](https://i.imgur.com/MRwjI8g.jpg)
*multi-channel-viewer.php*

If you'd like to set up multi-channel support using PseudoChannel.py, use these scripts to: 

1) Use a TV remote or Alexa or some device to trigger the channelup.sh/channeldown.sh (and other bash scripts) to cycle through the channels. 

2) Setup a "crontab" to run generate-channels-daily-schedule.sh script to automate each PseudoChannel.py to generate the daily
schedule:

`30 5 * * * cd /home/justin/channels && ./stop-all-channels.sh && ./generate-channels-daily-schedules.sh > /dev/null 2>&1`

*-Updating your folder locations as necessary.*

3) Use `updatechannels.sh` to update each channels' local db with newly added Plex library items. 

4) Use `update-channels-from-git.sh` to update all your channels with updates from this repo (uses the `develop` branch by default and preserves your DB, schedule XML and config).

5) Use, "manual.sh" to manually trigger a particular channel... i.e. `./manual.sh 9`, to switch to channel 9.

All of these scripts need to be placed in the "./channels/" dir. Your directory structure should look something like this:

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
--channelup.sh
--channeldown.sh
--manual.sh
--generate-channels-daily-schedule.sh
--generate-html-schedules.sh
--updatechannels.sh
--stop-all-channels.sh
--update-channels-from-git.sh
--multi-channel-api.php
--multi-channel-viewer.php
```

## Running a simple PHP server in `/channels` to view the `multi-channel-viewer.php` and to use the `multi-channel-api.php`
*As per the image above.*

1) Install PHP:

`sudo apt install php`

2) Start `screen` and run a simple PHP server in the `/channels` dir:

`screen`
`php -S 192.168.1.112:8080`

*-Change the IP:Port to your controller IP:Whatever port that's free/open*

3) Point your browser to your IP/Port/multi-channel-viewer.php:

`http://192.168.1.112:8080/multi-channel-viewer.php`

4) If using the `multi-channel-api.php` file to interact with the bash scripts, try navigating your browser to:

`http://192.168.1.112:8080/multi-channel-api.php/?command=KEY_CHANNELUP`

*-Open the multi-channel-api.php file to see the various commands. Edit as you see fit.*

5) Use cURL to trigger bash scripts (from any device running cURL):

`curl -I --request GET http://192.168.1.112:8080/?command=KEY_CHANNELUP`

Multi-channel Pseudo-Channel is a lot of fun. Stay tuned for better and easier functionality. 
