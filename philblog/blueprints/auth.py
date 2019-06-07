from flask import Blueprint,request,render_template,abort,redirect,flash
from philblog.forms import LoginForm
from philblog.extentions import db
from philblog.models import User


auth_bp = Blueprint('auth',__name__)

@auth_bp.route('/login')
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.login.data:
            username = request.form.get('username')
            password = request.form.get('password')
            user = db.session.query(User).filter(User.username==username,User.password==password).first()
            if user:
                flash('login sucessfully !')
                redirect('admin/post_manage')
            else:
                abort(400)
    return render_template('auth/login.html',form = form)

