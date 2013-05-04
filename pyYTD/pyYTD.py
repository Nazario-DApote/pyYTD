#!/usr/bin/env python

import os, sys
import getopt
import exceptions
import datetime
from plist import PlayListManager
import os.path

class pyYouTubeDownloader:

    # Option parameters variables
    download=False
    fileName=str()
    videoExtension="flv"
    videoWidth=0
    videoSize=0
    filelist=False
    help=False
    verbose=False
    playlist=False
    full=False

    def title(self):
        print
        print("---------------------------------------------")
        print("|        pyYouTubeDownloder v1.0.0.0         |")
        print("---------------------------------------------")
        print("The command line YoutTube video downloader.")
        print("Copyright \xa9 Nazario D'Apote 2013")
        print

    def usage(self):
        print
        print("Usage:")
        print("------")
        print("pyYTD [option] <url>")
        print
        print("Options:")
        print("--------------")
        print("-h | --help                 print the help.")
        print("-p | --playlist             get all video links from a playlist url and save to outfile")
        print("-f | --full                 when specified with -p export all video.")
        print("-d | --download             download the video url and save to output.")
        print("-l | --list                 consider the <url> parameter as a list of links.")
        print("-w | --width VALUE          specify the preferred video width.")
        print("-s | --size VALUE           specify the preferred video file size.")
        print("-e | --ext VALUE            specify the preferred video file extension.")
        print("-o | --output VALUE         specify the output file name.")
        print("-v | --verbose              show verbose message.")
        print

    def waitKeyPress(self):
        raw_input("Press Enter to continue...")

    def fetchArgs(self, argv):
        try:
            opts, args = getopt.getopt(argv, 'hdlo:w:s:e:vpf', 
                                       ["help", "download", "list", "output", \
                                        "width", "size", "ext", "verbose", "playlist", "full"])

        except getopt.GetoptError, err:
            print str(err)
            self.usage()
            sys.exit(-1)

        for o, a in opts:
            if o in ("-h", "--help"):
                usage()
                sys.exit(0)
            elif o in ("-d", "--download"):
               self.download=True
            elif o in ("-o", "--output"):
               self.fileName=a
            elif o in ("-p", "--playlist"):
               self.playlist=True
            elif o in ("-f", "--full"):
               self.full=True
            elif o in ("-l", "--list"):
               self.filelist=True
            elif o in ("-w", "--width"):
               self.videoWidth=a
            elif o in ("-s", "--size"):
               self.videoSize=a
            elif o in ("-e", "--ext"):
               self.videoExtension=a
            elif o in ("-v", "--verbose"):
               self.verbose=True
            else:
                print "ERROR: unhandled option"
                self.usage()
                sys.exit(-1)

        if len(args) == 0:
            print ("ERROR: Mandatory parameter missing!")
            print
            self.usage()
            sys.exit(-1)

        for arg in args:

            try:
                self.url = arg
            except exceptions.ValueError:
                print("ERROR: Station code must be an integer value")
                usage()
                sys.exit(-1)      

    def downloadVideo(self, url, filename):
        print "* Download YourTube video";
        print "url: %s" % url
        print "fileName: %s" % filename

        print "Fetching video informations ..."
        # TODO
        pass

    def main(self, argv):
        self.title()
        self.fetchArgs(argv)

        try:

            if self.playlist:
                print "* Playlist export"
                print "url: %s" % self.url
                print "fileName: %s" % self.fileName
                plm = PlayListManager()
                print "Playlist fetching ..."
                plm.Fetch(self.url)
                print "Playlist fetched."

                if len(plm.Playlist):
                    if not len(self.fileName):
                        self.fileName = plm.Title

                    plm.Save(self.fileName, self.full)
                else:
                    print "Playlist does not contain video."
            elif self.download:

                if self.filelist:
                    print "* Download YourTube videos from list";
                    print "URLs list: %s" % self.url
                    if os.path.isfile(self.url):
                        with open(self.url, 'r') as fr:
                            while True:
                                line = fr.readline()
                                if line:
                                    line = line.strip('\n')
                                    if PlayListManager().CheckUrl(line):
                                        self.downloadVideo(line, str())
                                else:
                                    break
                            fr.close()
                    else:
                        raise FileNotFoundException("File %s not found!" % self.fileName)
                else:
                    self.downloadVideo(url, fileName)
                pass

            self.waitKeyPress()

        except Exception, errDtl:
            print(errDtl)
            sys.exit(-1)

class FileNotFoundException(Exception):
    msg = str()

    @property
    def Message(self):
        return self.msg

    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

########################################################################
# This is the entry point
########################################################################

if __name__ == '__main__':
    pyYtd = pyYouTubeDownloader()
    pyYtd.main(sys.argv[1:])