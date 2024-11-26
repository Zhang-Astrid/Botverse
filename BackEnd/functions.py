import requests
import json


def simple_chat(model: str, msg: str, background: str) -> str:
    """
    model: 模型的名称\n
    msg: 当前的消息\n
    background: 背景消息
    """
    url = "https://api.aiproxy.io/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer sk-iiEY0IByanFKFqpERT27TwkauSK7GOrIgLKCIANsuiAiDGMI",  # 替换 $AIPROXY_API_KEY 为实际的API Key
    }

    # 请求的payload
    data = {
        "model": f"{model}",
        "messages": [
            {"role": "system", "content": f"{background}"},
            {"role": "user", "content": f"{msg}"},
        ],
        "stream": True,
    }

    # 发送POST请求
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # 打印响应内容
    print(response.json())
