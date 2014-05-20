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

import webapp2
import jinja2

import settings
import utils
from models import User

from google.appengine.api import memcache
from webapp2 import uri_for


class BaseHandler(webapp2.RequestHandler):
  JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(settings.TEMPLATE_PATH),
    autoescape=settings.TEMPLATE_ESCAPE,
    bytecode_cache=jinja2.MemcachedBytecodeCache(memcache, 
        prefix='jinja2/bytecode/', timeout=settings.JINJA2_BYTECODE_TIMEOUT)
  )

  def render(self, template, **params):
    self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
    template = self.JINJA_ENV.get_template(template)
    self.response.out.write(template.render(self.addMiscValues(params)))

  def addMiscValues(self, raw):
    raw['settings'] = settings
    raw['user'] = self.user
    return raw

  def setCookie(self, name, value):
    self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, value))

  def delCookie(self, name):
    self.response.headers.add_header('Set-Cookie', '%s=; Path=/' % name)

  def checkLogin(self):
    uid = self.request.cookies.get('uid')
    if uid:
      check = utils.checkCookie(uid)
      if check:
        u = User.getId(uid.split('|')[0])
        return u
      else:
        self.delCookie('uid')
        return None

  def restrictedArea(self, reverse=False):
    if reverse:
      self.delCookie('uid')
      self.user = None
    else:
      if not self.user:
        self.redirect(uri_for('signup'))

  def __init__(self, request, response):
    self.initialize(request, response)
    self.user = self.checkLogin()