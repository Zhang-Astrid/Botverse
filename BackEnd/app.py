from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from user_sys import user_sys  # 导入 login_sys 蓝图
from models import db

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  # 用于加密会话
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:200516@localhost/login_system"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
bcrypt = Bcrypt(app)

# 注册蓝图
app.register_blueprint(user_sys, url_prefix="/user_sys")  # 将蓝图注册到主应用


# with app.app_context():
#     db.create_all()  # 创建所有定义的表
#     print("Users table created.")

if __name__ == "__main__":
    app.run(debug=True, port=8080)
