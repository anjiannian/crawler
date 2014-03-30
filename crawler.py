#!/usr/bin/env python
# encoding: utf-8

import urllib2
import sys
import urlparse
from cgi import escape
from bs4 import BeautifulSoup

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

class Crawler(object):

    """Docstring for Crawler. """

    def __init__(self, url, max_depth=1):
        """@todo: to be defined1. """
        self.url = url
        self.max_depth = max_depth

    def crawl(self):
        tocrawl = [self.url]
        crawled = []
        depth = 0
        next_depth = []

        while tocrawl and depth <= self.max_depth:
            page = tocrawl.pop()
            print page
            if page not in crawled:
                union(next_depth, get_all_links(page))
                crawled.append(page)
            if not tocrawl:
                print 'xxxxxx'
                tocrawl, next_depth = next_depth, []
                depth += 1
        return crawled

def union(list_p, list_q):
    for p in list_q:
        if p not in list_p:
            list_p.append(p)

def get_all_links(url):
    page = GetLinks(url)
    page.getlinks()
    return page.urls

class GetLinks(object):

    """Docstring for GetLinks. """

    def __init__(self, url):
        """@todo: to be defined1.

        :url: @todo

        """
        self.url = url
        self.urls = []
    def open(self):
        try:
            request = urllib2.Request(self.url)
            request.add_header('User-Agent', user_agent)
            response = urllib2.urlopen(request)
        except IOError:
            return None
        return response
    def getlinks(self):
        response = self.open()
        if response:
            try:
                content = unicode(response.read(), "utf-8",
                        errors = "replace")
                soup = BeautifulSoup(content)
                tags = soup('a')
            except urllib2.HTTPError, error:
                if error.getcode() == 404:
                    print >> sys.stderr, "ERROR: %s -> %s" % (error, error.url)
                else:
                    print >> sys.stderr, "ERROR: %s" % error
                tags = []
            except urllib2.URLError, error:
                print >> sys.stderr, "ERROR: %s" % error
                tags = []
            for tag in tags:
                href = tag.get("href")
                if href is not None:
                    url = urlparse.urljoin(self.url, escape(href))
                    if url not in self.urls:
                        self.urls.append(url)

urls = get_all_links('http://www.baidu.com')
for url in urls:
    print url
#anjn = Crawler('http://anjn.info')
#print anjn.crawl()
wiki = Crawler('file:///Users/anjiannian/Dropbox/wiki/index.html')
print wiki.crawl()
