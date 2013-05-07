import os, sys, re
import urllib
from ytdHelper import Helper, Size, if_else

class videoQuality:

    _videoTitle = str()
    _extention = str()
    _downloadUrl = str()
    _videoUrl = str()
    _videoSize = long()
    _dimension = Size(0,0)
    _length = long()

    @property
    def VideoTitle(self):
        return self._videoTitle;

    @VideoTitle.setter
    def VideoTitle(self, value):
        self._videoTitle = value

    @property
    def Extension(self):
        return self._extention;

    @Extension.setter
    def Extension(self, value):
        self._extention = value

    @property
    def DownloadUrl(self):
        return self._downloadUrl;

    @DownloadUrl.setter
    def DownloadUrl(self, value):
        self._downloadUrl = value

    @property
    def VideoUrl(self):
        return self._videoUrl;

    @DownloadUrl.setter
    def VideoUrl(self, value):
        self._videoUrl = value

    @property
    def VideoSize(self):
        return self._videoSize;

    @VideoSize.setter
    def VideoSize(self, value):
        self._videoSize = value

    @property
    def Dimension(self):
        return self._dimension;

    @VideoSize.setter
    def Dimension(self, value):
        self._dimension = value

    @property
    def Length(self):
        return self._length;

    @VideoSize.setter
    def Length(self, value):
        self._length = value

    def SetQuality(self, Extention, Dimension):
        self.Extension = Extention
        self.Dimension = Dimension

    def SetSize(self, size):
        self.VideoSize = size;

    def __init(self):
        pass

