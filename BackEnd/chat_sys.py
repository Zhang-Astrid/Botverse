from datetime import datetime
from flask import Blueprint, request, jsonify

from functions import simple_chat
from models import db, Model, User, Session,Log  # 导入SQLAlchemy的db和模型

chat_sys = Blueprint("chat_sys", __name__)


@chat_sys.route("/create_session", methods=["POST"])
def create_session():
    data = request.get_json()  # 获取客户端传来的 JSON 数据

    # 从 JSON 数据中获取相关字段
    session_name = data.get("session_name")
    model_id = data.get("model_id")
    owner_id = data.get("owner_id")

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

    # 从 JSON 数据中获取相关字段 session_id必须存在 其他的session_name model_id owner_id 可以为空
    session_id = data.get("session_id")  # 获取会话 ID
    session_name = data.get("session_name")
    model_id = data.get("model_id")
    owner_id = data.get("owner_id")

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
                "created_at": session.created_at,
                "updated_at": session.updated_at,
            }
        ),
        200,
    )  # 返回 200 成功响应

# 根据session_id获取包含在这个session下的所有log记录
@chat_sys.route("/get_logs", methods=["GET"])
def get_logs():
    session_id = request.args.get("session_id")

    if not session_id:
        return jsonify({"error": "session_id is required"}), 401

    # 查找会话对象，确保它存在
    session = Session.query.get(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 401

    # 使用 session.logs 获取该会话的所有日志
    logs = session.logs  # 直接通过 Session 实例的 logs 属性访问关联的日志

    # 格式化日志为列表
    log_data = [
        {
            "id": log.id,
            "role": log.role,
            "message": log.message,
            "time": log.time,
        }
        for log in logs
    ]

    return jsonify(log_data), 200  # 返回会话日志



@chat_sys.route("/create_log", methods=["POST"])
def create_log():
    data = request.get_json()  # 获取客户端传来的 JSON 数据

    # 从 JSON 数据中获取相关字段
    session_id = data.get("session_id")
    role = data.get("role")
    message = data.get("message")

    # 检查必填字段
    if not session_id or not role or not message:
        return jsonify({"error": "session_id, role, and message are required"}), 401

    # 查找会话对象，确保它存在
    session = Session.query.get(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 401

    # 创建新的日志对象
    new_log = Log(
        session_id=session_id,
        role=role,
        message=message,
        time=datetime.datetime.now(datetime.timezone.utc)  # 设置日志时间为当前时间
    )

    # 将新日志保存到数据库
    db.session.add(new_log)
    db.session.commit()

    return jsonify(
        {
            "id": new_log.id,
            "session_id": new_log.session_id,
            "role": new_log.role,
            "message": new_log.message,
            "time": new_log.time,
        }
    ), 200  # 成功创建日志，返回日志信息