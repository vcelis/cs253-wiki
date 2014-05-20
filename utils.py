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
import re
import random
import hashlib
import hmac

import utils
import settings

from string import letters

def validateUsername(username):
  """Returns True if the username is not empty AND matched the regex"""
  return username and settings.RE_USERNAME.match(username)

def validatePassword(password):
  """Returns True if the password is not empty AND matched the regex"""
  return password and settings.RE_PASSWORD.match(password)

def validateEmail(email):
  """Returns True if the email is empty OR matched the regex"""
  return not email or settings.RE_EMAIL.match(email)

def validateLogin(**raw):
  """Validates the login form input

  Validates the input from the login form using the regex defined in settings.py
  
  Args:
    **raw: Collects all the named arguments

  Returns:
    A tuple containing:
      - Boolean: Whether there was an error or not
      - dict(): Containing the original params and the generated error params
  """
  error, params = False, {'username': raw['username'], 'password': raw['password']}
  if not utils.validateUsername(raw['username']):
    params['error_username'] = settings.RE_USERNAME_FAIL
    error = True
  if not raw['password']:
    params['error_password'] = settings.RE_PASSWORD_EMPTY
    error = True
  return (error, params)

def validateSignup(**raw):
  error, params = False, {'username': raw['username'], 'email': raw['email']}
  if not utils.validateUsername(raw['username']):
    params['error_username'] = settings.RE_USERNAME_FAIL
    error = True
  if not utils.validatePassword(raw['password']):
    params['error_password'] = settings.RE_PASSWORD_FAIL
    error = True
  elif raw['password'] != raw['verify']:
    params['error_verify'] = RE_PASSWORD_MATCH
    error = True
  if not utils.validateEmail(raw['email']):
    params['error_email'] =  settings.RE_EMAIL_FAIL
    error = True
  return (error, params)

def genCookie(uid):
  return '%s|%s' % (uid, hmac.new(settings.COOKIE_SALT, str(uid)).hexdigest())

def checkCookie(raw):
  uid = raw.split('|')[0]
  return uid if raw == genCookie(uid) else None

def genSalt(length=5):
  return ''.join(random.choice(string.letters) for x in xrange(length))

def genPwHash(name, pw, salt=None):
  salt = salt if salt else genSalt()
  return '%s|%s' % (salt, hashlib.sha256(name+pw+salt).hexdigest())

def checkPage(page):
  return 'home' if str(page) in settings.RESERVED_PAGES else page[1:]