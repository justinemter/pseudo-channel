#!/usr/bin/env python

from plexapi.server import PlexServer
from datetime import datetime
import sqlite3

import thread,SocketServer,SimpleHTTPServer

from yattag import Doc
from yattag import indent
import os, sys

import logging
import logging.handlers

class PseudoDailyScheduleController():

    def __init__(self, 
                 server, 
                 token, 
                 clients, 
                 controllerServerPath = '', 
                 controllerServerPort = '8000', 
                 debugMode = False
                 ):

        self.PLEX = PlexServer(server, token)

        self.BASE_URL = server

        self.TOKEN = token

        self.PLEX_CLIENTS = clients

        self.CONTROLLER_SERVER_PATH = controllerServerPath

        self.CONTROLLER_SERVER_PORT = controllerServerPort

        self.DEBUG = debugMode

        self.webserverStarted = False

        self.my_logger = logging.getLogger('MyLogger')
        self.my_logger.setLevel(logging.DEBUG)

        self.handler = logging.handlers.SysLogHandler(address = '/dev/log')

        self.my_logger.addHandler(self.handler)

    '''
    *
    * Get the full image url (including plex token) from the local db.
    * @param seriesTitle: case-unsensitive string of the series title
    * @return string: full path of to the show image
    *
    '''
    def get_show_photo(self, section, title):

        backgroundImagePath = None

        backgroundImgURL = ''

        try:

            backgroundImagePath = self.PLEX.library.section(section).get(title)

        except:

            return backgroundImgURL

        if backgroundImagePath != None and isinstance(backgroundImagePath.art, str):

            backgroundImgURL = self.BASE_URL+backgroundImagePath.art+"?X-Plex-Token="+self.TOKEN

        return backgroundImgURL

    def start_server(self):

        if self.webserverStarted == False:

            """Changing dir to the schedules dir."""
            web_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'schedules'))
            os.chdir(web_dir)

            PORT = int(self.CONTROLLER_SERVER_PORT)

            class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

                def log_message(self, format, *args):
                    return

            global httpd
            try:
                #print "Starting webserver at port: ", PORT
                # create the httpd handler for the simplehttpserver
                # we set the allow_reuse_address incase something hangs can still bind to port
                class ReusableTCPServer(SocketServer.TCPServer): allow_reuse_address=True
                # specify the httpd service on 0.0.0.0 (all interfaces) on port 80
                httpd = ReusableTCPServer(("0.0.0.0", PORT),MyHandler)

                # thread this mofo
                thread.start_new_thread(httpd.serve_forever,())

            # handle keyboard interrupts
            except KeyboardInterrupt:
                core.print_info("Exiting the SET web server...")
                httpd.socket.close()

            # handle the rest
            #except Exception:
            #    print "[*] Exiting the SET web server...\n"
            #    httpd.socket.close()

            self.webserverStarted = True

    def get_xml_from_daily_schedule(self, currentTime, bgImageURL, datalist):

        now = datetime.now()

        time = now.strftime("%B %d, %Y")

        doc, tag, text, line = Doc(

        ).ttl()

        doc.asis('<?xml version="1.0" encoding="UTF-8"?>')

        with tag('schedule', currently_playing_bg_image=bgImageURL if bgImageURL != None else ''):

            for row in datalist:

                if str(row[11]) == "Commercials" and self.DEBUG == False:

                    continue

                timeB = datetime.strptime(row[8], '%I:%M:%S %p')

                if currentTime == None:
                
                    with tag('time',
                            ('data-key', str(row[12])),
                            ('data-current', 'false'),
                            ('data-type', str(row[11])),
                            ('data-title', str(row[3])),
                            ('data-start-time', str(row[8])),
                        ):

                        text(row[8])

                elif currentTime.hour == timeB.hour and currentTime.minute == timeB.minute:

                    with tag('time',
                            ('data-key', str(row[12])),
                            ('data-current', 'true'),
                            ('data-type', str(row[11])),
                            ('data-title', str(row[3])),
                            ('data-start-time', str(row[8])),
                        ):

                        text(row[8])

                else:

                    with tag('time',
                            ('data-key', str(row[12])),
                            ('data-current', 'false'),
                            ('data-type', str(row[11])),
                            ('data-title', str(row[3])),
                            ('data-start-time', str(row[8])),
                        ):

                        text(row[8])

        return indent(doc.getvalue())


    '''
    *
    * Get the generated html for the .html file that is the schedule. 
    * ...This is used whenever a show starts or stops in order to add and remove various styles.
    * @param currentTime: datetime object 
    * @param bgImageURL: str of the image used for the background
    * @return string: the generated html content
    *
    '''
    def get_html_from_daily_schedule(self, currentTime, bgImageURL, datalist):

        now = datetime.now()

        time = now.strftime("%B %d, %Y")

        doc, tag, text, line = Doc(

        ).ttl()

        doc.asis('<!DOCTYPE html>')

        with tag('html'):

            with tag('head'):

                with tag('title'):

                    text(time + " - Daily Pseudo Schedule")

                doc.asis('<link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" rel="stylesheet">')
                doc.asis('<link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" rel="stylesheet">')
                doc.asis('<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>')

                doc.asis("""
        <script>
        $(function(){

            var refreshFlag = '';
            """
            +"""var controllerServerPath ='"""+self.CONTROLLER_SERVER_PATH+":"+self.CONTROLLER_SERVER_PORT+"""';

            if(controllerServerPath != ''){

                console.log("here");

                window.setInterval(function(){

                $.ajax({
                        url: controllerServerPath+"/pseudo_refresh.txt",
                        async: true,   // asynchronous request? (synchronous requests are discouraged...)
                        cache: false,   // with this, you can force the browser to not make cache of the retrieved data
                        dataType: "text",  // jQuery will infer this, but you can set explicitly
                        success: function( data, textStatus, jqXHR ) {
                            newFlag = data; 

                            if(refreshFlag != ''){
                            
                                if (refreshFlag != newFlag){

                                    location.reload();

                                } else {

                                    //do nothing
                                    console.log("skip");

                                }

                            } else {

                                refreshFlag = newFlag;

                            }

                        }
                    });
                }, 1000);

            } else {

                setTimeout(function() {location.reload();}, 30000);

            }

        });
        </script>
                            """)

                if bgImageURL != None:
                    doc.asis('<style>body{ background:transparent!important; } html { background: url('+bgImageURL+') no-repeat center center fixed; -webkit-background-size: cover;-moz-background-size: cover;-o-background-size: cover;background-size: cover;}.make-white { padding: 24px; background:rgba(255,255,255, 0.9); }</style>')

            with tag('body'):

                with tag('div', klass='container mt-3'):

                    with tag('div', klass='row make-white'):

                        with tag('div'):

                            with tag('div'):

                                line('h1', "Daily Pseudo Schedule", klass='col-12 pl-0')

                            with tag('div'):

                                line('h3', time, klass='col-12 pl-1')

                        with tag('table', klass='col-12 table table-bordered table-hover'):

                            with tag('thead', klass='table-info'):
                                with tag('tr'):
                                    with tag('th'):
                                        text('#')
                                    with tag('th'):
                                        text('Type')
                                    with tag('th'):
                                        text('Series')
                                    with tag('th'):
                                        text('Title')
                                    with tag('th'):
                                        text('Start Time')

                            numberIncrease = 0

                            for row in datalist:

                                if str(row[11]) == "Commercials" and self.DEBUG == False:

                                    continue

                                numberIncrease += 1

                                with tag('tbody'):

                                    timeB = datetime.strptime(row[8], '%I:%M:%S %p')

                                    if currentTime == None:

                                        with tag('tr'):
                                            with tag('th', scope='row'):
                                                text(numberIncrease)
                                            with tag('td'):
                                                text(row[11])
                                            with tag('td'):
                                                text(row[6])
                                            with tag('td'):
                                                text(row[3])
                                            with tag('td'):
                                                text(row[8])

                                    elif currentTime.hour == timeB.hour and currentTime.minute == timeB.minute:

                                            with tag('tr', klass='bg-info'):

                                                with tag('th', scope='row'):
                                                    text(numberIncrease)
                                                with tag('td'):
                                                    text(row[11])
                                                with tag('td'):
                                                    text(row[6])
                                                with tag('td'):
                                                    text(row[3])
                                                with tag('td'):
                                                    text(row[8])

                                    else:

                                        with tag('tr'):
                                            with tag('th', scope='row'):
                                                text(numberIncrease)
                                            with tag('td'):
                                                text(row[11])
                                            with tag('td'):
                                                text(row[6])
                                            with tag('td'):
                                                text(row[3])
                                            with tag('td'):
                                                text(row[8])


        return indent(doc.getvalue())

    '''
    *
    * Create 'schedules' dir & write the generated html to .html file.
    * @param data: html string
    * @return null
    *
    '''
    def write_schedule_to_file(self, data):

        now = datetime.now()

        fileName = "index.html"

        writepath = './' if os.path.basename(os.getcwd()) == "schedules" else "./schedules/"

        if not os.path.exists(writepath):

            os.makedirs(writepath)

        if os.path.exists(writepath+fileName):
            
            os.remove(writepath+fileName)

        mode = 'a' if os.path.exists(writepath) else 'w'

        with open(writepath+fileName, mode) as f:

            f.write(data)

        self.start_server()

    '''
    *
    * Create 'schedules' dir & write the generated xml to .xml file.
    * @param data: xml string
    * @return null
    *
    '''
    def write_xml_to_file(self, data):

        now = datetime.now()

        fileName = "pseudo_schedule.xml"

        writepath = './' if os.path.basename(os.getcwd()) == "schedules" else "./schedules/"

        if not os.path.exists(writepath):

            os.makedirs(writepath)

        if os.path.exists(writepath+fileName):
            
            os.remove(writepath+fileName)

        mode = 'a' if os.path.exists(writepath) else 'w'

        with open(writepath+fileName, mode) as f:

            f.write(data)


    '''
    *
    * Write 0 or 1 to file for the ajax in the schedule.html to know when to refresh
    * @param data: xml string
    * @return null
    *
    '''
    def write_refresh_bool_to_file(self):

        fileName = "pseudo_refresh.txt"

        writepath = './' if os.path.basename(os.getcwd()) == "schedules" else "./schedules/"

        first_line = ''

        if not os.path.exists(writepath):

            os.makedirs(writepath)

        if not os.path.exists(writepath+fileName):

            file(writepath+fileName, 'w').close()

        mode = 'r+'

        with open(writepath+fileName, mode) as f:

            f.seek(0)

            first_line = f.read()  

            print first_line

            if first_line == '' or first_line == "0":

                f.seek(0)
                f.truncate()
                f.write("1")

            else:

                f.seek(0)
                f.truncate()
                f.write("0")

            #f.close()

    '''
    *
    * Trigger "playMedia()" on the Python Plex API for specified media.
    * @param mediaType: str: "TV Shows"
    * @param mediaParentTitle: str: "Seinfeld"
    * @param mediaTitle: str: "The Soup Nazi"
    * @return null
    *
    '''
    def play_media(self, mediaType, mediaParentTitle, mediaTitle):


        try: 

            if mediaType == "TV Shows":

                mediaItems = self.PLEX.library.section(mediaType).get(mediaParentTitle).episodes()

                for item in mediaItems:

                # print(part.title)

                    if item.title == mediaTitle:

                        for client in self.PLEX_CLIENTS:

                            clientItem = self.PLEX.client(client)

                            clientItem.playMedia(item)
                            
                        break

            elif mediaType == "Movies":

                movie =  self.PLEX.library.section(mediaType).get(mediaTitle)

                for client in self.PLEX_CLIENTS:

                        clientItem = self.PLEX.client(client)

                        clientItem.playMedia(movie)

            elif mediaType == "Commercials":

                movie =  self.PLEX.library.section(mediaType).get(mediaTitle)

                for client in self.PLEX_CLIENTS:

                        clientItem = self.PLEX.client(client)

                        clientItem.playMedia(movie)

            else:

                print("Not sure how to play {}".format(mediaType))

        except Exception as e:

            print e.__doc__

            print e.message

            print "There was an error trying to play the media."

            pass
        
    '''
    *
    * If tv_controller() does not find a "startTime" for scheduled media, search for an "endTime" match for now time.
    * ...This is useful for clearing the generated html schedule when media ends and there is a gap before the next media.
    * @param null
    * @return null
    *
    '''
    def check_for_end_time(self, datalist):

        currentTime = datetime.now()

        """c.execute("SELECT * FROM daily_schedule")

        datalist = list(c.fetchall())
        """
        for row in datalist:

            try:
                
                endTime = datetime.strptime(row[9], '%Y-%m-%d %H:%M:%S.%f')

            except ValueError:

                endTime = datetime.strptime(row[9], '%Y-%m-%d %H:%M:%S')

            if currentTime.hour == endTime.hour:

                if currentTime.minute == endTime.minute:

                    if currentTime.second == endTime.second:

                        print("Ok end time found")

                        self.write_schedule_to_file(self.get_html_from_daily_schedule(None, None, datalist))
                        self.write_xml_to_file(self.get_xml_from_daily_schedule(None, None, datalist))

                        self.write_refresh_bool_to_file()

                        break

    def play(self, row, datalist):

        print("Starting Media: " + row[3])
        print(row)

        timeB = datetime.strptime(row[8], '%I:%M:%S %p')

        self.play_media(row[11], row[6], row[3])

        self.write_schedule_to_file(
            self.get_html_from_daily_schedule(
                timeB,
                self.get_show_photo(
                    row[11], 
                    row[6] if row[11] == "TV Shows" else row[3]
                ),
                datalist
            )
        )

        self.write_refresh_bool_to_file()

        """Generate / write XML to file
        """
        self.write_xml_to_file(
            self.get_xml_from_daily_schedule(
                timeB,
                self.get_show_photo(
                    row[11], 
                    row[6] if row[11] == "TV Shows" else row[3]
                ),
                datalist
            )
        )

        self.my_logger.debug('Trying to play: ' + row[3])


    '''
    *
    * Check DB / current time. If that matches a scheduled shows startTime then trigger play via Plex API
    * @param null
    * @return null
    *
    '''
    def tv_controller(self, datalist):

        datalistLengthMonitor = 0;

        currentTime = datetime.now()

        """c.execute("SELECT * FROM daily_schedule ORDER BY datetime(startTimeUnix) ASC")

        datalist = list(c.fetchall())"""

        self.my_logger.debug('TV Controller')

        for row in datalist:

            timeB = datetime.strptime(row[8], '%I:%M:%S %p')

            if currentTime.hour == timeB.hour:

                if currentTime.minute == timeB.minute:

                    if currentTime.second == timeB.second:

                        print("Starting Media: " + row[3])
                        print(row)

                        self.play_media(row[11], row[6], row[3])

                        self.write_schedule_to_file(
                            self.get_html_from_daily_schedule(
                                timeB,
                                self.get_show_photo(
                                    row[11], 
                                    row[6] if row[11] == "TV Shows" else row[3]
                                ),
                                datalist
                            )
                        )

                        self.write_refresh_bool_to_file()

                        """Generate / write XML to file
                        """
                        self.write_xml_to_file(
                            self.get_xml_from_daily_schedule(
                                timeB,
                                self.get_show_photo(
                                    row[11], 
                                    row[6] if row[11] == "TV Shows" else row[3]
                                ),
                                datalist
                            )
                        )

                        self.my_logger.debug('Trying to play: ' + row[3])

                        break

            datalistLengthMonitor += 1

            if datalistLengthMonitor >= len(datalist):

                self.check_for_end_time(datalist)

    def make_xml_schedule(self, datalist):

        print "+++++ ", "Writing XML / HTML to file."

        self.write_refresh_bool_to_file()
        self.write_schedule_to_file(self.get_html_from_daily_schedule(None, None, datalist))
        self.write_xml_to_file(self.get_xml_from_daily_schedule(None, None, datalist))