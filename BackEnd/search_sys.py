from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from models import db, User, Model
import yaml

# 创建蓝图
search_sys = Blueprint("search_sys", __name__)


@search_sys.route("/search_model", methods=["POST"])
def search_model():
    data = request.get_json()
    hint = data.get("hint")

    query = Model.query.filter(Model.model_name.ilike('%' + hint + '%'))

    # 执行查询
    results = query.all()

    model_info = [
        {
            "model_name": model.model_name,
            "model_type": model.model_type,
            "cost": model.cost,
            "prompt": model.prompt,
            "content": model.content,
        }
        for model in results
    ]

    return jsonify(model_info), 200


@search_sys.route("/search_user", methods=["POST"])
def search_user():
    data = request.get_json()
    hint = data.get("hint")

    query = User.query.filter(User.username.ilike('%' + hint + '%'))

    # 执行查询
    results = query.all()

    user_info = [
        {
            "user_name": user.username,
            "gender": user.gender,
            "birthday": user.birthday,
            "image": user.image,
        }
        for user in results
    ]

    return jsonify(user_info), 200



