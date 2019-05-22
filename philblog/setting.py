class BaseConfig:
    BLOG_POST_PER_PAGE = 5


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@123@localhost:3306/catpity"
    BLOG_POST_PER_PAGE = 5
    SECRET_KEY = 'SFSDKJFSKJF'
    CKEDITOR_FILE_UPLOADER = 'upload'


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@123@localhost:3306/catpity"
    BLOG_POST_PER_PAGE = 5


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@123@localhost:3306/catpity"
    BLOG_POST_PER_PAGE = 5


config = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'production': ProductionConfig
}
