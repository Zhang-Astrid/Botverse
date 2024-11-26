from flask import Blueprint, request, jsonify

from BackEnd.functions import simple_chat
from models import db, Model  # 导入SQLAlchemy的db和模型

chat_sys = Blueprint('chat_sys', __name__)


def check_model_available(id: int, model_name: str) -> bool:
    """
    Check if the user_model table contains a row with the given user_id and request_model.

    :param id: User ID
    :param model_name: Name of the model
    :return: True if the row exists, False otherwise.
    """
    # 查询user_model表
    record = Model.query.filter_by(id=id, model_name=model_name).first()
    return record is not None  # 如果记录存在，则返回True，否则返回False


@chat_sys.route('/send', methods=['POST'])
def send():
    """
    API endpoint to process a send request.
    """
    data = request.get_json()
    user_id = int(data['user_id'])
    request_model = data['request_model']
    model_background = data['model_background']
    a_request = data['a_request']

    # Check if the model is available for the user
    is_available = check_model_available(user_id, request_model)

    if is_available:
        return jsonify({"message": simple_chat(request_model,a_request,model_background)}), 200
    else:
        return jsonify({"message": "Model is not available."}),401
