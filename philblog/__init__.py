from flask import Flask
from philblog.blueprints.blog import blog_dp
from philblog.extentions import db
from philblog.setting import Config
from philblog.models import Article, Comment
import click


def create_app():
    app = Flask('CatchPity')
    app.config.from_object(Config)
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
