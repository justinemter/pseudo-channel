If you'd like to set up multi-channel support using PseudoChannel.py, use these scripts to: 

1) Use a remote or Alexa or some device to trigger the channelup.sh/channeldown.sh scripts to cycle through the channels. 

2) Setup a "crontab" to run generate-channels-daily-schedule.sh script to automate each PseudoChannel.py to generate the daily
schedule.

3) Use, "updatechannels.sh" to update each channels' local db with newly added Plex library items. 

4) Use, "manual.sh" to manually trigger a particular channel... i.e. `./manual.sh 9`, to switch to channel 9.

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
--generate-channels-daily-schedule.sh
--updatechannels.sh
```

*Note: this functionality is still being tweaked as are the bash scripts so only attempt this implementation if you are somewhat confident to tinker with bash/crontabs, etc. Or feel free to contact us at github or the discord chat room dedicated to PseudoChannel.tv. Just check the repo for more info. 