from flask import Blueprint,render_template,request,flash
from philblog.forms import EditorForm

admin_bp = Blueprint('admin',__name__)


@admin_bp.route('/admin',methods=['GET','POST'])
def editor():
    form = EditorForm()
    if request.method == 'POST':
        print(request.form['title'],request.form['category'])
        print(request.form['body'])
    return render_template('admin/editor.html',form = form)
