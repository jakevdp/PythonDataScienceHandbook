#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://jakevdp.github.io/PythonDataScienceHandbook'
RELATIVE_URLS = False

SHOW_FEED = False
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
FEED_USE_SUMMARY = True  # from the feed_summary plugin

DELETE_OUTPUT_DIRECTORY = True

DISQUS_SITENAME = "pythonicperambulations"
GOOGLE_ANALYTICS = "UA-34061646-1"
