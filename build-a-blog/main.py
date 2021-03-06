#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2
import cgi
from google.appengine.ext import db
#import sqlite3

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

#TemplateEngine named mainHandler1
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


## inserted Limit 5 11/12/2016
class BlogHandler(Handler):
    def render_blogpost(self):
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC LIMIT 5")

        self.render("blogpost.html",   arts = arts)
#title=title,
#art=art,
    def get(self):
        self.render_blogpost()

class NewPost(Handler):
    def render_front(self, title="", art="", error=""):

        self.render("frontpage.html", title=title, art=art, error=error)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:

            a = Art(title = title, art = art)
            a.put()

            self.redirect("/blog/%s" % str(a.key().id()))
        else:
            error = "Please add a Title and some Content"
            self.render_front(error = error, title = title, art = art)

class ViewPostHandler(Handler):
    def render_viewPost(self,id):

        #arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
        arts = Art.get_by_id (int(id),parent=None)
        #arts = db.GqlQuery("SELECT * FROM Art WHERE id = :id ", id)
        self.render("singleblogpost.html",   arts = arts)


    def get(self,id):
        self.render_viewPost(id)


class MainHandler(Handler):
    def render_front(self):
        #arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC")
        self.render("blogpost.html")

    def get(self):
        self.render_front()


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/blog', BlogHandler) ,
    webapp2.Route('/blog/newpost', NewPost),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)

], debug=True)
#('/blog/<id:\d+>', ViewPostHandler)
