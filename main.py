import webapp2
import jinja2
import os
from google.appengine.ext import db

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):

    #convenience function to write whatever
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    #returns string of the template
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    #calls write on the render string function above
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class BlogPost(db.Model):
    title = db.StringProperty(required=True)
    blog_post = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
    #default values for render parameter is empty
    def render_front(self, title='', blog_post='', error=''):
        #create cursor from query
        blogs = db.GqlQuery('SELECT * FROM BlogPost ORDER BY created DESC LIMIT 5')
        self.render("base.html" , title=title, blog_post = blog_post, error = error, blogs=blogs)

    def get(self):
        self.render_front()

    def post(self):
        #get title and post values
        title = self.request.get('title')
        blog_post = self.request.get('blog_post')

        #error handling
        if title and blog_post:
            post = BlogPost(title = title, blog_post = blog_post)
            post.put()

            self.redirect('/')
        else:
            error = 'We need both title and post content'
            self.render_front(title, blog_post, error)

app = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)
