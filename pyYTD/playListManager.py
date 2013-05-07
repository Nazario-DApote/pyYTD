import urllib
import os
from xml.etree import ElementTree as ET
import re
from datetime import datetime, date, timedelta
from ytdHelper import Helper

class VideoItem:
    _Date = date(1900, 1, 1)
    _Title = str()
    _Description = str()
    _Link = str()
    _Author = str()

    @property
    def Date(self):
        return self._Date

    @Date.setter
    def Date(self, value):
        self._Date = value

    @property
    def Title(self):
        return self._Title

    @Title.setter
    def Title(self, value):
        self._Title = value

    @property
    def Description(self):
        return self._Description

    @Description.setter
    def Description(self, value):
        self._Description = value

    @property
    def Link(self):
        return self._Link

    @Link.setter
    def Link(self, value):
        self._Link = value

    @property
    def Author(self):
        return self._Author

    @Author.setter
    def Author(self, value):
        self._Author = value

    def __init__(self):
        self._Date = date(1900, 1, 1)
        pass

class PlayListManager:
    _Title = str()
    _Playlist = []

    @property
    def Title(self):
        return self._Title

    @property
    def Playlist(self):
        return self._Playlist

    '''Get all video links from a YouTube playlist link'''
    def __init__(self):
        pass

    def Fetch(self, url):
        try:
            feedUrl = self.__parseUrl__(url)
            self.__parsePlaylist__(feedUrl)

        except Exception, err:
            print str(err)

    def __parseUrl__(serf, url):
        match = re.search(r'(?:http://www.youtube.com/playlist\?&?list=)(?P<Pid>.+)&?', url)
        if match:
            t = match.groups("Pid")
            return "http://gdata.youtube.com/feeds/api/playlists/" + match.groups("Pid")[0]

    def __parsePlaylist__(self, url):
            u = urllib.urlopen(url)

            #self.__download__(u, "plist_debug.xml")

            #try:
            #    localFile = open('plist_debug.xml', 'w')
            #    localFile.write(u.read())
            #finally:
            #    localFile.close()
           
            root = ET.parse(u).getroot()
            if root is not None:
                self.__getEntries__(root)

            u.close()

    def __getEntries__(self, root):
        nextUrl = str()
        namespace = '{http://www.w3.org/2005/Atom}'

        for parts in root:
            if parts.tag == (namespace + 'title'):
                title = parts.text
            if parts.tag == (namespace + 'title'):
                title = parts.text
            if parts.tag == (namespace + 'link') and parts.attrib['rel']:
                if parts.attrib['rel'] == 'next':
                    nextUrl = parts.attrib['href']
            if parts.tag == (namespace + 'entry'):
                vi = VideoItem()
                for entry in list(parts):
                    if entry.tag == (namespace + 'title'):
                        vi.Title = entry.text
                    if entry.tag == (namespace + 'published'):
                        vi.Date = self.__gt__(entry.text)
                    if entry.tag == (namespace + 'link') and entry.attrib['rel']:
                        if entry.attrib['rel'] == 'alternate' and Helper.CheckUrl(entry.attrib['href']):
                            vi.Link = entry.attrib['href']
                    if entry.tag == (namespace + 'content'):
                        vi.Description = entry.text
                    if entry.tag == (namespace + 'author'):
                        for authorItem in list(entry):
                            if authorItem.tag == (namespace + 'name'):
                                vi.Author = authorItem.text

                self._Playlist.append(vi)

        if Helper.CheckUrl(nextUrl):
            self.__parsePlaylist__(nextUrl)
        
    def Save(self, filename, full):

        try:

            with open(filename, 'w') as fw:
                for video in self._Playlist:
                    if full:
                        lines = ["Title: " + video.Title, \
                            "Description: " + video.Description, \
                            "Author: " + video.Author, \
                            "Date: " + unicode(video.Date), \
                            "Link: " + video.Link, ""]
                    else:
                        lines = [video.Link] 

                    fw.writelines(("%s\n" % l for l in lines))
                fw.close()

        except Exception, err:
            print str(err)

    def __gt__(self, dt_str):
            dt, _, us= dt_str.partition(".")
            dt= datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
            us= int(us.rstrip("Z"), 10)
            return dt + timedelta(microseconds=us)

    def __download__(self, u, file_name):
        f = open(file_name, 'wb')
        meta = u.info()

        file_size = int(1)
        if( meta.getheaders("Content-Length") ):
            file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,

        f.close()

########################################################################
# This is the entry point for Debug
########################################################################

if __name__ == '__main__':
    fd = PlayListManager()
    fd.Fetch("http://www.youtube.com/playlist?list=PL2D1942A4688E9D63")    
