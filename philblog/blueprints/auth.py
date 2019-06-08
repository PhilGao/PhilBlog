from flask import Blueprint,request,render_template,abort,redirect,flash,url_for
from philblog.forms import LoginForm
from philblog.extentions import db,login_manager
from philblog.models import User
from flask_login import login_user,logout_user,login_required


auth_bp = Blueprint('auth',__name__)


@login_manager.user_loader
def load_user(user_id):
    if not user_id:
        return None
    else:
        curr_user = db.session.query(User).filter(User.id == int(user_id)).first()
    return curr_user


@auth_bp.route('/login',methods = ['POST','GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.login.data:
            try:
                username = request.form.get('username')
                password = request.form.get('password')
                user = db.session.query(User).filter(User.username==username,User.password==password).first()
                if user:
                    login_user(user)
                    flash('Login Successfully !','success')
                    return redirect(url_for('blog.index'))
                else:
                    flash('Login Failed! Please check the user name and password!','error')
                    return redirect(url_for('auth.login'))
            except Exception as e :
                abort(500)
    return render_template('auth/login.html',form = form)


@auth_bp.route('/logout',methods = ['GET'])
@login_required
def logout():
    logout_user()
    flash("logout!",'success')
    return redirect(url_for('blog.index'))