# -*- coding: utf8 -*-

# Copyright (C) 2017- Alexandre Paradis <service.paradis@gmail.com>
# Thanks to Philipp Temminghoff <phil65@kodi.tv> for the inspiration
# This program is Free Software see LICENSE file for details

import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import xbmcplugin
import urllib2
#import os
#import sys
#import time
import simplejson #as json
from BeautifulSoup import BeautifulSoup

try:
    # Python 2.6-2.7
    from HTMLParser import HTMLParser
except ImportError:
    # Python 3
    from html.parser import HTMLParser

html = HTMLParser()

#ADDON = xbmcaddon.Addon()
#ADDON_ID = ADDON.getAddonInfo('id')
#ADDON_ICON = ADDON.getAddonInfo('icon')
#ADDON_NAME = ADDON.getAddonInfo('name')
#ADDON_PATH = ADDON.getAddonInfo('path').decode("utf-8")
#ADDON_VERSION = ADDON.getAddonInfo('version')
#ADDON_DATA_PATH = xbmc.translatePath("special://profile/addon_data/%s" % ADDON_ID).decode("utf-8")
#SETTING = ADDON.getSetting

REST_URL = 'http://thechive.com/wp-json/wp/v2/'
ITEMS_PER_PAGE = 25
MAX_PAGES = 100
DEFAULT_HEADERS = [('Accept', 'application/json'),
                   ('Origin', 'http://thechive.com'),
                   ('Referer', 'http://thechive.com')]


#todo some caching (view Utils)
def get_url_response(url, headers=DEFAULT_HEADERS):
    opener = urllib2.build_opener()
    opener.addheaders = headers
    return opener.open(url)


#todo some caching (view Utils)
def get_json_data(url, headers=DEFAULT_HEADERS):
    response = get_url_response(url, headers)
    return simplejson.load(response)


#def busy_dialog(func):
#    """
#    Decorator to show busy dialog while function is running
#    Only one of the decorated functions may run simultaniously
#    """
#
#    @wraps(func)
#    def decorator(self, *args, **kwargs):
#        xbmc.executebuiltin("ActivateWindow(busydialog)")
#        result = func(self, *args, **kwargs)
#        xbmc.executebuiltin("Dialog.Close(busydialog)")
#        return result
#
#    return decorator


#def get_http(url=None, headers=False):
#    """
#    fetches data from *url, returns it as a string
#    """
#    succeed = 0
#    if not headers:
#        headers = {'User-agent': 'XBMC/16.0 ( phil65@kodi.tv )'}
#    request = urllib2.Request(url)
#    log(url)
#    for (key, value) in headers.iteritems():
#        request.add_header(key, value)
#    while (succeed < 2) and (not xbmc.abortRequested):
#        try:
#            response = urllib2.urlopen(request, timeout=3)
#            log(response)
#            return response.read()
#        except:
#            log("get_http: could not get data from %s" % url)
#            xbmc.sleep(1000)
#            succeed += 1
#    return None


#def get_JSON_response(url="", cache_days=0.0, folder=False, headers=False):
#    """
#    get JSON response for *url, makes use of prop and file cache.
#    """
#    now = time.time()
#    hashed_url = hashlib.md5(url).hexdigest()
#    if folder:
#        cache_path = xbmc.translatePath(os.path.join(ADDON_DATA_PATH, folder))
#    else:
#        cache_path = xbmc.translatePath(os.path.join(ADDON_DATA_PATH))
#    path = os.path.join(cache_path, hashed_url + ".txt")
#    cache_seconds = int(cache_days * 86400.0)
#    if xbmcvfs.exists(path) and ((now - os.path.getmtime(path)) < cache_seconds):
#        results = read_from_file(path)
#        log("loaded file for %s. time: %f" % (url, time.time() - now))
#    else:
#        response = get_http(url, headers)
#        try:
#            results = json.loads(response)
#            log("download %s. time: %f" % (url, time.time() - now))
#            save_to_file(results, hashed_url, cache_path)
#        except:
#            log("Exception: Could not get new JSON data from %s. Tryin to fallback to cache" % url)
#            log(response)
#            if xbmcvfs.exists(path):
#                results = read_from_file(path)
#            else:
#                results = []
#    if results:
#        return results
#    else:
#        return []


#def log(txt):
#    if isinstance(txt, str):
#        txt = txt.decode("utf-8", 'ignore')
#    message = u'%s: %s' % (ADDON_ID, txt)
#    xbmc.log(msg=message.encode("utf-8", 'ignore'),
#             level=xbmc.LOGDEBUG)


#def save_to_file(content, filename, path=""):
#    """
#    dump json and save to *filename in *path
#    """
#    if not path:
#        return None
#    else:
#        if not xbmcvfs.exists(path):
#            xbmcvfs.mkdirs(path)
#        text_file_path = os.path.join(path, filename + ".txt")
#    now = time.time()
#    text_file = xbmcvfs.File(text_file_path, "w")
#    json.dump(content, text_file)
#    text_file.close()
#    log("saved textfile %s. Time: %f" % (text_file_path, time.time() - now))
#    return True


#def read_from_file(path="", raw=False):
#    """
#    return data from file with *path
#    """
#    if not path:
#        return None
#    if not xbmcvfs.exists(path):
#        return False
#    try:
#        with open(path) as f:
#            log("opened textfile %s." % (path))
#            if not raw:
#                result = json.load(f)
#            else:
#                result = f.read()
#        return result
#    except:
#        log("failed to load textfile: " + path)
#        return False


#def notify(header="", message="", icon=ADDON_ICON, time=5000, sound=True):
#    xbmcgui.Dialog().notification(heading=header,
#                                  message=message,
#                                  icon=icon,
#                                  time=time,
#                                  sound=sound)


#def prettyprint(string):
#    log(json.dumps(string,
#                   sort_keys=True,
#                   indent=4,
#                   separators=(',', ': ')))


#def add_image(item, total=0):
#    liz = xbmcgui.ListItem(str(item["index"]),
#                           iconImage="DefaultImage.png",
#                           thumbnailImage=item["thumb"])
#    liz.setInfo(type="image",
#                infoLabels={"Id": item["label"]})
#    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
#                                       url=item["thumb"],
#                                       listitem=liz,
#                                       isFolder=False,
#                                       totalItems=total)
