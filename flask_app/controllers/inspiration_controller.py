from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models.inspiration import Inspiration
from flask_app.models.user import User


@app.route('/inspiration/add', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        return redirect('/')
    if not Inspiration.val_inspiration(request.form):
        return redirect('/dashboard')
    data={
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    Inspiration.save_this_post(data)
    print(data)
    return redirect('/dashboard')

@app.route('/inspiration/update/<int:id>')
def update_inspiration(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    user_data = {
        'id': session['user_id']
    }
    return render_template('update_inspiration.html', changeinspiration = Inspiration.get_by_id(data), user=User.get_id(user_data))

@app.route('/inspiration/edit/<int:id>', methods=['POST'])
def edit_this_inspiration(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Inspiration.val_inspiration(request.form):
        return redirect(f'/inspiration/update/{id}')
    data={
        'id': id,
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    Inspiration.update_current_inspiration(data)
    return redirect('/dashboard')


@app.route('/inspiration/display/<int:id>')
def display_inspiration(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    user_data = {
        'id': session['user_id']
    }
    chooseinspiration = Inspiration.get_inspiration_by_id_with_viewer(data)
    print(chooseinspiration)
    return render_template('show_inspiration.html', chooseinspiration = chooseinspiration, user = User.get_id(user_data), listuserslikes=Inspiration.get_one_inspiration(data))

@app.route('/like/<int:id>')
def addLike(id):
    data = {
        'inspiration_id': id,
        'user_id': session['user_id']
    }
    Inspiration.addLike(data)
    return redirect("/dashboard")

@app.route('/unlike/<int:id>')
def removeLike(id):
    data = {
        'inspiration_id': id,
        'user_id': session['user_id']
    }
    Inspiration.removeLike(data)
    return redirect("/dashboard")

@app.route('/inspiration/devour/<int:id>')
def remove_data(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    Inspiration.delete_all_likes(data)
    Inspiration.diminish(data)
    return redirect('/dashboard')
