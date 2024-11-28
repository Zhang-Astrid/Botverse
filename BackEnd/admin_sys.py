from flask import Blueprint, request, jsonify
from models import db, User, Model
from sqlalchemy.exc import SQLAlchemyError

admin_sys = Blueprint("admin_sys", __name__)


# 确保只有管理员可以访问这些路由
def is_admin(user_id):
    user = User.query.get(user_id)
    return user and user.isAdmin


# 添加一个新的模型（机器人）
@admin_sys.route("/add_model", methods=["POST"])
def add_model():
    data = request.get_json()

    # 获取当前用户ID
    user_id = data.get("user_id")
    model_name = data.get("model_name")
    model_type = data.get("model_type")
    
    cost=0
    if is_admin(user_id):
        cost=data.get("cost",0)
    else:
        cost= 1000000

    # 检查必填字段
    if not model_name or not user_id or not model_type:
        return jsonify({"error": "user_id, model_name and model_type are required"}), 401

    # 检查用户是否存在
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 401

    # 如果是管理员，owner_id 设置为管理员自己的 ID，否则设置为当前用户的 ID
    owner_id = user_id  # 直接将 owner_id 设置为 user_id

    # 创建新的模型（机器人）
    new_model = Model(
        model_name=model_name,
        model_type=model_type,
        owner_id=owner_id,  # 设置为当前用户的 ID
        cost=cost,
    )

    # 添加到数据库
    try:
        db.session.add(new_model)
        db.session.commit()
        return (
            jsonify(
                {
                    "id": new_model.id,
                    "model_name": new_model.model_name,
                    "model_type": new_model.model_type,
                    "cost": new_model.cost,
                    "owner_id": new_model.owner_id,
                }
            ),
            200,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 401


# 修改模型的 cost
@admin_sys.route("/update_model_cost", methods=["POST"])
def update_model_cost():
    data = request.get_json()

    # 获取管理员的用户ID
    admin_user_id = data.get("admin_user_id")

    if not is_admin(admin_user_id):
        return jsonify({"error": "Unauthorized access. Admins only."}), 401

    model_id = data.get("model_id")
    new_cost = data.get("new_cost")

    if not model_id or new_cost is None:
        return jsonify({"error": "model_id and new_cost are required"}), 401

    # 查找模型
    model = Model.query.get(model_id)

    if not model:
        return jsonify({"error": "Model not found"}), 401

    # 更新模型的 cost
    model.cost = new_cost

    # 提交更改
    try:
        db.session.commit()
        return (
            jsonify(
                {
                    "id": model.id,
                    "model_name": model.model_name,
                    "model_type": model.model_type,
                    "cost": model.cost,
                    "owner_id": model.owner_id,
                }
            ),
            200,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 401


@admin_sys.route("/get_model", methods=["POST"])
def get_model():
    # 获取请求中的 model_id
    model_id = request.args.get("model_id")

    if not model_id:
        return (
            jsonify({"error": "model_id is required"}),
            401,
        )  # 如果没有提供 model_id，返回 401 错误

    # 查找模型
    model: Model = Model.query.get(model_id)

    if not model:
        return (
            jsonify({"error": "Model not found"}),
            401,
        )  # 如果没有找到模型，返回 401 错误

    # 返回模型的详细信息
    return (
        jsonify(
            {
                "id": model.id,
                "model_name": model.model_name,
                "model_type": model.model_type,
                "cost": model.cost,
                "owner_id": model.owner_id,
            }
        ),
        200,
    )  # 返回 200 成功响应


@admin_sys.route("/delete_model", methods=["POST"])
def delete_model():
    data = request.get_json()

    # 获取管理员或模型拥有者的用户ID
    user_id = data.get("user_id")  # 用户ID（可以是管理员ID或模型的所有者ID）
    model_id = data.get("model_id")  # 要删除的模型ID

    if not model_id or not user_id:
        return jsonify({"error": f"user_id {user_id} and model_id {model_id} are required"}), 401

    # 查找模型
    model = Model.query.get(model_id)

    # 如果模型不存在，返回错误
    if not model:
        return jsonify({"error": "Model not found"}), 401

    # 验证用户是否是管理员或该模型的所有者
    if not is_admin(user_id) and model.owner_id != user_id:
        return jsonify({"error": "Unauthorized access. You must be the owner or an admin to delete this model."}), 401

    # 删除模型
    try:
        db.session.delete(model)
        db.session.commit()
        return jsonify({"message": f"Model with id {model_id} has been deleted successfully."}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 401