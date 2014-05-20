# -*- coding: utf-8 -*-
import logging

from google.appengine.ext import ndb

class Page(ndb.Model):
  name = ndb.StringProperty(required=True)
  content = ndb.TextProperty(required=True)
  created = ndb.DateTimeProperty(auto_now_add=True)
  version = ndb.IntegerProperty(required=True)
  author = ndb.StringProperty(required=True)

  @staticmethod
  def get_key(group='default'):
    return ndb.Key('pages', group)

  @classmethod
  def get_name(cls, name):
    p = Page.query().filter(Page.name == name).fetch(1)
    return p[0] if p else None