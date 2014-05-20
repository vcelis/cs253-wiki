# -*- coding: utf-8 -*-
import logging

from base import BaseHandler, FormHandler
from models import User
import settings, utils

class SignupPage(BaseHandler, FormHandler):
  def get(self):
    self.restricted_area(True)
    self.render('signup.html')

  def post(self):
    fields = ['username', 'password', 'verify', 'email']
    raw = { field: self.request.get(field) for field in fields }
    error, params = self.validate_signup(**raw)
    if error:
      self.render('signup.html', **params)
    else:
      if User.get_name(raw['username']):
        params['error_username'] = 'That username already exists.'
        self.render('signup.html', **params)
      else:
        u = User.register(raw['username'], raw['password'], raw['email'])
        u.put()
        self.set_cookie('uid', utils.gen_cookie(u.key.integer_id()))
        self.redirect('/')

class LoginPage(BaseHandler, FormHandler):
  def get(self):
    self.restricted_area(True)
    self.render('login.html')

  def post(self):
    fields = ['username', 'password']
    raw = { field: self.request.get(field) for field in fields }
    error, params = self.validate_login(**raw)
    if error:
      self.render('login.html', **params)
    else:
      u = User.login(raw['username'], raw['password'])
      if u:
        self.set_cookie('uid', utils.gen_cookie(u.key.integer_id()))
        self.redirect('/')
      else:
        params['error_login'] = 'Invalid username and/or password'
        self.render('login.html', **params)

class LogoutPage(BaseHandler):
  def get(self):
    self.del_cookie('uid')
    self.redirect('/')