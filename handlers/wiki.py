# -*- coding: utf-8 -*-
import logging

from base import BaseHandler, FormHandler
from models import Page
from datetime import datetime
import utils

class WikiPage(BaseHandler):
  def get(self, name):
    name = utils.check_page(name)
    
    version = self.request.get('v')
    version = None if not version else int(version)

    if version:
      page = Page.query().filter(Page.name == name).filter(Page.version == version).fetch()
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

class HistoryPage(BaseHandler):
  def get(self, name):
    name = utils.check_page(name)
    page = Page.query().filter(Page.name == name).fetch()
    if not page:
      self.redirect('/')
    else:
      params = { 'page': page }
      self.render('history.html', **params)

class EditPage(BaseHandler, FormHandler):
  def get(self, name):
    self.restricted_area()
    name = utils.check_page(name)

    version = self.request.get('v')
    version = None if not version else int(version) 
    
    if version:
      page = Page.query().filter(Page.name == name).filter(Page.version == version).fetch()
      if not page:
        self.redirect('/_edit/%s' % name)
      else:
        params = { 'page': page[0] }
        self.render('edit.html', **params)
    else:
      page = Page.query().filter(Page.name == name).order(Page.version).fetch()
      if not page:
        page = Page(name=name, content='', version=1, created=datetime.utcnow(), author='admin')
      else:
        page = page[0]
      params = { 'page': page }
      self.render('edit.html', **params)

  def post(self, name):
    self.restricted_area()
    name = utils.check_page(name)

    content = self.request.get('content')
    version = len(Page.query().filter(Page.name == name).fetch())+1
    
    page = Page(name=name, content=content, version=version, created=datetime.utcnow(), author=self.user.name)
    page.put()
    self.redirect('/%s' % name)