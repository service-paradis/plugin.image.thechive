# -*- coding: utf8 -*-

# Copyright (C) 2017- Alexandre Paradis <service.paradis@gmail.com>
# This program is Free Software see LICENSE file for details

import xbmc
import xbmcplugin
import xbmcgui
import routing
from resources.lib.Utils import *

plugin = routing.Plugin()


#todo detect and play GIF
#todo detect and play videos
#todo useful functions in Utils
@plugin.route('/')
def root():
    items = [
        (plugin.url_for(allposts), xbmcgui.ListItem("All posts"), True),
        (plugin.url_for(browsebycategories), xbmcgui.ListItem("Browse by categories"), True),
        #todo other ways to browse content?
    ]
    xbmcplugin.addDirectoryItems(plugin.handle, items)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/allposts')
def allposts():
    #todo try busy_dialog (view Utils)
    xbmcplugin.setContent(plugin.handle, 'genres')
    cnt = min(get_thechive_pages(), MAX_PAGES)
    items = []
    for i in range(1, cnt+1):
        items.append((plugin.url_for(allposts_view, i),
                     xbmcgui.ListItem('Page ' + str(i)),
                     True))
    xbmcplugin.addDirectoryItems(plugin.handle, items)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/allposts/<page>')
def allposts_view(page):
    xbmcplugin.setContent(plugin.handle, 'images')
    items = get_thechive_posts(page=int(page))
    xbmcplugin.addDirectoryItems(plugin.handle, items)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/post/<post_id>')
def post_view(post_id):
    xbmcplugin.setContent(plugin.handle, 'images')
    items = get_thechive_post(post_id)
    for item in items:
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),
                                    url=item["thumb"],
                                    listitem=item['li'],
                                    isFolder=False)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/browsebycategories')
def browsebycategories():
    #todo try busy_dialog (view Utils)
    xbmcplugin.setContent(plugin.handle, 'genres')
    items = get_thechive_categories()
    xbmcplugin.addDirectoryItems(plugin.handle, items)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/category/<category_id>')
def category_view(category_id):
    xbmcplugin.setContent(plugin.handle, 'genres')
    cnt = min(get_thechive_pages(ITEMS_PER_PAGE, category_id), MAX_PAGES)
    items = []
    for i in range(1, cnt+1):
        items.append((plugin.url_for(categoryposts_view, category_id, i),
                      xbmcgui.ListItem('Page ' + str(i)),
                      True))
    xbmcplugin.addDirectoryItems(plugin.handle, items)
    xbmcplugin.endOfDirectory(plugin.handle)


@plugin.route('/category/<category_id>/<page>')
def categoryposts_view(category_id, page):
    xbmcplugin.setContent(plugin.handle, 'images')
    items = get_thechive_posts(page=int(page), category=category_id)
    xbmcplugin.addDirectoryItems(plugin.handle, items)
    xbmcplugin.endOfDirectory(plugin.handle)


def get_thechive_pages(per_page=ITEMS_PER_PAGE, category=None):
    url = REST_URL + 'posts?context=embed&per_page=' + str(per_page) + '&page=1'
    if category is not None:
        url = url + '&categories=' + category

    response = get_url_response(url)
    pages = response.info().getheader('x-wp-totalpages')
    return int(pages)


def get_thechive_posts(page=1, per_page=ITEMS_PER_PAGE, category=None):
    url = REST_URL + 'posts?context=embed&per_page=' + str(per_page) + '&page=' + str(page)
    if category is not None:
        url = url + '&categories=' + category

    posts = get_json_data(url)

    items = []
    for post in posts:
        title = html.unescape(post['title']['rendered'])
        list_item = xbmcgui.ListItem(title)
        list_item.setInfo('pictures', {'title': title})
        list_item.setArt({'thumb': post['featured_image_url'],
                          'icon': post['featured_image_url']})
        items.append((plugin.url_for(post_view, post['id']),
                      list_item,
                      True))

    return items


def get_thechive_post(post_id):
    url = REST_URL + 'posts/' + str(post_id)

    post = get_json_data(url)

    content = post['content']['rendered'].replace('\n', ' ').replace('\r', '').replace('\t', '')
    soup = BeautifulSoup(content)
    items = []
    for figure in soup.findAll('figure'):
        img = figure.find('img').get('src')
        label = figure.find("div", { "class" : "count-tag" }).string
        #todo figcaption always returning empty with beautifulsoup... ?!?
        #caption_text = ''
        #caption = figure.figcaption
        #if caption:
        #    caption_text = str(caption)
        #todo display attribution if there are one (which property should we use?)
        #attribution = figure.find('gallery-attribution', { 'class' : 'gallery-attribution' })
        list_item = xbmcgui.ListItem(label,
                                     iconImage="DefaultImage.png",
                                     thumbnailImage=img)
        list_item.setInfo("image",
                          {"title": figure.get('id')})
        #list_item.setProperty("description", caption_text)
        items.append({'li' : list_item, 'thumb' : img})

    return items


def get_thechive_categories():
    items = []
    page = 1
    pages = 1
    while page <= int(pages):
        url = REST_URL + 'categories?per_page=100&page='+str(page) #WP Rest API maximum value is 100
        response = get_url_response(url)
        if pages == 1:
            pages = response.info().getheader('x-wp-totalpages')

        categories = simplejson.load(response)
        for cat in categories:
            if cat['count'] >= 100: #We only display categories having at least 100 galleries
                title = html.unescape(cat['name'])
                items.append((plugin.url_for(category_view, cat['id']),
                             xbmcgui.ListItem(title),
                             True))
        page = page+1

    return items

if (__name__ == "__main__"):
    plugin.run()
xbmc.log('finished')
