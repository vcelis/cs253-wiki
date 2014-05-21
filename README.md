<h1>CS253-Wiki</h1>
<p>Welcome to my final exam submission for the Udacity CS253: Web Development course.</p>
<p><a href="http://uda-cs253-wiki.appspot.com/">Live Demo</a></p>

<h2>What makes this Wiki app Amazing?</h2>
<p>Every aspect of the course is implemented in this project and even the relative new full text search API.</p>
<p>The code follows the <a href="http://google-styleguide.googlecode.com/svn/trunk/pyguide.html">Google Python style guide</a>.</p>

<h2>Useful links</h2>
<ul>
  <li><a href="https://www.udacity.com/course/cs253">Udacity CS253: Web Development course overview</a></li>
  <li><a href="https://www.youtube.com/watch?v=bdes6p2h_YU">Final exam instructions</a></li>
  <li><a href="https://www.youtube.com/watch?v=bWnxTIT0vd8">Bonus question instructions</a></li>
  <li><a href="http://google-styleguide.googlecode.com/svn/trunk/pyguide.html">Google Python style guide</a></li>
  <li><a href="https://github.com/vcelis/gae-boilerplate">My own custom GAE boilerplate repository</a></li>
</ul>

<h2>Functions and features</h2>
<ul>
  <li>Authentication (Sign In, Sign Out, Sign Up, Validation)</li>
  <li>Server side form validation</li>
  <li>Wiki module (Add, Edit)</li>
  <li>Wiki page history system</li>
  <li>Full text search over all pages</li>
  <li>Auto memcached responsive design templates</li>
  <li>Central configuration file for easy customization</li>
  <li>Strong consistent query results</li>
</ul>

<h2>Backend Technologies used</h2>
<ul>
  <li><a href="https://www.python.org/">Python 2.7</a</li>
  <li><a href="https://developers.google.com/appengine/docs/python/ndb/">Google NDB datastore API</a></li>
  <li><a href="https://developers.google.com/appengine/docs/python/search/">Google full text search API</a></li>
  <li><a href="https://developers.google.com/appengine/docs/python/memcache/">Google memcache API</a></li>
  <li><a href="http://jinja.pocoo.org/docs/">Jinja2</a></li>
  <li><a href="http://webapp-improved.appspot.com/">webapp2 python web framework</a></li>
  <ul>
    <li><a href="http://webapp-improved.appspot.com/api/webapp2_extras/routes.html">webapp2_routes</a></li>
  </ul>
</ul>

<h2>Front-end Technologies</h2>
<ul>
  <li><a href="http://html5boilerplate.com/">HTML5 Boilerplate</a></li>
  <li><a href="http://getbootstrap.com/">Twitter Bootstrap</a></li>
  <li><a href="http://jquery.com/">JQuery</a></li>
  <li><a href="https://code.google.com/p/html5shiv/">HTML5 shiv</a></li>
  <li><a href="http://fortawesome.github.io/Font-Awesome/">Font Awesome</a></li>
  <li><a href="http://www.tinymce.com/">TinyMCE WYSIWYG editor</a></li>
</ul>

<h2>Caching</h2>
<p>The NDB datastore API handles model query caching automatically using memache.</p>
<p>The jinja2 environment is configured to use memcache to cache the html requests.</p>

<h2>Security</h2>
<h4>Passwords</h4>
<p>Passwords are hashed by an unique salt combined with the users info with the sha256 algorithm.</p>

<h4>Authentication</h4>
<p>As a form of session authentication a cookie is used with the users uid that matches the id of the users datastore entity. The cookie is of the form UID|HASH where hash is a combination of a common salt and the uid using the hmac algorithm.</p>
<p>This is a part where the project should improve to increase session security</p>

<h2>License</h2>
<p>The MIT License (MIT)</p>

<p>Copyright (c) 2014 Vincent Celis</p>

<p>Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:</p>

<p>The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.</p>

<p>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.</p>