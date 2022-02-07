import os

from flask import render_template, request, flash, redirect, url_for, send_from_directory
from flask_login import login_required
from flask_ckeditor import upload_success, upload_fail

from . import admin
from app import db
from app.forms import BlogForm, BlogDeleteForm, BlogUpdateForm
from app.models import Blog

@admin.route('/add_blogs', methods = ['GET', 'POST'])
@login_required
def admin_add_blog():
    form = BlogForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            blog = Blog(
                title=form.title.data, 
                content=form.content.data, 
                description=form.description.data
            )
            db.session.add(blog)
            db.session.commit()
            flash('Your blog is now live!')
            return redirect(url_for('home.admin_dashboard'))

    return render_template('admin/admin_add_blog.html', form=form)

@admin.route('/blogs', methods = ['GET', 'POST'])
def admin_view_blogs():
    blogs = Blog.query.order_by(Blog.timestamp.desc())
    return render_template('home/admin_dashboard.html', blogs=blogs)


@admin.route('/blogs/<pk>')
def admin_view_blog(pk):
    blog = Blog.query.get_or_404(pk)

    return render_template('admin/admin_blog.html', blog=blog)


@admin.route('/blogs/<pk>/edit', methods=['GET', 'POST'])
def admin_update_blog(pk):
    blog = Blog.query.get_or_404(pk)
    form = BlogUpdateForm(obj=blog)
    print(request.method)
    if request.method == 'POST':
        if form.validate_on_submit():
            blog.title = form.title.data
            blog.description = form.description.data
            blog.content = form.content.data

            db.session.commit()

            flash('Your blog is now live!')
            return redirect(url_for('admin.admin_view_blog', pk=blog.id))
    
    form.title.data = blog.title
    form.content.data = blog.content

    return render_template('admin/admin_update_blog.html', form=form, blog=blog)

@admin.route('/blogs/<pk>/delete', methods=['GET', 'POST'])
def admin_delete_blog(pk):
    blog = Blog.query.get_or_404(pk)
    form = BlogDeleteForm(obj=blog)

    if request.method == 'POST':
        if form.validate_on_submit():
            db.session.delete(blog)
            db.session.commit()
            flash('Your blog has been deleted!')
            return redirect(url_for('admin.admin_view_blogs'))

    return render_template('admin/admin_delete_blog.html', form=form, blog=blog)
