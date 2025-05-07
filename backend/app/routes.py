from flask import send_from_directory, render_template, request, jsonify
import requests
import logging
from .config import Config
from .database import insert_name, get_all_names

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_routes(app):
    # Static files route removed (handled by frontend)
    
    # Homepage route removed (handled by frontend)

    # Greet endpoint
    @app.route('/greet', methods=['POST'])
    def greet():
        data = request.get_json()
        name = data.get('name', '').strip()
        if not name:
            return jsonify({'message': '名字不能为空！'}), 400
        insert_name(name)
        message = f'欢迎 {name}！感谢您支持 SUSE 的开源创新！'
        return jsonify({'message': message})

    # Avatar upload
    @app.route('/upload-avatar', methods=['POST'])
    def upload_avatar():
        if 'avatar' not in request.files or 'name' not in request.form:
            return jsonify({'message': '缺少头像文件或用户名！'}), 400

        file = request.files['avatar']
        name = request.form['name'].strip()

        if not name:
            return jsonify({'message': '用户名不能为空！'}), 400

        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return jsonify({'message': '仅支持 PNG、JPG 或 JPEG 文件！'}), 400

        import time
        timestamp = int(time.time())
        object_key = f"avatars/{name}_{timestamp}.{file.filename.rsplit('.', 1)[1].lower()}"

        try:
            # Call OSS client service
            files = {'file': (file.filename, file.stream)}
            response = requests.post(
                'http://oss-client:5002/oss-upload',
                data={'object_key': object_key},
                files=files
            )
            if response.status_code != 200:
                raise Exception(f"OSS client error: {response.json().get('message')}")
            avatar_url = response.json().get('url')
            insert_name(name, avatar_url)
            return jsonify({'message': f'头像上传成功！欢迎 {name}！', 'avatar_url': avatar_url})
        except Exception as e:
            logger.error(f"Error uploading avatar: {e}")
            return jsonify({'message': '头像上传失败，请稍后再试！'}), 500