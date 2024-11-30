from flask import Blueprint, request, jsonify
from models import db, User, Model, Comment
from sqlalchemy.exc import SQLAlchemyError
import pytz

timezone = pytz.timezone("Asia/Shanghai")
comment_sys = Blueprint("comment_sys", __name__)


@comment_sys.route("/send_comment", methods=["POST"])
def send_comment():
    try:
        data = request.get_json()

        sender_id = data.get("sender_id")  # 评论的用户ID
        target_id = data.get("target_id")  # 评论的目标ID
        target_type = data.get("target_type")  # 评论目标类型，'model' 或 'user'
        content = data.get("content")  # 评论的内容

        if sender_id is None or target_id is None or not target_type or not content:
            return jsonify({"error": "Missing required fields"}), 400

        # 检查目标类型是否合法
        if target_type not in ["model", "user"]:
            return jsonify({"error": "Invalid target type"}), 400

        # 创建评论对象并保存到数据库
        comment = Comment(
            sender_id=sender_id,
            target_id=target_id,
            target_type=target_type,
            content=content,
        )

        db.session.add(comment)
        db.session.commit()

        return jsonify({"message": "Comment added successfully"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "message": str(e)}), 500


@comment_sys.route("/get_comments", methods=["POST"])
def get_comments():
    try:
        data = request.get_json()

        target_id = data.get("target_id")  # 目标ID
        target_type = data.get("target_type")  # 目标类型，'model' 或 'user'

        if target_id is None or not target_type:
            return jsonify({"error": "Missing required parameters"}), 400

        # 确保目标类型合法
        if target_type not in ["model", "user"]:
            return jsonify({"error": "Invalid target type"}), 400

        # 获取评论
        comments = Comment.query.filter_by(
            target_id=target_id, target_type=target_type
        ).all()

        # 转换为JSON格式并返回
        comment_list = [
            {
                "id": comment.id,
                "sender_id": comment.sender_id,
                "sender_name": User.query.filter_by(id=comment.sender_id).first().username,
                "content": comment.content,
                "created_at": comment.created_at.isoformat(),
            }
            for comment in comments
        ]

        return jsonify(comment_list), 200

    except SQLAlchemyError as e:
        return jsonify({"error": "Database error", "message": str(e)}), 500
