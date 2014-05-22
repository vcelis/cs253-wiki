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

import logging

import utils
import settings

from base import BaseHandler
from models import Page

class WikiPage(BaseHandler):
  """Page handler for the individual wiki pages

  Page handler to handle the requests for the individual wiki pages.
  Inherits common functionality from BaseHandler.
  """
  def get(self, name):
    """Handles the get requests for the wiki pages

    If a version is specified in the url it retreives the corresponding version
    of the requested page. If the version doesn't exists, it redirects to the
    requested page without a version specified.

    If no version is specified the latest version of the page will be retreived
    to be displayed.

    If there is no version of the page in the datastore, the user will be 
    redirected to '/_edit' which will be handled by EditPage.
    """
    name = utils.checkPage(name)
    last_pages = Page.getLast(10)
    version = self.request.get('v')

    try:
      version = None if not version else int(version)
    except ValueError:
      logging.error('Invalid version format givven')
      version = None

    if version:
      page = Page.query(ancestor=Page.getKey()).filter(Page.name == name)
      page = page.filter(Page.version == version).fetch()
      if not page:
        self.redirect('/%s' % name)
      else:
        params = { 'page':  page[0], 'last_pages': last_pages }
        self.render(settings.TEMPLATE_FILENAME['wiki'], **params)
    else:
      page = Page.query(ancestor=Page.getKey()).filter(Page.name == name).order(-Page.version).fetch()
      if not page:
        self.redirect('/_edit/%s' % name)
      else:
        params = { 'page': page[0], 'last_pages': last_pages }
        self.render(settings.TEMPLATE_FILENAME['wiki'], **params)

class EditPage(BaseHandler):
  """Page handler for the edit page of the individual wiki pages

  Page handler to handle the requests to edit the individual wiki pages.
  Inherits common functionality from BaseHandler.
  """
  def get(self, name):
    """Handles the get requests for edit page of the wiki pages

    The user will get redirected to the SignupPage if authentication fails.

    If a version is specified in the url it retreives the corresponding version
    of the requested page. If the version doesn't exists, it redirects to the
    requested edit page without a version specified.

    If no version is specified the latest version of the page will be retreived
    to be displayed.

    If there is no version of the page in the datastore, the requested name will
    be transformed and used for Page.name.
    """
    self.restrictedArea()
    name = utils.checkPage(name)

    version = self.request.get('v')
    version = 0 if not version else int(version) 
    
    page = Page.getName(name, version)

    if not page and version:
      self.redirect('/_edit/%s' % name)
      return None

    if not page and not version:
      page = Page.createPage(name)

    params = { 'page': page }
    self.render(settings.TEMPLATE_FILENAME['edit'], **params)

  def post(self, name):
    """Handles the post requests for edit page of the wiki pages

    The user will get redirected to the SignupPage if authentication fails.

    The entity will be stored and the user gets redirected to the new version of
    the page.
    """
    self.restrictedArea()
    name = utils.checkPage(name)

    page = Page.createPage(name, self.request.get('content'), self.user.name)
    page.put()

    utils.addSearchIndex(page)
    
    self.redirect('/%s' % name)

class HistoryPage(BaseHandler):
  """Page handler for the wiki pages history page

  Page handler to handle the requests for the history page of the wiki pages.
  Inherits common functionality from BaseHandler.
  """
  def get(self, name):
    """Handles the get requests for the history pages

    If the requested page doesn't exist, the user will be redirected to the root
    url.
    """
    name = utils.checkPage(name)
    versions = Page.getNameAll(name)
    
    if not versions:
      self.redirect('/')
      return None
    
    params = { 'versions': versions, 'page': versions[0] }
    self.render(settings.TEMPLATE_FILENAME['history'], **params)

class SearchPage(BaseHandler):
  """Page handler for the wiki search page

  Page handler to handle the requests for the search page.
  Inherits common functionality from BaseHandler.
  """
  def get(self):
    """Handles the get requests for the search page

    If no query is present an empty list of results will be passed to jinja.
    """
    query = self.request.get('q').strip()
    results = []
    qearch_query_first = ''
    if query:
      results = utils.searchQuery(query)
      search_query_first = query.split()[0]

    params = { 'results': results, 'search_query': query,
               'search_query_first': search_query_first }
    self.render(settings.TEMPLATE_FILENAME['search'], **params)