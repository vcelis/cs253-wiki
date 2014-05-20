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
  def get(self):
    self.restrictedArea(True)
    self.render('signup.html')

  def post(self):
    fields = ['username', 'password', 'verify', 'email']
    raw = { field: self.request.get(field) for field in fields }
    error, params = utils.validateSignup(**raw)
    if error:
      self.render('signup.html', **params)
    else:
      if User.getName(raw['username']):
        params['error_username'] = 'That username already exists.'
        self.render('signup.html', **params)
      else:
        u = User.register(raw['username'], raw['password'], raw['email'])
        u.put()
        self.setCookie('uid', utils.genCookie(u.key.integer_id()))
        self.redirect('/')

class LoginPage(BaseHandler):
  def get(self):
    self.restrictedArea(True)
    self.render('login.html')

  def post(self):
    fields = ['username', 'password']
    raw = { field: self.request.get(field) for field in fields }
    error, params = utils.validateLogin(**raw)
    if error:
      self.render('login.html', **params)
    else:
      u = User.login(raw['username'], raw['password'])
      if u:
        self.setCookie('uid', utils.genCookie(u.key.integer_id()))
        self.redirect('/')
      else:
        params['error_login'] = 'Invalid username and/or password'
        self.render('login.html', **params)

class LogoutPage(BaseHandler):
  def get(self):
    self.delCookie('uid')
    self.redirect('/')