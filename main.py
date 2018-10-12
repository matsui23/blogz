from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(600))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/', methods=['POST', 'GET'])
def index():
    title = 'Build-a-blog'
    if request.method == 'POST':
        return render_template('blog.html')
    if request.method == 'GET':
        return render_template('base.html', title = title)
    #tasks = Task.query.filter_by(completed=False).all()

@app.route('/blog', methods=['POST','GET'])
def blog():
    title = 'Build-a-blog'
    if request.method == 'POST':
        return render_template('blog.html')
    if request.method == 'GET':
        return render_template('base.html')

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'POST':
        
        title = request.form['title']
        post = request.form['post']
        new_post = Blog(title, post)
        db.session.add(new_post)
        db.session.commit()
        
        titles = Blog.query.all()
        
        return render_template('blog.html', titles = titles)

    if request.method == 'GET':
        return render_template('newpost.html')

if __name__ == '__main__':
    app.run()