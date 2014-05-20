# -*- coding: utf-8 -*-
import logging
import utils

from google.appengine.ext import ndb

class User(ndb.Model):
  """ Some text here """
  name = ndb.StringProperty(required=True)
  pw = ndb.StringProperty(required=True)
  email = ndb.StringProperty()

  @staticmethod
  def get_key(group='default'):
    return ndb.Key('users', group)

  @classmethod
  def get_id(cls, uid):
    return User.get_by_id(long(uid), parent=User.get_key())

  @classmethod
  def get_name(cls, name):
    u = User.query().filter(User.name == name).fetch(1)
    return u[0] if u else None

  @classmethod
  def register(cls, name, pw, email=None):
    pw = utils.gen_pw_hash(name, pw)
    return cls(parent=User.get_key(), name=name, pw=pw, email=email)

  @classmethod
  def login(cls, name, pw):
    u = User.get_name(name)
    return u if u and u.pw == utils.gen_pw_hash(name, pw, u.pw.split('|')[0]) else None