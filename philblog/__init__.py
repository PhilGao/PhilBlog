from flask import Flask
from philblog.blueprints.blog import blog_dp
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
    return app


def register_extentions(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(blog_dp)


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
