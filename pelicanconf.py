#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Maneesha Sane'
SITENAME = 'Cooking * Parenting * Programming'
SITESUBTITLE = "Not necessarily in that order"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

THEME = "../elegant"

# Blogroll
# LINKS = (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/maneeshasane'),
          ('GitHub', 'https://github.com/maneesha'),)

DEFAULT_PAGINATION = 10

ARTICLE_SAVE_AS = '{category}/{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_URL = '{category}/{date:%Y}/{date:%m}/{slug}.html'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
DISPLAY_SEARCH_FORM = True
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_CATEGORIES_ON_SUBMENU = True

PLUGIN_PATHS = ['plugins']
PLUGINS = ['tipue_search']
DIRECT_TEMPLATES = ["index", "tags", "categories", "archives", "search", "404"]


MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.admonition": {},
        "markdown.extensions.codehilite": {"css_class": "highlight"},
        "markdown.extensions.extra": {},
        "markdown.extensions.meta": {},
        "markdown.extensions.toc": {"permalink": " "},
    }
}
