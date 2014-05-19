# -*- coding: utf-8 -*-
import os

# Force dev mode even on deployed app.
# Caching and error reporting use this setting.
# Only use while debugging!
FORCE_DEV = True

# Application title and meta settings
APP_TITLE = 'GAE-Boilerplate'
APP_DESCRIPTION = 'The ultimate GAE boilerplate'
APP_KEYWORDS = 'HTML5 Boilerplate, Font Awesome, Twitter Bootstrap, Jinja2'
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
  'canonical': 'http://localhost:8080',
  'canonical_secure': 'https://localhost:8080'
}