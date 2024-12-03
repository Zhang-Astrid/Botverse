import datetime
from flask import Blueprint, request, jsonify
from models import db, User, Model
from sqlalchemy.exc import SQLAlchemyError
import pytz

timezone = pytz.timezone("Asia/Shanghai")
admin_sys = Blueprint("admin_sys", __name__)


# 确保只有管理员可以访问这些路由
def is_admin(user_id):
    user = User.query.get(user_id)
    return user and user.isAdmin


@admin_sys.route("/eval_and_click", methods=["POST"])
def eval_and_click():
    data = request.get_json()

    modelid = data.get("model_id")
    add_good_eval = data.get("add_good_eval")
    add_bad_eval = data.get("add_bad_eval")
    add_heat = data.get("add_heat")

    model: Model = Model.query.get(modelid)

    if add_good_eval:
        model.good_eval = model.good_eval + add_good_eval
    if add_bad_eval:
        model.bad_eval = model.bad_eval + add_bad_eval
    if add_heat:
        model.heat = model.heat + add_heat

    try:
        db.session.commit()
        return (
            jsonify(
                {
                    "message": "success!",
                }
            ),
            200,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 401


@admin_sys.route("/model", methods=["POST"])
def model():
    data = request.get_json()

    modelid = data.get("model_id")
    # 获取当前登录用户的所有信息，排除 id 和 isAdmin

    model: Model = Model.query.filter_by(id=modelid).first()

    if not model:
        return jsonify({"error": "Model does not exit!"}), 401
    # 返回用户信息，排除 id 和 isAdmin 字段
    user: User = User.query.filter_by(id=model.owner_id).first()

    model_info = {
        "model_name": model.model_name,
        "model_type": model.model_type,
        "owner_id": model.owner_id,
        "owner_name": user.username,
        "cost": model.cost,
        "prompt": model.prompt,
        "content": model.content,
        "created_at": model.created_at,
        "good_eval": model.good_eval,
        "bad_eval": model.bad_eval,
        "heat": model.heat,
    }

    return jsonify(model_info), 200


# 添加一个新的模型（机器人）
@admin_sys.route("/add_model", methods=["POST"])
def add_model():
    data = request.get_json()

    # 获取当前用户ID
    user_id = data.get("user_id")
    model_name = data.get("model_name")
    model_type = data.get("model_type")
    prompt = data.get("prompt")
    content = data.get("content")

    cost = 0
    if is_admin(user_id):
        cost = data.get("cost", 0)
    else:
        cost = 100

    # 检查必填字段
    if not model_name or user_id is None or not model_type:
        return (
            jsonify({"error": "user_id, model_name and model_type are required"}),
            401,
        )

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
        prompt=prompt,
        content=content,
        created_at=datetime.datetime.now(timezone),
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
@admin_sys.route("/update_model", methods=["POST"])
def update_model():
    data = request.get_json()

    # 获取管理员的用户ID

    model_id = data.get("model_id")
    new_cost = data.get("new_cost")
    new_model_name = data.get("new_model_name")
    new_model_type = data.get("new_model_type")
    increament = data.get("increament")

    if not model_id:
        return jsonify({"error": "model_id and new_cost are required"}), 401

    # 查找模型
    model: Model = Model.query.get(model_id)

    if not model:
        return jsonify({"error": "Model not found"}), 401

    # 更新模型的 cost
    if new_cost:
        model.cost = new_cost

    if new_model_name:
        model.model_name = new_model_name

    if new_model_type:
        model.model_type = new_model_type

    if increament:
        model.earning = model.earning + increament
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


@admin_sys.route("/get_all_users_model", methods=["POST"])
def get_all_users_model():
    # 获取请求中的 model_id

    # 查找模型
    models = Model.query.filter(Model.owner_id > 0).all()

    # 格式化返回数据
    model_data = [
        {
            "id": model.id,
            "name": model.model_name,
            "type": model.model_type,
            "cost": model.cost,
            "owner": User.query.get(model.owner_id).username,
            "prompt": model.prompt,
            "earning": model.earning,
            "created_at": model.created_at,
            "heat": model.heat,
        }
        for model in models
    ]

    # 返回模型列表
    return jsonify(model_data), 200  # 返回 200 成功响应


@admin_sys.route("/get_all_users", methods=["POST"])
def get_all_users():
    # 查找所有用户
    users = User.query.filter(User.id > 0).all()

    # 格式化返回数据
    user_data = [
        {
            "user_id": user.id,
            "username": user.username,
            "gender": user.gender,
            "birthday": user.birthday,
            "image": user.image,
            "score": user.score,
        }
        for user in users
    ]

    # 返回模型列表
    return jsonify(user_data), 200  # 返回 200 成功响应


@admin_sys.route("/delete_model", methods=["POST"])
def delete_model():
    data = request.get_json()

    # 获取管理员或模型拥有者的用户ID
    user_id = data.get("user_id")  # 用户ID（可以是管理员ID或模型的所有者ID）
    model_id = data.get("model_id")  # 要删除的模型ID

    if not model_id or user_id is None:
        return (
            jsonify(
                {"error": f"user_id {user_id} and model_id {model_id} are required"}
            ),
            401,
        )

    # 查找模型
    model = Model.query.get(model_id)

    # 如果模型不存在，返回错误
    if not model:
        return jsonify({"error": "Model not found"}), 401

    if not is_admin(user_id) and int(model.owner_id) != int(user_id):
        return (
            jsonify(
                {
                    "error": "Unauthorized access. You must be the owner or an admin to delete this model."
                }
            ),
            401,
        )

    # 删除模型
    try:
        db.session.delete(model)
        db.session.commit()
        return (
            jsonify(
                {"message": f"Model with id {model_id} has been deleted successfully."}
            ),
            200,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 401


@admin_sys.route("/get_models_by_user", methods=["POST"])
def get_models_by_user():
    # 从请求的 JSON 数据中获取 user_id
    data = request.get_json()
    user_id = data.get("user_id")

    # 检查 user_id 是否存在
    if user_id is None:
        return jsonify({"error": "user_id is required"}), 401  # 返回 401 错误

    # 查找该用户是否存在
    user = User.query.get(user_id)
    if not user:
        return (
            jsonify({"error": "User not found"}),
            401,
        )  # 如果用户不存在，返回 401 错误

    # 获取该用户所有的模型
    models = Model.query.filter_by(owner_id=user_id).all()
    if user_id == 0:
        print(1)
        # 格式化返回数据
        model_data = [
            {
                "id": model.id,
                "name": model.model_name,
                "type": model.model_type,
                "cost": model.cost,
                "prompt": model.prompt,
                "earning": model.earning,
            }
            for model in models
        ]
    else:
        print(0)
        model_data = [
            {
                "id": model.id,
                "name": model.model_name,
                "type": model.model_type,
                "cost": model.cost,
                "prompt": model.prompt,
            }
            for model in models
        ]
    # 返回模型列表
    return jsonify(model_data), 200  # 返回 200 成功响应
