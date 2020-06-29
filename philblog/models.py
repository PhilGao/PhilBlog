from philblog.extentions import db
from philblog.search import query_index, add_to_index, remove_from_index


class SearchableMixin(object):
    """
    实现搜索的Mixin类，包括搜索es关键字，db session提交前与提交后的处理以及reindex的方法
    """

    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls, expression, page, per_page)
        return cls.query.filter(cls.id.in_(ids)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(obj.__tablename__, obj)


# add hooker to db event
db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

mapping_article_category = db.Table('mapping_article_category',
                                    db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
                                    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
                                    )


class Article(db.Model, SearchableMixin):
    __tablename__ = 'article'
    __searchable__ = ['title', 'content','createdate','modifieddate']
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    title = db.Column(db.String(255))
    showwindow = db.Column(db.String(255))
    content = db.Column(db.Text)
    createdate = db.Column(db.DateTime)
    modifieddate = db.Column(db.DateTime)

    comments = db.relationship('Comment')
    categorys = db.relationship('Category', secondary=mapping_article_category, back_populates='articles')


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    information = db.Column(db.String(255))


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'))
    comments = db.Column(db.Text)
    reply_id = db.Column(db.Integer)
    comment_date = db.Column(db.DateTime)
    article = db.relationship('Article')


class Visitor(db.Model):
    __tablename__ = 'visitor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    information = db.Column(db.String(255))


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50))

    articles = db.relationship('Article', secondary=mapping_article_category, back_populates='categorys')


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def is_active(self):
        # This property should return True if this is an active user
        return True

    def is_authenticated(self):
        # This property should return True if the user is authenticated,
        return True

    def is_anonymous(self):
        # This property should return True if this is an anonymous user. (Actual users should return False instead.)
        return False

    def get_id(self):
        return str(self.id)
