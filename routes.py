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

import webapp2
import handlers

ROUTE_LIST = [
  webapp2.Route(r'/signup', handler=handlers.SignupPage, name='signup'),
  webapp2.Route(r'/login', handler=handlers.LoginPage, name='login'),
  webapp2.Route(r'/logout', handler=handlers.LogoutPage, name='logout'),
  webapp2.Route(r'/_edit<name:/(?:[a-zA-Z0-9_-]+/?)*>',
                handler=handlers.EditPage, name='edit'),
  webapp2.Route(r'/_history<name:/(?:[a-zA-Z0-9_-]+/?)*>',
                handler=handlers.HistoryPage, name='history'),
  webapp2.Route(r'<name:/(?:[a-zA-Z0-9_-]+/?)*>',
                handler=handlers.WikiPage, name='wiki')
  ]