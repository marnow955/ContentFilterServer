class Config(object):
    PROJECT = 'Content filtering server'
    SECRET_KEY = 'dev key'
    DEBUG = False


class DbConfig(object):
    HOST = "localhost"
    USER = "root"
    PASSWORD = ""
    DATABASE = "posts"


class SqliteConfig(object):
    DATABASE_PATH = 'PATH/TO/LOCAL/SQLITE/DATABASE'


AuthConfig = [{
    'USER': 'admin',
    'PASSWORD': 'BD2B1AAF7EF4F09BE9F52CE2D8D599674D81AA9D6A4421696DC4D93DD0619D68'
                '2CE56B4D64A9EF097761CED99E0F67265B5F76085E5B0EE7CA4696B2AD6FE2B2'  # 'secret'
}]
