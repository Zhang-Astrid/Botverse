# 数据库模型
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import (
    JSON,
)  # 使用 PostgreSQL 的 JSON 类型，如果不是 PostgreSQL，也可以用 Text
import datetime
import pytz

timezone = pytz.timezone("Asia/Shanghai")

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
    :param image: 用户头像地址
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(10))
    birthday = db.Column(db.Date)
    isAdmin = db.Column(db.Boolean, default=False)
    image = db.Column(db.String(255))

    score = db.Column(db.Integer, default=0)

    # 定义用户创建的所有会话的关系
    bel_sessions = db.relationship(
        "Session", backref="owner", lazy=True, cascade="all, delete"
    )
    bel_models = db.relationship(
        "Model", backref="owner", lazy=True, cascade="all, delete"
    )


class Model(db.Model):
    """
    model的表格

    :param id: 唯一编号，自动生成
    :param model_name: 模型的名字，可以重复
    :param model_type: 模型的型号 内置的LLM模型
    :param owner_id: 模型的创造者的id
    :param cost: 模型生成每个token需要用户支付的积分
    :param prompt: 模型的提示词
    :param content: 模型的介绍
    :param earning: 模型的利润
    :param created_at: 模型的创建时间
    :param good_eval: 模型的好评数量
    :param bad_eval: 模型的差评数量
    :param heat: 模型的热度
    """

    __tablename__ = "models"
    id = db.Column(db.Integer, primary_key=True)  # Model 的编号
    model_name = db.Column(db.String(150), nullable=False)  # Model 的名字
    model_type = db.Column(db.String(150), nullable=False)  # Model 的型号
    owner_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # 外键，链接到 User 表
    cost = db.Column(db.Integer, default=0)  # cost 每token
    prompt = db.Column(db.Text)
    content = db.Column(db.Text)
    earning = db.Column(db.Integer, default=0)
    
    created_at= db.Column(db.DateTime, default=datetime.datetime.now(timezone))
    good_eval= db.Column(db.Integer, default=0)
    bad_eval = db.Column(db.Integer, default=0)
    heat = db.Column(db.Integer, default=0)


class Session(db.Model):
    """
    session的表格

    :param id: 唯一编号，自动生成
    :param sub_id: session的子id
    :param session_name: session的名字
    :param modei_id: session使用的模型编号
    :param owner_id: session的创建者编号
    :param created_at: session创建的时间 用datetime记录
    :param logs: session所关联的所有log class 创建时不需要传入此参数
    """

    __tablename__ = "sessions"  # 明确表名
    id = db.Column(db.Integer, primary_key=True)  # Session 的编号
    sub_id = db.Column(db.Integer, default=0)
    session_name = db.Column(db.String(150), nullable=False)  # Session 的名字
    model_id = db.Column(
        db.Integer, db.ForeignKey("models.id"), nullable=False
    )  # 使用的模型编号
    owner_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # 外键，链接到 User 表
    created_at = db.Column(
        db.DateTime, default=datetime.datetime.now(timezone)
    )  # 会话创建时间

    logs = db.relationship("Log", backref="session", lazy=True, cascade="all, delete")


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
    session_id = db.Column(
        db.Integer, db.ForeignKey("sessions.id"), nullable=False
    )  # 外键，关联到Session
    time = db.Column(db.DateTime, default=datetime.datetime.now(timezone))
    role = db.Column(db.String(50))  # 角色，可能是 "model_name" 或 "user_name"
    message = db.Column(db.Text)


class Comment(db.Model):
    """
    评论的表格

    :param id: 唯一编号，自动生成
    :param sender_id: 发送者的用户id
    :param target_id: 被评论对象的id，可以是 session_id 或 model_id，根据需求决定
    :param content: 评论的内容
    :param created_at: 评论的创建时间
    :param has_read: 是否被对象或者对象的所有者阅读
    """

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)  # 评论的编号
    sender_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # 发送者的用户id
    target_id = db.Column(
        db.Integer, nullable=False
    )  # 被评论对象的id，可以是 session_id 或 model_id
    content = db.Column(db.Text, nullable=False)  # 评论内容
    created_at = db.Column(
        db.DateTime, default=datetime.datetime.now(timezone)
    )  # 评论创建时间

    # 如果 target_id 关联的是 session 或 model，可以分别定义对应的关系
    # 可以选择使用`target_type`来标识评论的目标是 session 还是 model
    target_type = db.Column(
        db.String(50), nullable=False
    )  # 目标类型，可能是 'model' 或 'user'

    has_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Comment id={self.id} sender_id={self.sender_id} target_id={self.target_id} content={self.content[:20]}>"


class Post(db.Model):
    """
    Post的表格

    :param id: 唯一编号，自动生成
    :param title: 帖子的标题
    :param owner_id: 帖子创建者的用户ID
    :param target_id: 帖子对象的id，可以是model 或者 user
    :param created_at: 帖子创建时间
    :param logs: 帖子关联的所有日志
    :param hasRead: 是否被对象或者对象的所有者阅读
    :param content: 帖子的描述
    """

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)  # 帖子编号
    title = db.Column(db.String(255), nullable=False)  # 帖子的标题
    content = db.Column(db.Text)
    owner_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # 创建者的用户ID
    created_at = db.Column(
        db.DateTime, default=datetime.datetime.now(timezone)
    )  # 创建时间

    target_id = db.Column(
        db.Integer, nullable=False
    )  # 被发帖对象的id，可以是 session_id 或 model_id

    # 如果 target_id 关联的是 session 或 model，可以分别定义对应的关系
    # 可以选择使用`target_type`来标识评论的目标是 session 还是 model
    target_type = db.Column(
        db.String(50), nullable=False
    )  # 目标类型，可能是 'model' 或 'user'

    logs = db.relationship(
        "PostLog", backref="post", lazy=True, cascade="all, delete"
    )  # 关联到 PostLog 类

    has_read = db.Column(db.Boolean, default=False)


class PostLog(db.Model):
    """
    PostLog的表格

    :param id: 唯一编号，自动生成
    :param post_id: 所属帖子的编号
    :param time: 日志记录时间
    :param sender_id: 发送者的id
    :param message: 日志的内容
    """

    __tablename__ = "post_logs"

    id = db.Column(db.Integer, primary_key=True)  # 日志编号
    post_id = db.Column(
        db.Integer, db.ForeignKey("posts.id"), nullable=False
    )  # 关联到 Post
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(timezone))  # 记录时间
    sender_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # 发送者的用户id  
    message = db.Column(db.Text)  # 日志内容
