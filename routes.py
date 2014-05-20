# -*- coding: utf-8 -*-
import webapp2, handlers

PAGE_RE = r'(/?(?:[a-zA-Z0-9_-]+/?)*)'
# URL mappings
ROUTE_LIST = [
  webapp2.Route(r'/signup', handler=handlers.SignupPage, name='signup'),
  webapp2.Route(r'/login', handler=handlers.LoginPage, name='login'),
  webapp2.Route(r'/logout', handler=handlers.LogoutPage, name='logout'),
  webapp2.Route(r'/_edit<name:/(?:[a-zA-Z0-9_-]+/?)*>', handler=handlers.EditPage, name='edit'),
  webapp2.Route(r'/_history<name:/(?:[a-zA-Z0-9_-]+/?)*>', handler=handlers.HistoryPage, name='history'),
  webapp2.Route(r'<name:/(?:[a-zA-Z0-9_-]+/?)*>', handler=handlers.WikiPage, name='wiki')
  ]