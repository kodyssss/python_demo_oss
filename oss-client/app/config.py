import os

class Config:
    OSS_ACCESS_KEY_ID = os.getenv('OSS_ACCESS_KEY_ID', 'LTAI5tBBgFYxQKaEF3ZQ2y9W')
    OSS_ACCESS_KEY_SECRET = os.getenv('OSS_ACCESS_KEY_SECRET', 'i683yLu5t8FvaqRoci3tAOJjUEbKKN')
    OSS_ENDPOINT = os.getenv('OSS_ENDPOINT', 'https://oss-cn-shanghai.aliyuncs.com')
    OSS_BUCKET_NAME = os.getenv('OSS_BUCKET_NAME', 'for-kody-iso')