from flask import Flask, request, redirect, render_template, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:pass@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'secretkey'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(600))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    posts = db.relationship('Blog', backref = 'owner')
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    print('()()()()()()()()()()()()()()()')
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

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
        current_user = session['email']
        print('================')
        print(session['email'])
        print('================')
        titles = Blog.query.all()
        #titles_id = Blog.query.get(id)
        print('++++++++++++++++++++++++++++')
        users = User.query.all()
        #print(titles_id)
        print(users)

        print('++++++++++++++++++++++++++++')

        
        return render_template('blog.html', titles = titles, current_user = current_user, users = users)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    owner = User.query.filter_by(username = session['email']).first()
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

        new_post = Blog(title, post, owner)
        db.session.add(new_post)
        db.session.commit()

        current_id = new_post.id
        user_id = new_post.owner_id
        return redirect('/post?id={0}&user_id={1}'.format(current_id, user_id))
        
        titles = Blog.query.all()
        
        return render_template('blog.html', titles = titles, user_id = user_id)
        
    if request.method == 'GET':
        return render_template('newpost.html')

@app.route('/post', methods = ['POST', 'GET'])
def see_post():
    
   # if request.method == 'POST'
  #      pass
    print('----------------------')
    if request.method == 'GET':
        current_id = request.args.get('id')
        user_id = request.args.get('user_id')
        post = Blog.query.get(current_id)
        user = User.query.get(user_id)
        # need to query for the id to pass to the html
        return render_template('post.html', post = post, user = user)

@app.route('/register', methods = ['POST', 'GET'])
def register():

    print('-------------------------------')
    if request.method == 'GET':
        print('-------------------------------')
        return render_template('register.html')

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        duplicate_user = False
        error_email = False
        error_password = False
        error_pass_match = False

        existing_user = User.query.filter_by(username = email).first()

        if existing_user:
            duplicate_user = True
            return render_template('register.html', email = email, duplicate_user = duplicate_user, error_email = error_email, error_password = error_password, error_pass_match = error_pass_match)

        if email =='' and password == '' and verify == '':
            error_email = True
            error_password = True
            return render_template('register.html', email = email, duplicate_user = duplicate_user, error_email = error_email, error_password = error_password, error_pass_match = error_pass_match)
        
        if password == '' or verify =='':
            error_password = True
            return render_template('register.html', email = email, duplicate_user = duplicate_user, error_email = error_email, error_password = error_password, error_pass_match = error_pass_match)
        
        if password != verify:
            error_pass_match = True
            return render_template('register.html', email = email, duplicate_user = duplicate_user, error_email = error_email, error_password = error_password, error_pass_match = error_pass_match)

        if not existing_user and password == verify and password:

            new_user  = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            
            session['email'] = email

            print('-----------------------')
            return redirect('/blog')
        else:
            print('***********************')
            
            return redirect('/register')

        

@app.route('/login', methods = ['POST', 'GET'])
def login():

    print('-------------------------------')
    if request.method == 'GET':
        print('-------------------------------')
        return render_template('login.html')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        error_email = False
        error_password = False
        error_email_empty = False
        error_password_empty = False
        
        user = User.query.filter_by(username = email).first()

        if user and user.password == password:
           
            session['email'] = email
            return redirect('/newpost')

        if email == '' and password == '':

            error_email_empty = True
            error_password_empty = True

            return render_template('login.html', email = email, error_email = error_email, error_password = error_password, error_email_empty = error_email_empty, error_password_empty = error_password_empty)

        if not user:

            error_email = True
            return render_template('login.html', email = email, error_email = error_email, error_password = error_password, error_email_empty = error_email_empty, error_password_empty = error_password_empty)

        if user.password != password:

            error_password = True
            return render_template('login.html', email = email, error_email = error_email, error_password = error_password, error_email_empty = error_email_empty, error_password_empty = error_password_empty)


        return render_template('login.html')

@app.route('/logout')
def logout():
    print('----------------------------')
    print(session['email'])
    print('----------------------------')
    del session['email']
    return redirect('/')

@app.route('/userlist', methods = ['POST', 'GET'])
def display_users():
    if request.method == 'GET':
        users = User.query.all()

        return render_template('user_list.html', users = users)

@app.route('/userposts', methods = ['POST', 'GET'])
def display_users_posts():
    if request.method == 'GET':
        owner_id = request.args.get('id')
        print('**********************')
        print(owner_id)
        print('**********************')
        posts = Blog.query.filter_by(owner_id = owner_id)
        
        print('[][][][[][][][][]')
        print(posts)
        print('[][][][[][][][][]')

        return render_template('users_posts.html', posts = posts)

if __name__ == '__main__':
    app.run()
