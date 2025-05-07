from flask import Flask, request, jsonify
from .oss import OSSClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    oss_client = OSSClient()

    @app.route('/oss-upload', methods=['POST'])
    def oss_upload():
        if 'file' not in request.files or 'object_key' not in request.form:
            return jsonify({'message': '缺少文件或对象键！'}), 400

        file = request.files['file']
        object_key = request.form['object_key']

        try:
            url = oss_client.upload_file(object_key, file.stream)
            return jsonify({'url': url})
        except Exception as e:
            logger.error(f"Error uploading to OSS: {e}")
            return jsonify({'message': 'OSS 上传失败！'}), 500

    return app