from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.inspiration import Inspiration
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['post'])
def register():
    
    if not User.val_email(request.form):
        return redirect('/')
    data ={
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.remember(data)
    session['user_id'] = id
    
    return redirect('/dashboard')

@app.route('/login', methods=['post'])
def login():
    user = User.get_email(request.form)
    if not user:
        flash('Invalid Credentials', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid Credentials', 'login')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id'not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html',user=User.get_id(data), inspiration=Inspiration.connect_viewer_to_post(), user_likes=Inspiration.all_user_liked_inspirations(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')