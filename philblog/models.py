from philblog.extentions import db

mapping_article_category = db.Table('mapping_article_category',
                                    db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
                                    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
                                    )


class Article(db.Model):
    __tablename__ = 'article'
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
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def is_active(self):
        #This property should return True if this is an active user
        return True
    def is_authenticated(self):
        #This property should return True if the user is authenticated,
        return True
    def is_anonymous(self):
        #This property should return True if this is an anonymous user. (Actual users should return False instead.)
        return False
    def get_id(self):
        return str(self.id)