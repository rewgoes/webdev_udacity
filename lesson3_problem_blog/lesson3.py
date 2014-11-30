import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class MainPage(Handler):
    def render_front(self):
        posts = db.GqlQuery("select * from Post order by created desc")

        self.render("index.html", posts = posts)

    def get(self):
        self.render_front()


class NewPost(Handler):
    def render_front(self, subject="", content="", error=""):
        self.render("new.html", subject = subject, content = content, error = error)

    def get(self):
        self.render_front()

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            p = Post(subject = subject, content = content)
            p = p.put()

            self.redirect("/blog/%d" % p.id())
        else:
            error = "We need both a subject and content!"
            self.render_front(subject, content, error)


class PostHandler(Handler):
    def render_front(self, post):
        self.render("view.html", post = post)

    def get(self, id):
        post = Post.get_by_id(int(id))
        self.render_front(post)


routes = [(r'/blog', MainPage),
          (r'/blog/newpost', NewPost),
          (r'/blog/(\d+)', PostHandler),
          ]

app = webapp2.WSGIApplication(routes,debug=True)
