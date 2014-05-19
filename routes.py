# -*- coding: utf-8 -*-
import webapp2, handlers

# URL mappings
ROUTE_LIST = [
  webapp2.Route(r'/', handler=handlers.HomePage, name='home'),
  ]