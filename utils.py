# -*- coding: utf-8 -*-
import settings
import re
import random, hashlib, hmac, string

def validate_username(username):
  return username and settings.RE_USERNAME.match(username)

def validate_password(password):
  return password and settings.RE_PASSWORD.match(password)

def validate_email(email):
  return not email or settings.RE_EMAIL.match(email)

def gen_cookie(uid):
  return '%s|%s' % (uid, hmac.new(settings.COOKIE_SALT, str(uid)).hexdigest())

def check_cookie(raw):
  uid = raw.split('|')[0]
  return uid if raw == gen_cookie(uid) else None

def gen_salt(length=5):
  return ''.join(random.choice(string.letters) for x in xrange(length))

def gen_pw_hash(name, pw, salt=None):
  salt = salt if salt else gen_salt()
  return '%s|%s' % (salt, hashlib.sha256(name+pw+salt).hexdigest())

def check_page(page):
  return 'home' if str(page) in settings.RESERVED_PAGES else page[1:]