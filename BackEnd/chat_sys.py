from datetime import datetime
from flask import Blueprint, request, jsonify

from functions import simple_chat
from models import db, Model, User, Session  # 导入SQLAlchemy的db和模型

chat_sys = Blueprint('chat_sys', __name__)


@chat_sys.route('/create_session',methods=["POST"])
def create_session():
    data = request.get_json()  # 获取客户端传来的 JSON 数据
    
    # 从 JSON 数据中获取相关字段
    session_name = data.get("session_name")
    model_id = data.get("model_id")
    owner_id = data.get("owner_id")
    logs = data.get("logs", [])  # 如果没有日志字段，则默认为空数组

    # 检查必填字段
    if not session_name or not model_id or not owner_id:
        return jsonify({"error": "session_name, model_id, and owner_id are required"}), 401  # 修改为 401 错误码
    
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
        created_at=datetime.now(datetime.timezone.utc)  # 设置创建时间为当前时间
    )
    
    # 将新会话保存到数据库
    db.session.add(new_session)
    db.session.commit()
    
    return jsonify({
        "id": new_session.id,
        "session_name": new_session.session_name,
        "model_id": new_session.model_id,
        "owner_id": new_session.owner_id,
        "created_at": new_session.created_at
    }), 200  # 修改为 200 成功响应


