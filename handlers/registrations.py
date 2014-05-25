#!/usr/bin/env python
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

import settings
import utils

from base import BaseHandler
from models import User

class SignupPage(BaseHandler):
  """Page handler for the signup page

  Page handler to handle the requests for the signup page.
  Inherits common functionality from BaseHandler.
  """
  def get(self):
    """Handles the get requests for signup page

    The user will get logged out when authentication succeeds and the requested
    page will be displayed.
    """
    self.restrictedArea(True)
    self.render(settings.TEMPLATE_FILENAME['signup'])

  def post(self):
    """Handles the post requests for the signup page

    The user will get logged out when authentication succeeds and the request
    will get processed.
    """
    self.restrictedArea(True)
    fields = [ 'username', 'password', 'verify', 'email' ]
    raw = { field: self.request.get(field) for field in fields }
    error, params = utils.validateSignup(**raw)
    
    if error:
      self.render(settings.TEMPLATE_FILENAME['signup'], **params)
    else:
      if User.getName(raw['username']):
        params['error_username'] = 'That username already exists.'
        self.render(settings.TEMPLATE_FILENAME['signup'], **params)
      else:
        u = User.register(raw['username'], raw['password'], raw['email'])
        u.put()
        self.setCookie('uid', utils.genCookie(u.key.integer_id()))
        self.redirect('/')

class LoginPage(BaseHandler):
  """Page handler for the login page

  Page handler to handle the requests for the login page.
  Inherits common functionality from BaseHandler.
  """
  def get(self):
    """Handles the get requests for login page

    The user will get logged out when authentication succeeds and the requested
    page will be displayed.
    """
    self.restrictedArea(True)
    self.render(settings.TEMPLATE_FILENAME['login'])

  def post(self):
    """Handles the post requests for the login page

    The user will get logged out when authentication succeeds and the request
    will get processed.
    """
    self.restrictedArea(True)
    fields = [ 'username', 'password' ]
    raw = { field: self.request.get(field) for field in fields }
    error, params = utils.validateLogin(**raw)
    
    if error:
      self.render(settings.TEMPLATE_FILENAME['login'], **params)
    else:
      u = User.login(raw['username'], raw['password'])
      if u:
        self.setCookie('uid', utils.genCookie(u.key.integer_id()))
        self.redirect('/')
      else:
        params['error_login'] = 'Invalid username and/or password'
        self.render(settings.TEMPLATE_FILENAME['login'], **params)

class LogoutPage(BaseHandler):
  """Page handler for the logout page

  Page handler to handle the requests for the logout page.
  Inherits common functionality from BaseHandler.
  """
  def get(self):
    """Handles the get requests for logout page

    Cookie will be deleted and redirected to the root url.
    """
    self.delCookie('uid')
    self.redirect('/')