import os

class Config:
    STATIC_DIR = os.path.join(os.path.dirname(__file__), '../static')
    VERSION = "v1.0.0"
    # MySQL 配置
    MYSQL_HOST = os.getenv('MYSQL_HOST', '127.0.0.1')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
    MYSQL_DB = os.getenv('MYSQL_DB', 'suse_db')
    # OSS 配置
    OSS_ACCESS_KEY_ID = os.getenv('OSS_ACCESS_KEY_ID', 'LTAI5tBBgFYxQKaEF3ZQ2y9W')
    OSS_ACCESS_KEY_SECRET = os.getenv('OSS_ACCESS_KEY_SECRET', 'i683yLu5t8FvaqRoci3tAOJjUEbKKN')
    OSS_ENDPOINT = os.getenv('OSS_ENDPOINT', 'oss-cn-shanghai.aliyuncs.com')
    OSS_BUCKET_NAME = os.getenv('OSS_BUCKET_NAME', 'for-kody-iso')