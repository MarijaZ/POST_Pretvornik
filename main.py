#!/usr/bin/env python
import os
import jinja2
import webapp2
from math import fsum


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        self.render_template("hello.html")

class PretvornikHandler(BaseHandler):
    def post(self):

        stevilo = self.request.get("vnos3")
        prva_enota = self.request.get("vnos1")
        druga_enota = self.request.get("vnos2")
        rezultat = 0

        if druga_enota == "centimeter" or "cm":
            rezultat = float(stevilo) * 0.01
        elif druga_enota == "meter" or "m":
            rezultat = float(stevilo) / 100

        params = {"vnos3": stevilo, "vnos2":druga_enota, "vnos1": prva_enota, "rezultat": rezultat}

        self.render_template("pretvornik.html", params)




app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/pretvornik', PretvornikHandler)
], debug=True)
# POST_Pretvornik
