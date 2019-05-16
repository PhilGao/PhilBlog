from flask import Flask,render_template
from philblog.blueprints.blog import blog_dp
from philblog.blueprints.admin import admin_bp
from philblog.extentions import db
from philblog.setting import config
from philblog.models import Article, Comment
import click


def create_app(config_name=None):
    # __name__ ---> module name,
    # so app would point to philblog package ,
    # and it would find the templates folder and render the template
    app = Flask('philblog') #app = Flask(__name__) would be better
    if config_name is None:
        config_name = 'development'
    app.config.from_object(config[config_name])
    register_extentions(app)
    register_blueprints(app)
    register_command(app)
    register_error(app)
    return app


def register_extentions(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(blog_dp)
    app.register_blueprint(admin_bp)


def register_error(app):
    @app.errorhandler(404)
    def error_404(error):
        return render_template('/errors/404.html'), 404

    @app.errorhandler(400)
    def error_400(error):
        return render_template('/errors/400.html'), 404

    @app.errorhandler(500)
    def error_500(error):
        return render_template('/errors/500.html'), 404


def register_command(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, article=Article, comment=Comment)

    @app.cli.command()
    def init_db():
        click.echo('...initial the database')
        db.drop_all()
        db.create_all()

    @app.cli.command()
    def init_fakedata():
        from philblog.fake import fake_author, fake_visitor, fake_category, fake_article_category, fake_comments
        fake_author()
        fake_visitor()
        fake_category()
        fake_article_category()
        fake_comments()

    return app
