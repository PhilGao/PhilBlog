from flask import Blueprint,render_template,request,flash,current_app,url_for,send_from_directory
from philblog.models import Article,Category
from philblog.forms import EditorForm
from philblog.extentions import db
import os
from flask_ckeditor import upload_success,upload_fail

admin_bp = Blueprint('admin',__name__)


@admin_bp.route('/admin',methods=['GET','POST'])
def editor():
    form = EditorForm()
    if request.method == 'POST':
        if form.draft.data :
            return render_template('admin/editor.html', form=form)
        if form.submit.data and form.validate_on_submit():
            title = request.form.get('title')
            category_id = request.form.get('category')
            body = request.form.get('body')
            category = db.session.query(Category).filter(Category.id == category_id).first()
            new_article = Article(title=title,content=body)
            new_article.categorys.append(category)
            db.session.add(new_article)
            db.session.commit()
    return render_template('admin/editor.html',form = form)

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
