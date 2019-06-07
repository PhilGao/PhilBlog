from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,SubmitField,PasswordField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import data_required,length
from philblog.models import Category


class EditorForm(FlaskForm):
    title = StringField('Title',validators=[data_required(),length(1,200)])
    category = SelectField('Category',coerce=int,default=1)
    body = CKEditorField('body')
    show_window = FileField('Show Windows...')
    submit = SubmitField('Submit')
    discard = SubmitField('Discard')

    def __init__(self,*args,**kwargs):
        super(EditorForm,self).__init__(*args,**kwargs)
        self.category.choices = [(category.id,category.category_name) for category in Category.query.order_by(Category.id).all()]


class LoginForm(FlaskForm):
    username = StringField('UserName', validators = [data_required(),length(1,50)],render_kw={"placeholder": "please enter username"})
    password = PasswordField('password', validators = [data_required()],render_kw={"placeholder": "Please enter password"})
    login = SubmitField('Login')
    def __init__(self,*args,**kwargs):
        super(LoginForm,self).__init__(*args,**kwargs)