class ytDownloader:

    def __init(selft):
        pass

    @staticmethod
    def GetYouTubeVideoUrls(videoUrlsArray):

        urls = []

        if type(videoUrlsArray) is type([]):

            for videoUrl in videoUrlsArray:
                if Helper.CheckUrl(videoUrl):
                     html = Helper.GetHTMLPage(videoUrl)
                     ytDownloader.Save(html)
                     title = ytDownloader.GetTitle(html)
                     for videoLink in ytDownloader.ExtractUrls(html):
                        q = videoQuality()
                        q.DownloadUrl = videoLink + "&title=" + "'"+ title + "'";
                        if not ytDownloader.getSize(q):
                            continue
                        q.Length = re.search('"length_seconds":(.+?)', html, re.IGNORECASE).group(1)
                        IsWide = ytDownloader.IsWideScreen(html)
                        if ytDownloader.getQuality(q, IsWide):
                            urls.append(q)

        return urls

    @staticmethod
    def GetTitle(html):

        title = (Helper.GetTxtBtwn(html, "'VIDEO_TITLE': '", "'"))[1]
        if not len(title):
            title = Helper.GetTxtBtwn(html, "\"title\" content=\"", "\"")[1];
        if not len(title):
            title = Helper.GetTxtBtwn(html, "&title=", "&")[1];

        return title

    @staticmethod
    def getSize(videoQ):
        size = Helper.getSize(videoQ.DownloadUrl)
        if size > 0:
            videoQ.SetSize(size)
            return True
        return False

    @staticmethod
    def IsWideScreen(html):
        res = False;

        match = re.search("'IS_WIDESCREEN':\s+(.+?)\s+", html, re.IGNORECASE).group(1).lower().strip();
        res = ((match == "true") or (match == "true,"));
        return res;

    @staticmethod
    def getQuality(videoQ, _Wide):
        '''
        @type  videoQ: videoQuality
        @param videoQ: VideoQuality instance

        @rtype:   Boolean
        @return:  True if video size  is valid
        '''
        iTag = re.match("^(.*)itag=(\d+)", videoQ.DownloadUrl)
        if iTag != None:
            size = int(iTag.group(2))

            if size == 5: videoQ.SetQuality("flv", Size(320, if_else(_Wide, 180, 240)))
            elif size == 6: videoQ.SetQuality("flv", Size(480, if_else(_Wide, 270, 360)))
            elif size == 17: videoQ.SetQuality("3gp", Size(176, if_else(_Wide, 99, 144)))
            elif size == 18: videoQ.SetQuality("mp4", Size(640, if_else(_Wide, 360, 480)))
            elif size == 22: videoQ.SetQuality("mp4", Size(1280, if_else(_Wide, 720, 960)))
            elif size == 34: videoQ.SetQuality("flv", Size(640, if_else(_Wide, 360, 480)))
            elif size == 35: videoQ.SetQuality("flv", Size(854, if_else(_Wide, 480, 640)))
            elif size == 36: videoQ.SetQuality("3gp", Size(320, if_else(_Wide, 180, 240)))
            elif size == 37: videoQ.SetQuality("mp4", Size(1920, if_else(_Wide, 1080, 1440)))
            elif size == 38: videoQ.SetQuality("mp4", Size(2048, if_else(_Wide, 1152, 1536)))
            elif size == 43: videoQ.SetQuality("webm", Size(640, if_else(_Wide, 360, 480)))
            elif size == 44: videoQ.SetQuality("webm", Size(854, if_else(_Wide, 480, 640)))
            elif size == 45: videoQ.SetQuality("webm", Size(1280, if_else(_Wide, 720, 960)))
            elif size == 46: videoQ.SetQuality("webm", Size(1920, if_else(_Wide, 1080, 1440)))
            elif size == 42: videoQ.SetQuality("3D.mp4", Size(480, if_else(_Wide, 270, 360))) # 3D
            elif size ==83: videoQ.SetQuality("3D.mp4", Size(640, if_else(_Wide, 360, 480))) # 3D
            elif size ==84: videoQ.SetQuality("3D.mp4", Size(1280, if_else(_Wide, 720, 960))) # 3D
            elif size ==85: videoQ.SetQuality("3D.mp4", Size(1920, if_else(_Wide, 1080, 1440))) # 3D
            elif size ==100: videoQ.SetQuality("3D.webm", Size(640, if_else(_Wide, 360, 480))) # 3D
            elif size ==101: videoQ.SetQuality("3D.webm", Size(640, if_else(_Wide, 360, 480))) # 3D
            elif size ==102: videoQ.SetQuality("3D.webm", Size(1280, if_else(_Wide, 720, 960))) # 3D
            else: 
                videoQ.SetQuality("itag-" + size, Size(0, 0)) # unknown or parse error
                return False
            
            return True

        return False

    @staticmethod
    def ExtractUrls(html):
        urls = []
        DataBlockStart = "\"url_encoded_fmt_stream_map\":\\s+\"(.+)&" # Marks start of Javascript Data Block
        jsMatch = re.search(DataBlockStart, html, re.MULTILINE | re.IGNORECASE)

        if jsMatch != None:
            shtml = jsMatch.group(1)
            firstPattern =  shtml[0: shtml.index('=') + 1];
            matches = re.split(firstPattern, shtml)

            for i in range(len(matches)):
                matches[i] = firstPattern + matches[i];

            for match in matches:
                if match.find('url=') < 0: continue

                url = Helper.GetTxtBtwn(match, "url=", "\\u0026")[1];
                if not len(url): url = Helper.GetTxtBtwn(match, "url=", ",url")[1];
                if not len(url): url = Helper.GetTxtBtwn(match, "url=", "\",")[1];

                sig = Helper.GetTxtBtwn(match, "sig=", "\\u0026")[1];
                if not len(sig): sig = Helper.GetTxtBtwn(match, "sig=", ",sig")[1];
                if not len(sig): sig = Helper.GetTxtBtwn(match, "sig=", "\",")[1];

                while (url.endswith(',') or url.endswith(".")) or (url.endswith('"') ):
                    url = url[0:len(url)-2]

                while (sig.endswith(',') or sig.endswith(".")) or (sig.endswith('"') ):
                    sig = sig[0:len(sig)-2]

                if len(url) == 0: continue
                if len(sig):
                    url += "&signature=" + sig;

                urls.append(url)

        return urls
    
    @staticmethod
    def Save(html):
        with open("videopage.html", "wb") as fw:
            fw.write(html.encode("utf-8"))
            fw.close()

class RequestException(Exception):
    _message = str()

    @property
    def Message(self):
        return self._message

    def __init__(self, message):
        self._message = message


