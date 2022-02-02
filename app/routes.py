from flask import render_template, flash, redirect, request, url_for
from app import app, db
from app.forms import CommentForm, LoginForm, BlogForm, BlogUpdateForm, BlogDeleteForm
from app.models import User, Comment, Blog


@app.route('/')
@app.route('/home')
def home():
    blogs = Blog.query.order_by(Blog.timestamp.desc())
    return render_template('home.html', title='Home', blogs=blogs)

@app.route('/about-me')
def about_me():
    return render_template('about_me.html', title='About Me')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', title='Portfolio')

@app.route('/hire-me')
def hire_me():
    return render_template('hire_me.html', title='Hire Me')


@app.route('/forms', methods=['GET', 'POST'])
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
    return render_template('forms.html', title='Forms', form=form, posts=posts)

@app.route('/blogs/<int:pk>')
def view_blog(pk):
    blog = Blog.query.get_or_404(pk)
    posts = Comment.query.order_by(Comment.timestamp.desc())
    return render_template('view_blog.html', blog=blog, posts=posts)  


@app.route('/secret/blogs/', methods=['GET', 'POST'])
def blogs():
    form = BlogForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            blog = Blog(title=form.title.data, content=form.content.data)
            db.session.add(blog)
            db.session.commit()
            flash('Your blog is now live!')
            return redirect(url_for('blogs'))
    
    blogs = Blog.query.order_by(Blog.timestamp.desc())
    return render_template('add_blog.html', form=form)

@app.route('/secret/blogs/<pk>/')
def admin_view_blog(pk):
    blog = Blog.query.get_or_404(pk)

    return render_template('admin_blog.html', blog=blog)

@app.route('/secret/blogs/<pk>/edit', methods=['GET', 'POST'])
def update_blog(pk):
    blog = Blog.query.get_or_404(pk)
    form = BlogUpdateForm(obj=blog)
    print(request.method)
    if request.method == 'POST':
        if form.validate_on_submit():
            blog.title = form.title.data
            blog.content = form.content.data

            db.session.commit()

            flash('Your blog is now live!')
            return redirect(url_for('admin_view_blog', pk=blog.id))
    
    form.title.data = blog.title
    form.content.data = blog.content

    return render_template('update_blog.html', form=form, blog=blog)

@app.route('/secret/blogs/<pk>/delete/', methods=['GET', 'POST'])
def delete_blog(pk):
    blog = Blog.query.get_or_404(pk)
    form = BlogDeleteForm(obj=blog)
    print(request.method)
    if request.method == 'POST':
        if form.validate_on_submit():
            print(1)
            db.session.delete(blog)
            db.session.commit()
            print(2)
            return redirect(url_for('admin_view_blog', pk=blog.id))

    return render_template('delete_blog.html', form=form, blog=blog)

@app.route('/secret/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    email = form.email.data
    password = form.password.data
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        if user:
            return redirect(url_for('blogs'))
        else:
            return 'Authentication Failed'
    return render_template('login.html', form=form)