# -*- coding: utf-8 -*-
import logging
import webapp2
import jinja2
import settings

from google.appengine.api import memcache

JINJA_ENV = jinja2.Environment(
  loader=jinja2.FileSystemLoader(settings.TEMPLATE_PATH),
  autoescape=settings.TEMPLATE_ESCAPE,
  bytecode_cache=jinja2.MemcachedBytecodeCache(memcache, prefix='jinja2/bytecode/', timeout=settings.JINJA2_BYTECODE_TIMEOUT)
)

class BaseHandler(webapp2.RequestHandler):
  """
    Extension of the normal RequestHandler

    - self.write() provides a quick way to write out plain text
    - self.render() provides a quick way to render templates with
      template variables
    - self.render_json() provides a quick way to respond with JSON
  """
  def write(self, data):
    """ Provides a quick way to write out plain text """
    self.response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    self.response.out.write(data)

  def render(self, template, **params):
    """ Provides a quick way to render templates with variables """
    self.response.headers['Content-Type'] = 'text/html; charset=utf-8'
    self.response.out.write(JINJA_ENV.get_template(template).render(BaseHandler.add_settings_values(params)))

  def render_json(self, obj):
    """ Provides a quick way to respond with JSON """
    self.response.headers.content_type = 'application/json'
    self.response.write(json.dump(obj))

  @staticmethod
  def add_settings_values(raw):
    raw['settings'] = settings
    return raw