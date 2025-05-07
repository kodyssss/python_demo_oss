import os
import requests
import logging
import traceback
from flask import request, jsonify
from .config import Config
from .database import insert_name, get_all_names

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

def init_routes(app):
    OSS_CLIENT_URL = os.getenv('OSS_CLIENT_URL', 'http://oss-client:5002')

    @app.route('/greet', methods=['POST'])
    def greet():
        data = request.get_json()
        name = data.get('name', '').strip()
        logger.debug(f"Received greet request: {data}")
        if not name:
            logger.warning("Name is empty in greet request")
            return jsonify({'message': '名字不能为空！'}), 400
        insert_name(name)
        message = f'欢迎 {name}！感谢您支持 SUSE 的开源创新！'
        logger.info(f"Greet successful for name: {name}")
        return jsonify({'message': message})

    @app.route('/upload-avatar', methods=['POST'])
    def upload_avatar():
        logger.debug(f"Received upload-avatar request: {request.form}, files: {request.files}")
        if 'avatar' not in request.files or 'name' not in request.form:
            logger.warning("Missing avatar file or name in upload-avatar request")
            return jsonify({'message': '缺少头像文件或用户名！'}), 400

        file = request.files['avatar']
        name = request.form['name'].strip()

        if not name:
            logger.warning("Name is empty in upload-avatar request")
            return jsonify({'message': '用户名不能为空！'}), 400

        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            logger.warning(f"Invalid file extension: {file.filename}")
            return jsonify({'message': '仅支持 PNG、JPG 或 JPEG 文件！'}), 400

        import time
        timestamp = int(time.time())
        object_key = f"avatars/{name}_{timestamp}.{file.filename.rsplit('.', 1)[1].lower()}"
        logger.debug(f"Generated object_key: {object_key}")

        try:
            files = {'file': (file.filename, file.stream)}
            data = {'object_key': object_key}
            logger.debug(f"Sending request to OSS client: {OSS_CLIENT_URL}/oss-upload, data: {data}, file: {file.filename}")
            response = requests.post(
                f'{OSS_CLIENT_URL}/oss-upload',
                data=data,
                files=files,
                timeout=10  # Add timeout to avoid hanging
            )
            logger.debug(f"OSS client response: status={response.status_code}, body={response.text}")
            if response.status_code != 200:
                raise Exception(f"OSS client error: {response.json().get('message', 'Unknown error')}")
            avatar_url = response.json().get('url')
            logger.info(f"Successfully uploaded avatar for {name}, URL: {avatar_url}")
            insert_name(name, avatar_url)
            return jsonify({'message': f'头像上传成功！欢迎 {name}！', 'avatar_url': avatar_url})
        except Exception as e:
            logger.error(f"Error uploading avatar: {str(e)}")
            logger.error(f"Stack trace: {traceback.format_exc()}")
            return jsonify({'message': '发生错误，请稍后再试！'}), 500