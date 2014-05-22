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

from datetime import datetime

from google.appengine.ext import ndb

class Page(ndb.Model):
  """Models the Page entity for the datastore

  Models the Page entity for storage in the datastore.

  Attributes:
    name: A string containing the name of the page
    content: A text property containing the content of the page
    created: A Datetime object containing the datetime of creation
    version: An Integer containing the version number of the page
    author: A string containing the version authors username
  """
  name = ndb.StringProperty(required=True)
  content = ndb.TextProperty(required=True)
  created = ndb.DateTimeProperty(auto_now_add=True)
  version = ndb.IntegerProperty(required=True)
  author = ndb.StringProperty(required=True)

  @staticmethod
  def getKey(group='default'):
    """Returns the key used for the model"""
    return ndb.Key('pages', group)

  @classmethod
  def getName(cls, name, version=0):
    """Returns the entity instance for a given page name and version if exists"""
    query = Page.query(ancestor=Page.getKey())
    query = query.filter(Page.name == name)
    
    if version:
      query = query.filter(Page.version == version)
    
    page = query.order(-Page.version).fetch(1)
    return page[0] if page else None

  @classmethod
  def getNameAll(cls, name):
    """Returns all the version of a given pagename in descending order"""
    query = Page.query(ancestor=Page.getKey())
    query = query.filter(Page.name == name).order(-Page.version)
    return query.fetch()

  @classmethod
  def getLast(cls, i):
    """Returns the last i edited pages"""
    result = []
    tmp = []
    query = Page.query(ancestor=Page.getKey())
    query = query.order(-Page.created)
    
    for r in query.fetch(i):
      if r.name not in tmp:
        result.append(r)
        tmp.append(r.name)

    return result

  @classmethod
  def createPage(cls, name, content='', author='admin'):
    """Returns a new entity instance for the given attributes

      The version will be computed by counting the total number of entities for
      the given page and adding 1. This is not very scaleable.
    """
    version = len(Page.query(ancestor=Page.getKey()).filter(Page.name == name).fetch())+1
    created = datetime.utcnow()
    
    return cls(parent=Page.getKey(), name=name, content=content,
               version=version, created=created, author=author)