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

from google.appengine.ext import ndb

class User(ndb.Model):
  """Models the User entity for the datastore

  Models the User entity for storage in the datastore. It has a few @classmethod
  's to handle user registration and authentication.

  Attributes:
    name: A string containing the username
    pw: A string containing the hashed pw
    email: A string containing the email address
  """
  name = ndb.StringProperty(required=True)
  pw = ndb.StringProperty(required=True)
  email = ndb.StringProperty()

  @staticmethod
  def getKey(group='default'):
    """Returns the key used for the model"""
    return ndb.Key('users', group)

  @classmethod
  def getId(cls, uid):
    """"Returns the entity instance for a given uid"""
    return User.get_by_id(long(uid), parent=User.getKey())

  @classmethod
  def getName(cls, name):
    """Returns the entity instance for a given username if exists"""
    u = User.query(ancestor=User.getKey()).filter(User.name == name).fetch(1)
    return u[0] if u else None

  @classmethod
  def register(cls, name, pw, email=None):
    """Returns a new entity instance for the given attributes"""
    pw = utils.genPwHash(name, pw)
    return cls(parent=User.getKey(), name=name, pw=pw, email=email)

  @classmethod
  def login(cls, name, pw):
    """Returns the entity instance if the provided username and password match"""
    u = User.getName(name)
    return u if u and u.pw == utils.genPwHash(name, pw, u.pw.split('|')[0]) else None