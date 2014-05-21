# -*- coding: utf-8 -*-

# Copyright (c) 2014 Vincent Celis
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import re

# Enable/Disables GAE dev mode
FORCE_DEV = True

# Application title and meta settings
APP_TITLE = 'Wiki'
APP_DESCRIPTION = 'The ultimate GAE wiki'
APP_KEYWORDS = 'Wiki, GAE, Udacity, CS253, Google App Engine, vincentcelis.be'
APP_AUTHOR = 'Vincent Celis'
# URL's for the canonical meta information
APP_URLS = {
  'canonical': 'http://uda-cs253-wiki.appspot.com',
  'canonical_secure': 'http://uda-cs253-wiki.appspot.com'
}

# The directory where the templates live
TEMPLATE_DIR = 'templates'
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), TEMPLATE_DIR)
# Enable/Disable jinja2 auto escape
TEMPLATE_ESCAPE = True
# Jinja2 cache timeout
JINJA2_BYTECODE_TIMEOUT = 3600
# Template filenames
TEMPLATE_FILENAME = {
  'login': 'login.html',
  'signup': 'signup.html',
  'wiki': 'wiki.html',
  'edit': 'edit.html',
  'history': 'history.html',
  'search': 'search.html'
}

# Regex for form fields
RE_USERNAME = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
RE_PASSWORD = re.compile(r'^.{3,20}$')
RE_EMAIL = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
# Form validation error messages
RE_USERNAME_FAIL = 'That\'s not a valid username.'
RE_PASSWORD_FAIL = 'That\'s not a valid password.'
RE_EMAIL_FAIL = 'That\'s not a valid email.'
RE_PASSWORD_EMPTY = 'You didn\'t enter any password.'
RE_PASSWORD_MATCH = 'Your passwords didn\'t match.'

# Common cookie salt
COOKIE_SALT = r'Z}QKEA~Qef4&uz,t@XXbA>(~RY>ZcYUPK45Udz<f=;n3Gn)dFKf&MS2tqT}'

# Reserved pages that can't be edited; Avoids for example: /_edit/_edit/
RESERVED_PAGES = [ '/_edit', '/_history', '/login','/signup', '/logout',
                   '/search', '/', '' ]

# Search API wiki index name
SEARCH_INDEX_WIKI = 'wiki'