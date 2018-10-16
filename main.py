from flask import Flask, request, redirect, render_template, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:pass@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(600))

    def __init__(self, title, body):
        self.title = title
        self.body = body

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/', methods=['POST', 'GET'])
def index():
    title = 'Build-a-blog'
    if request.method == 'POST':
        return render_template('blog.html')
    if request.method == 'GET':
        titles = Blog.query.all()
        return render_template('blog.html', titles = titles)
        
@app.route('/blog', methods=['POST','GET'])
def blog():
    title = 'Build-a-blog'
    if request.method == 'POST':
        return render_template('blog.html')
    if request.method == 'GET':

        titles = Blog.query.all()
        return render_template('blog.html', titles = titles)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        
        title = request.form['title']
        post = request.form['post']
        
        error_title = False
        error_post = False

        if title == '':
            error_title = True
            print(error_title)
            return render_template('newpost.html', error_title = error_title, error_post = error_post, 
            title = title, post = post)
        if post == '':
            print(error_post)
            error_post = True
            return render_template('newpost.html', error_title = error_title, error_post = error_post, 
            title = title, post = post)

        new_post = Blog(title, post)
        db.session.add(new_post)
        db.session.commit()

        current_id = new_post.id
        return redirect('/post?id={0}'.format(current_id))
        
        titles = Blog.query.all()
        
        return render_template('blog.html', titles = titles)
        
    if request.method == 'GET':
        return render_template('newpost.html')

@app.route('/post', methods = ['POST', 'GET'])
def see_post():
    
   # if request.method == 'POST'
  #      pass
    print('----------------------')
    if request.method == 'GET':
        current_id = request.args.get('id')
        post = Blog.query.get(current_id)
        return render_template('post.html', post = post)

@app.route('/register', methods = ['POST', 'GET'])
def register():

    print('-------------------------------')
    if request.method == 'GET':
        print('-------------------------------')
        return render_template('register.html')

    if request.method == 'POST':
        return render_template('register.html')

if __name__ == '__main__':
    app.run()
