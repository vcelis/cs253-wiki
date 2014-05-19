# -*- coding: utf-8 -*-
import webapp2
import settings
import routes

app = webapp2.WSGIApplication(routes.ROUTE_LIST, debug=settings.FORCE_DEV)