# -*- coding: utf-8 -*-
import logging

from google.appengine.ext import ndb
from google.appengine.api import memcache

class User(ndb.Model):
  """
    Storage for 
  """
  name = ndb.StringProperty(required=True)
  pw = ndb.StringProperty(required=True)
  email = ndb.StringProperty()