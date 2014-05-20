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

  Validates the input from the login form using the regex defined in settings
  
  Args:
    **raw: Collects all the named arguments

  Returns:
    A tuple containing:
      - Boolean: Whether there was an error or not
      - dict(): Containing the original params and the generated error params
  """
  error = False
  params = { 'username': raw['username'], 'password': raw['password'] }
  
  if not utils.validateUsername(raw['username']):
    params['error_username'] = settings.RE_USERNAME_FAIL
    error = True

  if not raw['password']:
    params['error_password'] = settings.RE_PASSWORD_EMPTY
    error = True

  return (error, params)

def validateSignup(**raw):
  """Validates the signup form input

  Validates the input from the signup form using the regex defined in settings

  Args:
    **raw: Collects all the named arguments

  Returns:
    A tuple containing:
      - Boolean: Whether there was an error or not
      - dict(): Containing the original params and the generated error params
  """
  error = False
  params = { 'username': raw['username'], 'email': raw['email'] }
  
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
  """Generates a cookie for a given uid

  Generates a cookie for the given uid containing the uid and a hashed 
  representation of the uid seperated by a pipe.

  The hash uses the string representation of the uid and a common salt specified
  in the settings module. 

  Args:
    uid: the uid to generate a cookie for

  Returns:
    - String: A string of the form UID|HASH
  """
  return '%s|%s' % (uid, hmac.new(settings.COOKIE_SALT, str(uid)).hexdigest())

def checkCookie(raw):
  """Checks a given raw cookie if it is a valid uid cookie

  Checks the raw input if it is compliant with our uid cookie layout by
  generating the expected cookie using the uid in the raw input and comparing
  this to the raw input.

  Args:
    raw: The raw cookie to check

  Returns:
    - boolean: None or False when the cookie check fails
               Integer representing the uid if the cookie checks out
  """
  uid = raw.split('|')[0]
  return uid if raw == genCookie(uid) else None

def genSalt(length=5):
  """Returns a string containing <length> random letters"""
  return ''.join(random.choice(string.letters) for x in xrange(length))

def genPwHash(name, pw, salt=None):
  """Generates the password hash to store in the datastore

  Generates a password hash to store in the database for the given username
  and password. An optional salt is provided to confirm the hash stored in the
  datastore.

  The sha256 hash uses the a concatenation of the username, password and salt.

  Args:
    name: Username for the hash
    pw:   Password for the hash
    salt: OPTIONAL, salt for the hash

  Returns:
    - String: A string of the form SALT|HASH
  """
  salt = salt if salt else genSalt()
  return '%s|%s' % (salt, hashlib.sha256(name+pw+salt).hexdigest())

def checkPage(page):
  """Modifies a given raw page (path) to a useable page name"""
  return 'home' if str(page) in settings.RESERVED_PAGES else page[1:]