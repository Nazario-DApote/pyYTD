import re
import urllib
import httplib, urlparse
#import ImageFile

def if_else(condition, trueVal, falseVal):
    if condition:
        return trueVal
    else:
        return falseVal

class Helper:

    _urlValid = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def __init__(self):
        pass

    @staticmethod
    def CheckUrl(url):
        return Helper._urlValid.match(url)

    @staticmethod
    def GetTxtBtwn(s, left, right):
        '''picking up piece of string between separators
        function using partition, like partition, but drops the separators'''
        before,_,a = s.partition(left)
        a,_,after = a.partition(right)
        return before,a,after

    @staticmethod
    def GetHTMLPage(url):
        uresponse = urllib.urlopen(url) #open url
        contents = urllib.unquote_plus(uresponse.read()).decode('utf-8') #read from url file
        uresponse.close()
        return contents

    @staticmethod
    def getSize(uri):
        # http://effbot.org/zone/pil-image-size.htm
        # check the uri
        scheme, host, path, params, query, fragment = urlparse.urlparse(uri)
        if scheme != "http":
            raise ValueError("only supports HTTP requests")
        if not path:
            path = "/"
        if params:
            path = path + ";" + params
        if query:
            path = path + "?" + query

        # make a http HEAD request
        h = httplib.HTTP(host)
        h.putrequest("HEAD", path)
        h.putheader("Host", host)
        h.endheaders()

        status, reason, headers = h.getreply()

        h.close()

        return headers.get("content-length")

    @staticmethod
    def getSize(url):
        file = urllib.urlopen(url)
        size = file.headers.get("content-length")
        file.close()
        return size

    #@staticmethod
    #def getImageSize(uri):
    #    # get file size *and* image size (None if not known)
    #    file = urllib.urlopen(uri)
    #    size = file.headers.get("content-length")
    #    if size: size = int(size)
    #    p = ImageFile.Parser()
    #    while 1:
    #        data = file.read(1024)
    #        if not data:
    #            break
    #        p.feed(data)
    #        if p.image:
    #            return size, p.image.size
    #            break
    #    file.close()
    #    return size, None

class Size:
    _width = 0
    _height = 0

    @property
    def Width(self):
        return self._width

    @property
    def Height(self):
        return self._height

    def __init__(self, width, height):
        self._width = width
        self._height = height