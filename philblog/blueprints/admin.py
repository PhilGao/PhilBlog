from flask import Blueprint,render_template
from philblog.forms import EditorForm

admin_bp = Blueprint('admin',__name__)


@admin_bp.route('/admin',methods=['GET','POST'])
def editor():
    form = EditorForm()
    return render_template('admin/editor.html',form = form)
