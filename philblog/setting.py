class BaseConfig:
    BLOG_POST_PER_PAGE = 5


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@123@localhost:3306/catpity"
    ELASTICSEARCH_URL = "http://localhost:9200"
    BLOG_POST_PER_PAGE = 5
    SECRET_KEY = 'SFSDKJFSKJF'
    CKEDITOR_FILE_UPLOADER = 'upload'
    #WTF_CSRF_ENABLED = False


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@123@localhost:3306/catpity"
    BLOG_POST_PER_PAGE = 5
    SECRET_KEY = 'SFSDKJFSKJF'
    CKEDITOR_FILE_UPLOADER = 'upload'



class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@123@localhost:3306/catpity"
    BLOG_POST_PER_PAGE = 5
    SECRET_KEY = 'SFSDKJFSKJF'
    CKEDITOR_FILE_UPLOADER = 'upload'


config = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'production': ProductionConfig
}
