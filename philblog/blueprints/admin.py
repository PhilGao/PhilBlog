from flask import Blueprint, render_template, request, flash, current_app, url_for, send_from_directory, redirect, abort
from philblog.models import Article, Category
from philblog.forms import EditorForm, LoginForm
from philblog.extentions import db
import os
from datetime import datetime
from philblog.util import render_upload_file
from flask_ckeditor import upload_success, upload_fail
from flask_login import login_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/post/manage', methods=['GET', 'POST'])
@login_required
def post_manage():
    articles = db.session.query(Article.title, Article.id).all()
    return render_template('admin/managepost.html', articles=articles)


# todo : category should be the mutiple-checkbox..

@admin_bp.route('/post/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def post_edit(id):
    form = EditorForm()
    article = db.session.query(Article).filter(Article.id == id).first()
    if article:
        form.title.data, form.body.data = article.title, article.content
        category_old_list = article.categorys
        if request.method == 'POST':
            if form.submit.data and form.validate_on_submit():
                show_window_file = request.files.get('show_window')
                if show_window_file:
                    show_window_path = render_upload_file(show_window_file.filename, 'show_window')
                    print(show_window_path)
                    show_window_file.save(show_window_path)
                title = request.form.get('title')
                category_id = request.form.get('category')
                body = request.form.get('body')
                category = db.session.query(Category).filter(Category.id == category_id).first()
                for category_old in category_old_list:
                    article.categorys.remove(category_old)
                article.title = title
                article.content = body
                article.categorys.append(category)
                article.showwindow = show_window_file.filename
                db.session.commit()
                flash('modify the article sucessfully %s' % article.title, 'success')
                return redirect(url_for('admin.post_manage'))
            if form.discard.data:
                return redirect(url_for('admin.post_manage'))
    else:
        flash('No such article', 'error')
        abort(404)
    return render_template('admin/editpost.html', form=form)


@admin_bp.route('/post/<int:id>/drop', methods=['POST'])
@login_required
def post_drop(id):
    try:
        article = db.session.query(Article).filter(Article.id == id).first()
        db.session.delete(article)
        db.session.commit()
        flash('drop the article %s successfully !' % article.title, 'success')
    except Exception as e:
        flash('drop the article %s with error %s ' % (article.title, e), 'success')
    return redirect(url_for('admin.post_manage'))


# todo : save file logic should change to another way , flash category mapping with message color, eg.. error->red,info-->grey
@admin_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def post_new():
    form = EditorForm()
    if request.method == 'POST':
        if form.discard.data:
            title = request.form.get('title')
            message = 'drop the draft {}!'.format(title)
            flash(message, 'success')
            return redirect(url_for('admin.post_manage'))
        if form.submit.data and form.validate_on_submit():
            show_window_file = request.files.get('show_window')
            if show_window_file:
                show_window_path = render_upload_file(show_window_file.filename, 'show_window')
                print(show_window_path)
                show_window_file.save(show_window_path)
            title = request.form.get('title')
            category_id = request.form.get('category')
            body = request.form.get('body')
            category = db.session.query(Category).filter(Category.id == category_id).first()
            new_article = Article(title=title, content=body, createdate=datetime.now(),
                                  showwindow=show_window_file.filename)
            new_article.categorys.append(category)
            db.session.add(new_article)
            db.session.commit()
            flash('The article {} has successfully submitted!'.format(title), 'success')
            return redirect(url_for('admin.post_manage'))
        print(form.errors)
    return render_template('admin/newpost.html', form=form)


@admin_bp.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload():
    f = request.files.get('upload')
    path = os.path.join(current_app.root_path, 'upload', f.filename)
    f.save(path)
    url = url_for('admin.getimage', filename=f.filename)
    return upload_success(url, f.filename)


@admin_bp.route('/getimage/<path:filename>', methods=['GET'])
def getimage(filename):
    return send_from_directory(os.path.join(current_app.root_path, 'upload'), filename)
