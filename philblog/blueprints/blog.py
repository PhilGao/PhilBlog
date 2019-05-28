from flask import Flask, render_template, redirect, Blueprint, url_for, request, current_app,send_from_directory
from philblog.extentions import db
import os
from philblog.models import Article, Category
from sqlalchemy import distinct, func

blog_dp = Blueprint('blog', __name__)


@blog_dp.route('/', defaults={'page': 1}, methods=['GET'])
@blog_dp.route('/index', defaults={'page': 1}, methods=['GET'])
@blog_dp.route('/page/<int:page>', methods=['GET'])
def index(page):
    # page = request.args.get('page',1,type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Article.query.order_by(Article.createdate.desc()).paginate(page, per_page=per_page)
    articles = pagination.items
    # articles = Article.query.order_by(Article.createdate.desc()).limit(10).all()
    return render_template('index.html', articles=articles, pagination=pagination)


@blog_dp.route('/tag', methods=['GET'])
def tag():
    # TODO : add cloud pic in here...
    categorys = Category.query.all()
    return render_template('tag.html', categorys=categorys)


@blog_dp.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


# TODO : ISSUE IN HERE , the result is not corret  look like the in expression is not corrent .not sure the reason
@blog_dp.route('/tagged/<int:category_id>', methods=['GET'])
def tagged(category_id):
    articles = Article.query.join(Article.categorys).filter(Category.id.in_([category_id])).all()
    category = db.session.query(Category).filter(Category.id == category_id).first()
    return render_template('tagged.html', articles=articles, category=category)


@blog_dp.route('/archive', methods=['GET'])
def archive():
    # TODO: check the ORM alias the column , now in template using the position which would be confusing in futher
    createdates = db.session.query(distinct(func.date_format(Article.createdate, '%Y-%m-%d'))).order_by(
        func.date_format(Article.createdate, '%Y-%m-%d').desc())
    articles = db.session.query(Article.title, func.date_format(Article.createdate, '%Y-%m-%d'), Article.id).all()
    return render_template('archive.html', createdates=createdates, articles=articles)


@blog_dp.route('/blog/<int:post_id>', methods=['GET'])
def blog(post_id):
    id = post_id
    post = Article.query.get_or_404(id)
    return render_template('blog.html', post=post)