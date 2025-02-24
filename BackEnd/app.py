from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from user_sys import user_sys  # 导入 login_sys 蓝图
from chat_sys import chat_sys
from store_sys import store_sys
from admin_sys import admin_sys
from comment_sys import comment_sys
from forum_sys import forum_sys
from search_sys import search_sys
from models import db
from flask_cors import CORS
import yaml

# 修改数据库配置

with open("BackEnd\infos.yaml", "r") as file:
    config = yaml.safe_load(file)
    file.close()

database_user = config["data_source"]["database_user"]
database_pwd = config["data_source"]["database_pwd"]
database_name = config["data_source"]["database_name"]

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  # 用于加密会话
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{database_user}:{database_pwd}@localhost/{database_name}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
bcrypt = Bcrypt(app)
CORS(app, origins="*")


# 注册蓝图
app.register_blueprint(user_sys, url_prefix="/user_sys")  # 将蓝图注册到主应用
app.register_blueprint(chat_sys, url_prefix="/chat_sys")
app.register_blueprint(store_sys, url_prefix="/store_sys")
app.register_blueprint(admin_sys, url_prefix="/admin_sys")
app.register_blueprint(comment_sys, url_prefix="/comment_sys")
app.register_blueprint(forum_sys, url_prefix="/forum_sys")
app.register_blueprint(search_sys, url_prefix="/search_sys")

with app.app_context():
    db.create_all()  # 创建所有定义的表
    print("Users table created.")

if __name__ == "__main__":
    app.run(debug=True, port=8080, threaded=True)
