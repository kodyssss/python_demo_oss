import oss2
import logging
from .config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OSSClient:
    def __init__(self):
        auth = oss2.Auth(Config.OSS_ACCESS_KEY_ID, Config.OSS_ACCESS_KEY_SECRET)
        self.bucket = oss2.Bucket(auth, Config.OSS_ENDPOINT, Config.OSS_BUCKET_NAME)

    def upload_file(self, object_key, file_stream):
        try:
            result = self.bucket.put_object(object_key, file_stream)
            if result.status == 200:
                url = f"https://{Config.OSS_BUCKET_NAME}.{Config.OSS_ENDPOINT.replace('https://', '')}/{object_key}"
                logger.info(f"File uploaded to OSS: {url}")
                return url
            else:
                logger.error(f"OSS upload failed with status: {result.status}")
                raise Exception("OSS upload failed")
        except Exception as e:
            logger.error(f"Error uploading to OSS: {e}")
            raise