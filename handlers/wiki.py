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

from datetime import datetime
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
    
    version = self.request.get('v')
    version = None if not version else int(version)

    if version:
      page = Page.query().filter(Page.name == name)
      page = page.filter(Page.version == version).fetch()
      if not page:
        self.redirect('/%s' % name)
      else:
        params = { 'page':  page[0] }
        self.render('wiki.html', **params)
    else:
      page = Page.query().filter(Page.name == name).order(-Page.version).fetch()
      if not page:
        self.redirect('/_edit/%s' % name)
      else:
        params = { 'page': page[0] }
        self.render('wiki.html', **params)

class EditPage(BaseHandler):
  """Page handler for the edit page of the individual wiki pages

  Page handler to handle the requests to edit the individual wiki pages.
  Inherits common functionality from BaseHandler.
  """
  def get(self, name):
    self.restrictedArea()
    name = utils.checkPage(name)

    version = self.request.get('v')
    version = None if not version else int(version) 
    
    if version:
      page = Page.query().filter(Page.name == name)
      page = page.filter(Page.version == version).fetch()
      if not page:
        self.redirect('/_edit/%s' % name)
      else:
        params = { 'page': page[0] }
        self.render('edit.html', **params)
    else:
      page = Page.query().filter(Page.name == name).order(Page.version).fetch()
      if not page:
        page = Page(name=name, content='', version=1, created=datetime.utcnow(),
                    author='admin')
      else:
        page = page[0]
      params = { 'page': page }
      self.render('edit.html', **params)

  def post(self, name):
    self.restrictedArea()
    name = utils.checkPage(name)

    content = self.request.get('content')
    version = len(Page.query().filter(Page.name == name).fetch())+1
    
    page = Page(name=name, content=content, version=version,
                created=datetime.utcnow(), author=self.user.name)
    page.put()
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
    page = Page.query().filter(Page.name == name).fetch()
    if not page:
      self.redirect('/')
    else:
      params = { 'page': page }
      self.render('history.html', **params)