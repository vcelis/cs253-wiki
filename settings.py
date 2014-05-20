# -*- coding: utf-8 -*-
import os
import re

# Force dev mode even on deployed app.
# Caching and error reporting use this setting.
# Only use while debugging!
FORCE_DEV = True

# Application title and meta settings
APP_TITLE = 'Wiki'
APP_DESCRIPTION = 'The ultimate GAE wiki'
APP_KEYWORDS = 'Wiki, GAE, Udacity, CS253, Google App Engine, vincentcelis.be'
APP_AUTHOR = 'Vincent Celis'

# The directory where the templates live
TEMPLATE_DIR = 'templates'
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), TEMPLATE_DIR)
# Enable/Disable jinja2 auto escape
TEMPLATE_ESCAPE = True

# Jinja2 cache timeout
JINJA2_BYTECODE_TIMEOUT = 3600

# URLS
APP_URLS = {
  'canonical': 'http://uda-cs253-wiki.appspot.com',
  'canonical_secure': 'http://uda-cs253-wiki.appspot.com'
}

# Regex for different fields
RE_USERNAME = re.compile(r'^[a-zA-Z0-9_-]{3,20}$')
RE_PASSWORD = re.compile(r'^.{3,20}$')
RE_EMAIL = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

# Cookie salt
COOKIE_SALT = r'Z}QKEA~Qe.f4&uz,t@XXbA.>(~RY>ZcYUPK45Udz<f.=;n3Gn)dFKf&M*.S2tqT}'

RESERVED_PAGES = [ '/_edit', '/_history', '/login','/signup', '/logout', '/', '' ]