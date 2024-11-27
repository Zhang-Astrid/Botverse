from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from models import db, User

# 创建蓝图
user_sys = Blueprint("user_sys", __name__)

# 初始化 Bcrypt
bcrypt = Bcrypt()


# 注册用户
@user_sys.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # 获取请求的用户名和密码
    username = data.get("username")
    password = data.get("password")
    gender = data.get("gender")
    birthday = data.get("birthday")

    # 密码加密
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    # 创建用户
    new_user = User(
        username=username, password=hashed_password, gender=gender, birthday=birthday
    )
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully!"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Username already exists!"}), 401


# 登录用户
@user_sys.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # 获取请求的用户名和密码
    username = data.get("username")
    password = data.get("password")

    # 查找用户
    user = User.query.filter_by(username=username).first()
    print(username)
    if user and bcrypt.check_password_hash(user.password, password):
        # 登录成功，将用户 ID 存储在 session 中
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"message": "Invalid username or password."}), 401


# 获取用户信息
@user_sys.route("/user", methods=["GET"])
def user():
    data = request.get_json()

    username = data.get("username")
    # 获取当前登录用户的所有信息，排除 id 和 isAdmin
    user: User = User.query.filter_by(username=username).first()

    # 返回用户信息，排除 id 和 isAdmin 字段
    user_info = {
        "username": user.username,
        "gender": user.gender,
        "birthday": user.birthday,
        "image": user.image,
    }

    return jsonify(user_info), 200


# 修改用户信息
@user_sys.route("/update", methods=["POST"])
def update_user():

    # 获取请求数据
    data = request.get_json()

    user_id= data.get("user_id")
    username = data.get("username")
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    gender = data.get("gender")
    birthday = data.get("birthday")
    image = data.get("image")

    # 查找当前登录用户
    user: User = User.query.filter_by(id=user_id).first()

    # 检查旧密码是否正确
    if not bcrypt.check_password_hash(user.password, old_password):
        return jsonify({"message": "Old password is incorrect."}), 401

    # 修改密码（如果提供了新密码）
    if new_password:
        hashed_new_password = bcrypt.generate_password_hash(new_password).decode(
            "utf-8"
        )
        user.password = hashed_new_password

    # 修改性别（如果提供了性别）
    if gender:
        user.gender = gender

    # 修改生日（如果提供了生日）
    if birthday:
        user.birthday = birthday

    if image:
        user.image = image

    # 提交更改
    try:
        db.session.commit()  # 提交更改到数据库
        return jsonify({"message": "User information updated successfully!"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Failed to update user information."}), 401
