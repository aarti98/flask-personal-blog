from flask import (
    render_template, redirect, flash, url_for, abort, request
    )
from flask_login import login_required, current_user

from . import home
from app import db
from app.forms import CommentForm, BlogForm
from app.models import Blog, Comment, User

@home.route('/')
def index():
    blogs = Blog.query.order_by(Blog.timestamp.desc())
    return render_template('home/index.html', title='Home', blogs=blogs)

@home.route('/about-me')
def about_me():
    return render_template('home/about_me.html', title='About Me')

@home.route('/portfolio')
def portfolio():
    return render_template('home/portfolio.html', title='Portfolio')

@home.route('/hire-me')
def hire_me():
    return render_template('home/hire_me.html', title='Hire Me')


@home.route('/forms', methods=['GET', 'POST'])
def forms():
    form = CommentForm()
    if form.validate_on_submit():
        user = User(name = form.name.data, email = form.email.data)
        post = Comment(body = form.comment.data, author = user)
        db.session.add(user)
        db.session.add(post)
        db.session.commit()
        flash('Your comment is now live!')
        return redirect(url_for('forms'))
    posts = Comment.query.order_by(Comment.timestamp.desc())
    return render_template('home/forms.html', title='Forms', form=form, posts=posts)

@home.route('/blogs/<int:pk>')
def view_blog(pk):
    blog = Blog.query.get_or_404(pk)
    posts = Comment.query.order_by(Comment.timestamp.desc())
    return render_template('home/view_blog.html', blog=blog, posts=posts) 


# add admin dashboard view
@home.route('/admin/dashboard')
@login_required
def admin_dashboard():

    blogs = Blog.query.order_by(Blog.timestamp.desc())
    return render_template('home/admin_dashboard.html', title="Dashboard", blogs=blogs)