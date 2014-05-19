# -*- coding: utf-8 -*-
from base import BaseHandler
import settings

class HomePage(BaseHandler):
  def get(self):
    params = {}
    self.render('home.html', **params)