from datetime import datetime
from flask import Blueprint, request, jsonify

from functions import simple_chat
from models import db, Model, User, Session  # 导入SQLAlchemy的db和模型

chat_sys = Blueprint("chat_sys", __name__)


@chat_sys.route("/create_session", methods=["POST"])
def create_session():
    data = request.get_json()  # 获取客户端传来的 JSON 数据

    # 从 JSON 数据中获取相关字段
    session_name = data.get("session_name")
    model_id = data.get("model_id")
    owner_id = data.get("owner_id")
    logs = data.get("logs", [])  # 如果没有日志字段，则默认为空数组

    # 检查必填字段
    if not session_name or not model_id or not owner_id:
        return (
            jsonify({"error": "session_name, model_id, and owner_id are required"}),
            401,
        )  # 修改为 401 错误码

    # 检查是否存在相关的用户和模型
    user = User.query.get(owner_id)
    model = Model.query.get(model_id)

    if not user:
        return jsonify({"error": "User not found"}), 401  # 修改为 401 错误码
    if not model:
        return jsonify({"error": "Model not found"}), 401  # 修改为 401 错误码

    # 创建新的 Session 对象
    new_session = Session(
        session_name=session_name,
        model_id=model_id,
        owner_id=owner_id,
        logs=logs,
        created_at=datetime.now(datetime.timezone.utc),  # 设置创建时间为当前时间
    )

    # 将新会话保存到数据库
    db.session.add(new_session)
    db.session.commit()

    return (
        jsonify(
            {
                "id": new_session.id,
                "session_name": new_session.session_name,
                "model_id": new_session.model_id,
                "owner_id": new_session.owner_id,
                "created_at": new_session.created_at,
            }
        ),
        200,
    )  # 修改为 200 成功响应


@chat_sys.route("/update_session", methods=["POST"])
def update_session():
    data = request.get_json()  # 获取客户端传来的 JSON 数据

    # 从 JSON 数据中获取相关字段
    session_id = data.get("session_id")  # 获取会话 ID
    session_name = data.get("session_name")
    model_id = data.get("model_id")
    owner_id = data.get("owner_id")
    logs = data.get("logs")

    # 检查 session_id 是否存在
    if not session_id:
        return (
            jsonify({"error": "session_id is required"}),
            401,
        )  # 返回错误，如果没有提供 session_id

    # 查找会话对象
    session = Session.query.get(session_id)

    if not session:
        return (
            jsonify({"error": "Session not found"}),
            401,
        )  # 如果会话不存在，返回 401 错误

    # 检查是否提供了更新的字段，如果有需要更新的字段则更新
    if session_name:
        session.session_name = session_name
    if model_id:
        # 检查模型是否存在
        model = Model.query.get(model_id)
        if not model:
            return (
                jsonify({"error": "Model not found"}),
                401,
            )  # 如果模型不存在，返回 401 错误
        session.model_id = model_id
    if owner_id:
        # 检查用户是否存在
        user = User.query.get(owner_id)
        if not user:
            return (
                jsonify({"error": "User not found"}),
                401,
            )  # 如果用户不存在，返回 401 错误
        session.owner_id = owner_id
    if logs is not None:  # 如果 logs 字段存在且不为 None，进行更新
        session.logs = logs

    # 更新会话的修改时间（例如，设置为当前时间）
    session.updated_at = datetime.now(datetime.timezone.utc)  # 使用当前 UTC 时间更新

    # 提交更改
    db.session.commit()

    return (
        jsonify(
            {
                "id": session.id,
                "session_name": session.session_name,
                "model_id": session.model_id,
                "owner_id": session.owner_id,
                "logs": session.logs,
                "created_at": session.created_at,
                "updated_at": session.updated_at,
            }
        ),
        200,
    )  # 返回 200 成功响应


@chat_sys.route("/get_session", methods=["GET"])
def get_session():
    # 从请求的查询参数中获取 session_id
    session_id = request.args.get("session_id")

    # 检查 session_id 是否存在
    if not session_id:
        return jsonify({"error": "session_id is required"}), 401  # 返回 401 错误

    # 查询数据库，查找对应的会话
    session = Session.query.get(session_id)

    if not session:
        return jsonify({"error": "Session not found"}), 401  # 返回 401 错误

    # 返回会话信息
    return (
        jsonify(
            {
                "id": session.id,
                "session_name": session.session_name,
                "model_id": session.model_id,
                "owner_id": session.owner_id,
                "logs": session.logs,
                "created_at": session.created_at,
                "updated_at": session.updated_at,
            }
        ),
        200,
    )  # 返回 200 成功响应
