from flask import Flask, request, jsonify
from .oss import OSSClient
import logging
import traceback

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    oss_client = OSSClient()
    logger.info("OSS client initialized")

    @app.route('/health')
    def health():
        logger.debug("Received health check request")
        return jsonify({'status': 'ok'})

    @app.route('/oss-upload', methods=['POST'])
    def oss_upload():
        logger.debug(f"Received oss-upload request: {request.form}, files: {request.files}")
        if 'file' not in request.files or 'object_key' not in request.form:
            logger.warning("Missing file or object_key in oss-upload request")
            return jsonify({'message': '缺少文件或对象键！'}), 400

        file = request.files['file']
        object_key = request.form['object_key']
        logger.debug(f"Processing upload for object_key: {object_key}, file: {file.filename}")

        # Basic extension validation (since python-magic is not installed)
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            logger.warning(f"Invalid file extension: {file.filename}")
            return jsonify({'message': '仅支持 PNG、JPG 或 JPEG 文件！'}), 400

        try:
            url = oss_client.upload_file(object_key, file.stream)
            logger.info(f"Successfully uploaded file to OSS: {url}")
            return jsonify({'url': url})
        except Exception as e:
            logger.error(f"Error uploading to OSS: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            return jsonify({'message': 'OSS 上传失败！'}), 500

    return app
