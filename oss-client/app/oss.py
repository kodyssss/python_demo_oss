import oss2
import logging
import traceback
from .config import Config

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

class OSSClient:
    def __init__(self):
        logger.debug(f"Initializing OSS client with endpoint: {Config.OSS_ENDPOINT}, bucket: {Config.OSS_BUCKET_NAME}")
        auth = oss2.Auth(Config.OSS_ACCESS_KEY_ID, Config.OSS_ACCESS_KEY_SECRET)
        self.bucket = oss2.Bucket(auth, Config.OSS_ENDPOINT, Config.OSS_BUCKET_NAME)
        logger.info("OSS client initialized successfully")

    def upload_file(self, object_key, file_stream):
        """
        上传文件到 OSS
        :param object_key: OSS 中的文件路径（如 'avatars/user123.png'）
        :param file_stream: 文件流（如 request.files['avatar'].stream）
        :return: 文件的 OSS URL
        """
        logger.debug(f"Uploading file to OSS: object_key={object_key}")
        try:
            result = self.bucket.put_object(object_key, file_stream)
            logger.debug(f"OSS put_object response: status={result.status}")
            if result.status == 200:
                url = f"https://{Config.OSS_BUCKET_NAME}.{Config.OSS_ENDPOINT.replace('https://', '')}/{object_key}"
                logger.info(f"File uploaded to OSS: {url}")
                return url
            else:
                logger.error(f"OSS upload failed with status: {result.status}")
                raise Exception(f"OSS upload failed with status: {result.status}")
        except Exception as e:
            logger.error(f"Error uploading to OSS: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            raise