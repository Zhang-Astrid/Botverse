from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Post, PostLog, User
from sqlalchemy.exc import IntegrityError
import datetime
import pytz

timezone = pytz.timezone("Asia/Shanghai")
# 创建forum蓝图
forum_sys = Blueprint('forum_sys', __name__)

# 创建帖子
@forum_sys.route('/create_post', methods=['POST'])
def create_post():
    data = request.get_json()
    
    # 从请求数据获取信息
    title = data.get('title')
    content = data.get('content')
    owner_id = data.get('owner_id')
    target_id = data.get('target_id')
    target_type = data.get('target_type')
    
    # 确保提供了必需的字段
    if not title or owner_id is None or target_id is None or not target_type:
        return jsonify({"error": "Missing required fields"}), 400

    # 创建新的Post实例
    new_post = Post(
        title=title,
        content=content,
        owner_id=owner_id,
        target_id=target_id,
        target_type=target_type,
        created_at=datetime.datetime.now(timezone)
    )
    
    try:
        # 添加到数据库
        db.session.add(new_post)
        db.session.commit()
        
        # 返回创建成功的响应
        return jsonify({"message": "Post created successfully", "post_id": new_post.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Error creating post, possibly due to database constraints"}), 500

# 创建帖子日志
@forum_sys.route('/create_post_log', methods=['POST'])
def create_post_log():
    data = request.get_json()
    
    # 从请求数据获取信息
    post_id = data.get('post_id')
    sender_id = data.get('sender_id')
    message = data.get('message')

    # 确保提供了必需的字段
    if not post_id or sender_id is None or not message:
        return jsonify({"error": "Missing required fields"}), 400

    # 确保帖子存在
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    # 创建新的PostLog实例
    new_post_log = PostLog(
        post_id=post_id,
        sender_id=sender_id,
        message=message,
        created_at=datetime.datetime.now(timezone)
    )

    try:
        # 添加到数据库
        db.session.add(new_post_log)
        db.session.commit()
        
        # 返回创建成功的响应
        return jsonify({"message": "Post log created successfully", "log_id": new_post_log.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Error creating post log, possibly due to database constraints"}), 500

# 获取指定帖子的所有日志
@forum_sys.route('/get_post_logs', methods=['POST'])
def get_post_logs():
    data = request.get_json()

    # 从请求数据获取帖子ID
    post_id = data.get('post_id')
    
    # 确保提供了帖子ID
    if not post_id:
        return jsonify({"error": "Missing post_id"}), 400
    
    # 确保帖子存在
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    # 获取帖子下的所有日志
    post_logs = PostLog.query.filter_by(post_id=post_id).all()

    # 构造日志列表
    logs_data = [
        {
            "log_id": log.id,
            "sender_id": log.sender_id,
            "sender_name": User.query.get(log.sender_id).username,
            "message": log.message,
            "time": log.created_at  # 格式化时间
        }
        for log in post_logs
    ]
    
    return jsonify(logs_data), 200

# 获取所有帖子
@forum_sys.route('/get_all_posts', methods=['POST'])
def get_all_posts():
    # 获取所有帖子
    posts = Post.query.all()

    # 构造帖子列表
    posts_data = [
        {
            "post_id": post.id,
            "title": post.title,
            "owner_id": post.owner_id,
            "target_id": post.target_id,
            "target_type": post.target_type,
            "created_at": post.created_at  # 格式化时间
        }
        for post in posts
    ]
    
    return jsonify(posts_data), 200