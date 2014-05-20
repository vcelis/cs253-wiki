# -*- coding: utf-8 -*-
import logging
import webapp2
import jinja2
import settings
import utils
from webapp2 import uri_for

from models import User

from google.appengine.api import memcache

class BaseHandler(webapp2.RequestHandler):
  """
    Extension of the normal RequestHandler

    - self.write() provides a quick way to write out plain text
    - self.render() provides a quick way to render templates with
      template variables
    - self.render_json() provides a quick way to respond with JSON
    - add_settings_values(raw) adds the settings object
  """
  JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(settings.TEMPLATE_PATH),
    autoescape=settings.TEMPLATE_ESCAPE,
    bytecode_cache=jinja2.MemcachedBytecodeCache(memcache, prefix='jinja2/bytecode/', timeout=settings.JINJA2_BYTECODE_TIMEOUT)
  )

  def write(self, data):
    self.response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    self.response.out.write(data)

  def render(self, template, **params):
    self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
    self.response.out.write(self.JINJA_ENV.get_template(template).render(self.add_misc_values(params)))

  def render_json(self, obj):
    self.response.headers.content_type = 'application/json'
    self.response.write(json.dump(obj))

  def add_misc_values(self, raw):
    raw['settings'] = settings
    raw['user'] = self.user
    return raw

  def set_cookie(self, name, value):
    self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, value))

  def del_cookie(self, name):
    self.response.headers.add_header('Set-Cookie', '%s=; Path=/' % name)

  def check_login(self):
    uid = self.request.cookies.get('uid')
    if uid:
      check = utils.check_cookie(uid)
      if check:
        u = User.get_id(uid.split('|')[0])
        return u
      else:
        self.del_cookie('uid')
        return None

  def restricted_area(self, reverse=False):
    if reverse:
      self.del_cookie('uid')
      self.user = None
    else:
      if not self.user:
        self.redirect(uri_for('signup'))

  def __init__(self, request, response):
    self.initialize(request, response)
    self.user = self.check_login()

class FormHandler():
  """
    Extension for page handlers who need form validation
  """
  def validate_signup(self, **raw):
    error, params = False, {'username': raw['username'], 'email': raw['email']}
    if not utils.validate_username(raw['username']):
      params['error_username'] = 'That\'s not a valid username.'
      error = True
    if not utils.validate_password(raw['password']):
      params['error_password'] = 'That wasn\'t a valid password.'
      error = True
    elif raw['password'] != raw['verify']:
      params['error_verify'] = 'Your passwords didn\'t match.'
      error = True
    if not utils.validate_email(raw['email']):
      params['error_email'] =  'That\'s not a valid email.'
      error = True
    return (error, params)

  def validate_login(self, **raw):
    error, params = False, {'username': raw['username'], 'password': raw['password']}
    if not utils.validate_username(raw['username']):
      params['error_username'] = 'That\'s not a valid username.'
      error = True
    if not raw['password']:
      params['error_password'] = 'You didn\'t enter any password.'
      error = True
    return (error, params)