import webapp2
import jinja2
import os
from google.appengine.ext import db

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

def get_posts(limits, offsets):
    #return list with at most limit posts
    limits=int(limits)
    offsets = int(offsets)
    postquery = 0
    return postquery

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

class BlogView(Handler):

    def get(self):
        query_text = 'SELECT * FROM BlogPost ORDER BY created DESC LIMIT {0} OFFSET {1}'.format(5, 0)
        blogs = db.GqlQuery(query_text)
        self.render('blog.html', blogs=blogs)

class NewPost(Handler):
    #render with error, preserve content if error
    def render_form(self, title='', blog_post='', error=''):
        self.render("newpost.html" , title=title, blog_post = blog_post, error=error)

    def get(self):
        self.render_form()

    def post(self):
        #get title and post values
        title = self.request.get('title')
        blog_post = self.request.get('blog_post')

        #error handling
        if title and blog_post:
            post = BlogPost(title = title, blog_post = blog_post)
            post.put()
            #redirect to blog permalink page
            post_id = '/blog/'+str(post.key().id())
            self.redirect(post_id)
        else:
            error = 'Please provide both title and content'
            #preserve content, re-render with error message
            self.render_form(title, blog_post, error)

class ViewPostHandler(Handler):
    def get(self, id):
        post = BlogPost.get_by_id( int(id) )
        if post:
            self.render('post.html',title=post.title, blog_post = post.blog_post, error='')
        else:
            error = "There is no post with that ID"
            self.render('post.html', error = error)


app = webapp2.WSGIApplication([
    ('/blog', BlogView),
    ('/newpost', NewPost),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
