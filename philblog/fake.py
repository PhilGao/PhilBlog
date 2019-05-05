from faker import Faker
from philblog.extentions import db
from philblog.models import Article, Author, Comment, Visitor, Category, mapping_article_category
import random

fake = Faker()


def fake_author(count=5):
    for i in range(count):
        author = Author(
            name=fake.name(),
            email=fake.email(),
            information=fake.sentence()
        )
        db.session.add(author)
    db.session.commit()


def fake_visitor(count=20):
    for i in range(count):
        visitor = Visitor(
            name=fake.name(),
            email=fake.email(),
            information=fake.sentence()
        )
        db.session.add(visitor)
    db.session.commit()


def fake_category(count=8):
    for i in range(count):
        category = Category(category_name=fake.city())
        db.session.add(category)
    db.session.commit()


def fake_article_category(count=50):
    categorys = db.session.query(Category).all()
    categorycount = db.session.query(Category).count()
    for i in range(count):
        article = Article(title=fake.sentence(),
                          content=fake.text(2000),
                          createdate=fake.date_time_this_year(),
                          # TODO: should be the random id from min id to maxid
                          author_id=random.randint(1, Author.query.count())
                          )
        for j in range(random.randint(0, categorycount)):
            article.categorys.append(categorys[j])
        db.session.add(article)
    db.session.commit()


def fake_comments(count=100):
    article_count = Article.query.count()
    visitor_count = Visitor.query.count()
    for i in range(count):
        comment = Comment(
            article_id=random.randint(1, article_count),
            visitor_id=random.randint(1, visitor_count),
            comments=fake.sentence(),
            comment_date=fake.date_time_this_year()
        )
        db.session.add(comment)
    db.session.commit()
