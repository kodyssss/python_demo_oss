from flask import send_from_directory, render_template, request, jsonify
from .config import Config
from .database import insert_name, get_all_names
from .oss import OSSClient
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_routes(app):
    oss_client = OSSClient()

    # 静态文件
    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory(Config.STATIC_DIR, filename)

    # 首页
    @app.route('/')
    def hello():
        names = get_all_names()
        return render_template('index.html', version=Config.VERSION, names=names)

    # 问候
    @app.route('/greet', methods=['POST'])
    def greet():
        data = request.get_json()
        name = data.get('name', '').strip()
        if not name:
            return jsonify({'message': '名字不能为空！'}), 400
        insert_name(name)
        message = f'欢迎 {name}！感谢您支持 SUSE 的开源创新！'
        return jsonify({'message': message})

    # 头像上传
    @app.route('/upload-avatar', methods=['POST'])
    def upload_avatar():
        if 'avatar' not in request.files or 'name' not in request.form:
            return jsonify({'message': '缺少头像文件或用户名！'}), 400

        file = request.files['avatar']
        name = request.form['name'].strip()

        if not name:
            return jsonify({'message': '用户名不能为空！'}), 400

        # 验证文件类型
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return jsonify({'message': '仅支持 PNG、JPG 或 JPEG 文件！'}), 400

        # 构造 OSS 文件路径（使用时间戳和用户名避免冲突）
        import time
        timestamp = int(time.time())
        object_key = f"avatars/{name}_{timestamp}.{file.filename.rsplit('.', 1)[1].lower()}"

        try:
            # 上传到 OSS
            avatar_url = oss_client.upload_file(object_key, file.stream)
            # 存储到数据库
            insert_name(name, avatar_url)
            return jsonify({'message': f'头像上传成功！欢迎 {name}！', 'avatar_url': avatar_url})
        except Exception as e:
            logger.error(f"Error uploading avatar: {e}")
            return jsonify({'message': '头像上传失败，请稍后再试！'}), 500