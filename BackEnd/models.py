# 数据库模型
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import (
    JSON,
)  # 使用 PostgreSQL 的 JSON 类型，如果不是 PostgreSQL，也可以用 Text
import datetime

db = SQLAlchemy()


class User(db.Model):
    """
    user的表格

    :param id: 用户id，唯一数字，自动生成
    :param username: 用户名字，不能重复，每个用户得不一样
    :param password: 用户密码，这里是储存加密后的字符串
    :param gender: 性别，有male和female两种选项
    :param birthday: 生日，用Date形式储存
    :param isAdmin: 是否为管理员，boolean形式储存
    :param score: 用户的积分，积分用于机器人聊天时的开销
    :param bel_sessions: 用户创建的会话，在register的时候不需要传入这个参数
    :param bel_models: 用户创建的模型，在register的时候不需要传入这个参数
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(10))
    birthday = db.Column(db.Date)
    isAdmin = db.Column(db.Boolean, default=False)

    score = db.Column(db.Integer, default=0)

    # 定义用户创建的所有会话的关系
    bel_sessions = db.relationship("Session", backref="owner", lazy=True)
    bel_models = db.relationship("Model", backref="owner", lazy=True)


class Model(db.Model):
    """
    model的表格

    :param id: 唯一编号，自动生成
    :param model_name: 模型的名字，可以重复
    :param owner_id: 模型的创造者的id
    :param cost: 模型生成每个token需要用户支付的积分
    :param paras: 这是一个json变量，表示额外传入的参数，用以用户自定义模型，比如："type"(表示自定义模型是用来图片、翻译等其他功能)、"promopt"(给模型预先设置的提示词)等等
    """

    __tablename__ = "models"
    id = db.Column(db.Integer, primary_key=True)  # Model 的编号
    model_name = db.Column(db.String(150), unique=True, nullable=False)  # Model 的名字
    owner_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # 外键，链接到 User 表
    cost = db.Column(db.Integer, default=0)  # cost 每token

    paras = db.Column(JSON, nullable=True)  # paras为None 是默认机器人，否则是用户自定义


class Session(db.Model):
    """
    session的表格

    :param id: 唯一编号，自动生成
    :param session_name: session的名字
    :param modei_id: session使用的模型编号
    :param owner_id: session的创建者编号
    :param created_at: session创建的时间 用datetime记录
    :param logs: session所关联的所有log class 创建时不需要传入此参数
    """

    __tablename__ = "sessions"  # 明确表名
    id = db.Column(db.Integer, primary_key=True)  # Session 的编号
    session_name = db.Column(db.String(150), nullable=False)  # Session 的名字
    model_id = db.Column(
        db.Integer, db.ForeignKey("models.id"), nullable=False
    )  # 使用的模型编号
    owner_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # 外键，链接到 User 表
    created_at = db.Column(
        db.DateTime, default=datetime.datetime.now(datetime.timezone.utc)
    )  # 会话创建时间

    logs = db.relationship("Log", backref="session", lazy=True)

class Log(db.Model):
    """
    Log的表格

    :param id: 唯一编号，自动生成
    :param session_id: 所属的session的编号
    :param time: log的记录时间
    :param role: 发送log的角色，可能是 "model_name" 或 "user_name"
    :param message: log的内容
    """
    __tablename__ = "logs"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False)  # 外键，关联到Session
    time = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    role = db.Column(db.String(50))  # 角色，可能是 "model_name" 或 "user_name"
    message = db.Column(db.Text)
