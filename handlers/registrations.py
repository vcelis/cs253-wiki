# -*- coding: utf-8 -*-
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