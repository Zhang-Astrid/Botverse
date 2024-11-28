from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models import db, User


store_sys = Blueprint("store_sys", __name__)


# 更改积分
@store_sys.route("/update", methods=["POST"])
def update():
    data = request.get_json()

    username = data.get("username")
    increament = data.get("increament")

    user: User = User.query.filter_by(username=username).first()

    if user.score < 0 and increament < 0:
        return (
            jsonify(
                {"message": "The score is less or equal than zero, please buy first!"}
            ),
            401,
        )

    user.score = user.score + int(increament)

    # 提交更改
    try:
        db.session.commit()  # 提交更改到数据库
        return (
            jsonify(
                {
                    "message": "User score updated successfully!",
                    "score": f"{user.score}",
                }
            ),
            200,
        )
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Failed to update user score."}), 401


# 查询积分
@store_sys.route("/score", methods=["GET"])
def score():
    data = request.get_json()

    username = data.get("username")

    user: User = User.query.filter_by(username=username).first()

    user_info = {
        "score": user.score,
    }

    return jsonify(user_info), 200
