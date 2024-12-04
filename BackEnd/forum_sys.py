from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Post, PostLog, User, Model
from sqlalchemy.exc import IntegrityError
import datetime
import pytz
from sqlalchemy.exc import SQLAlchemyError

timezone = pytz.timezone("Asia/Shanghai")
# 创建forum蓝图
forum_sys = Blueprint("forum_sys", __name__)


# 创建帖子
@forum_sys.route("/create_post", methods=["POST"])
def create_post():
    data = request.get_json()

    # 从请求数据获取信息
    title = data.get("title")
    content = data.get("content")
    owner_id = data.get("owner_id")
    target_id = data.get("target_id")
    target_type = data.get("target_type")

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
        created_at=datetime.datetime.now(timezone),
    )

    try:
        # 添加到数据库
        db.session.add(new_post)
        db.session.commit()

        # 返回创建成功的响应
        return (
            jsonify({"message": "Post created successfully", "post_id": new_post.id}),
            201,
        )
    except IntegrityError:
        db.session.rollback()
        return (
            jsonify(
                {"error": "Error creating post, possibly due to database constraints"}
            ),
            500,
        )


# 创建帖子日志
@forum_sys.route("/create_post_log", methods=["POST"])
def create_post_log():
    data = request.get_json()

    # 从请求数据获取信息
    post_id = data.get("post_id")
    sender_id = data.get("sender_id")
    message = data.get("message")

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
        created_at=datetime.datetime.now(timezone),
    )

    try:
        # 添加到数据库
        db.session.add(new_post_log)
        db.session.commit()

        # 返回创建成功的响应
        return (
            jsonify(
                {"message": "Post log created successfully", "log_id": new_post_log.id}
            ),
            201,
        )
    except IntegrityError:
        db.session.rollback()
        return (
            jsonify(
                {
                    "error": "Error creating post log, possibly due to database constraints"
                }
            ),
            500,
        )


# 获取指定帖子的所有日志
@forum_sys.route("/get_post_logs", methods=["POST"])
def get_post_logs():
    data = request.get_json()

    # 从请求数据获取帖子ID
    post_id = data.get("post_id")

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
            "time": log.created_at,  # 格式化时间
        }
        for log in post_logs
    ]

    return jsonify(logs_data), 200


# 获取所有帖子
@forum_sys.route("/get_all_posts", methods=["POST"])
def get_all_posts():
    data = request.get_json()
    search_id = data.get("search_id")
    Type = data.get("search_type")

    if search_id == "" or search_id is None:
        posts = Post.query.all()
    else:
        if Type == "owner_id":
            posts = Post.query.filter_by(owner_id=search_id).all()
        elif Type == "target_user":
            posts = Post.query.filter_by(target_id=search_id, target_type="user").all()
        else:
            posts = Post.query.filter_by(target_id=search_id, target_type="model").all()
    # 获取所有帖子

    # 构造帖子列表
    posts_data = [
        {
            "post_id": post.id,
            "title": post.title,
            "owner_id": post.owner_id,
            "owner_name": User.query.get(post.owner_id).username,
            "target_id": post.target_id,
            "target_type": post.target_type,
            "target_name": (
                User.query.get(post.target_id).username
                if post.target_type == "user"
                else Model.query.get(post.target_id).model_name
            ),
            "created_at": post.created_at,  # 格式化时间
            "content": post.content,
        }
        for post in posts
    ]

    return jsonify(posts_data), 200


@forum_sys.route("/get_posts_by_all_user", methods=["POST"])
def get_posts_by_all_user():
    try:
        data = request.get_json()

        user_id = data.get("user_id")  # 目标ID

        posts = Post.query.filter_by(target_id=user_id, target_type="user").all()

        post_list = [
            {
                "id": post.id,
                "model_name": "",
                "sender_id": post.owner_id,
                "sender_name": User.query.filter_by(id=post.owner_id).first().username,
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at.isoformat(),
                "has_read": post.has_read,
            }
            for post in posts
        ]

        models: list[Model] = Model.query.filter_by(owner_id=user_id).all()
        for model in models:
            model_posts: list[Post] = Post.query.filter_by(
                target_id=model.id, target_type="model"
            ).all()

            for post in model_posts:
                post_list.append(
                    {
                        "id": post.id,
                        "model_name": model.model_name,
                        "sender_id": post.owner_id,
                        "sender_name": User.query.filter_by(id=post.owner_id)
                        .first()
                        .username,
                        "title": post.title,
                        "content": post.content,
                        "created_at": post.created_at.isoformat(),
                        "has_read": post.has_read,
                    }
                )

        return jsonify(post_list), 200

    except SQLAlchemyError as e:
        print(str(e))
        return jsonify({"error": "Database error", "message": str(e)}), 500


@forum_sys.route("/read_posts", methods=["POST"])
def read_posts():
    data = request.get_json()

    post_id = data.get("id")
    post: Post = Post.query.get(post_id)

    post.has_read = True
    db.session.commit()
    return jsonify({"message": "Success!"}), 200
