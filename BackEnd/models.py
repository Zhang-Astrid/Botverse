# 数据库模型
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import (
    JSON,
)  # 使用 PostgreSQL 的 JSON 类型，如果不是 PostgreSQL，也可以用 Text
import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(10))
    birthday = db.Column(db.Date)
    isAdmin = db.Column(db.Boolean, default=False)

    # 定义用户创建的所有会话的关系
    bel_sessions = db.relationship("Session", backref="owner", lazy=True)
    bel_models = db.relationship("Model", backref="owner", lazy=True)

class Model(db.Model):
    __tablename__ = "models"
    id = db.Column(db.Integer, primary_key=True)  # Model 的编号
    model_name = db.Column(db.String(150), nullable=False)  # Model 的名字
    owner_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # 外键，链接到 User 表
    paras = db.Column(JSON, nullable=True)


class Session(db.Model):
    __tablename__ = "sessions"  # 明确表名
    id = db.Column(db.Integer, primary_key=True)  # Session 的编号
    session_name = db.Column(db.String(150), nullable=False)  # Session 的名字
    model_id = db.Column(
        db.Integer, db.ForeignKey("models.id"), nullable=False
    )  # 使用的模型编号
    owner_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # 外键，链接到 User 表
    logs = db.Column(JSON, nullable=True)  # JSON 数组存储日志
    created_at = db.Column(
        db.DateTime, default=datetime.datetime.now(datetime.timezone.utc)
    )  # 会话创建时间



