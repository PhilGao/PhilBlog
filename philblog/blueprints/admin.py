from flask import Blueprint,render_template,request,flash,current_app,url_for,send_from_directory,redirect,abort
from philblog.models import Article,Category
from philblog.forms import EditorForm,LoginForm
from philblog.extentions import db
import os
from datetime import datetime
from philblog.util import render_upload_file
from flask_ckeditor import upload_success,upload_fail

admin_bp = Blueprint('admin',__name__)


@admin_bp.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.login.data:
            #TODO: do validation here.
            return
    return render_template('admin/login.html',form = form)


@admin_bp.route('/post/manage',methods = ['GET','POST'])
def post_manage():
    articles = db.session.query(Article.title,Article.id).all()
    return render_template('admin/managepost.html',articles = articles)

#todo : category should be the mutiple-checkbox.. remove the show window required
@admin_bp.route('/post/<int:id>/edit',methods = ['GET','POST'])
def post_edit(id):
    form = EditorForm()
    article = db.session.query(Article).filter(Article.id==id).first()
    if article:
        form.title.data,form.body.data = article.title,article.content
        category_old_list = article.categorys
        if request.method == 'POST':
            if form.submit.data and form.validate_on_submit():
                title = request.form.get('title')
                category_id = request.form.get('category')
                body = request.form.get('body')
                category = db.session.query(Category).filter(Category.id == category_id).first()
                for category_old in category_old_list:
                    article.categorys.remove(category_old)
                article.title = title
                article.content = body
                article.categorys.append(category)
                db.session.commit()
                flash('modify the article sucessfully %s' %article.title)
                return redirect(url_for('admin.post_manage'))
    else:
        flash('No such article')
        abort(404)
    return render_template('admin/editpost.html',form=form)

@admin_bp.route('/post/<int:id>/drop',methods = ['POST'])
def post_drop(id):
    try:
        article = db.session.query(Article).filter(Article.id == id).first()
        db.session.delete(article)
        db.session.commit()
        flash('drop the article %s successfully !' %article.title)
    except Exception as e:
        flash('drop the article %s with error %s ' %(article.title,e))
    return redirect('/post/manage')

# todo : change the route name to new post may be better, save file logic should change to another way
@admin_bp.route('/post/new',methods=['GET','POST'])
def post_new():
    form = EditorForm()
    if request.method == 'POST':
        if form.draft.data :
            title = request.form.get('title')
            message = 'drop the draft {}!'.format(title)
            flash(message)
            return redirect(url_for('admin.editor'))
        if form.submit.data and form.validate_on_submit():
            show_window_file = request.files.get('show_window')
            if show_window_file:
                show_window_path = render_upload_file(show_window_file.filename,'show_window')
                print(show_window_path)
                show_window_file.save(show_window_path)
            title = request.form.get('title')
            category_id = request.form.get('category')
            body = request.form.get('body')
            category = db.session.query(Category).filter(Category.id == category_id).first()
            new_article = Article(title=title,content=body,createdate=datetime.now(),showwindow=show_window_file.filename)
            new_article.categorys.append(category)
            db.session.add(new_article)
            db.session.commit()
            flash('The article {} has successfully submitted!'.format(title))
            return redirect(url_for('admin.post_manage'))
        print(form.errors)
    return render_template('admin/newpost.html',form = form)

@admin_bp.route('/upload/',methods = ['GET','POST'])
def upload():
    f = request.files.get('upload')
    path = os.path.join(current_app.root_path,'upload',f.filename)
    f.save(path)
    url = url_for('admin.getimage',filename = f.filename)
    return upload_success(url,f.filename)


@admin_bp.route('/getimage/<path:filename>',methods = ['GET'])
def getimage(filename):
    return send_from_directory(os.path.join(current_app.root_path,'upload'),filename)
