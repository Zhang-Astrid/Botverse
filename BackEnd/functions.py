import requests
from flask import Response,jsonify
import json
from openai import OpenAI

client = OpenAI(
    #将这里换成你在aiproxy api keys拿到的密钥
    api_key="sk-iiEY0IByanFKFqpERT27TwkauSK7GOrIgLKCIANsuiAiDGMI",
    # 这里将官方的接口访问地址，替换成aiproxy的入口地址
    base_url="https://api.aiproxy.io/v1"
)

def simple_chat(model: str, msg: str, background: str):
    """
    model: 模型的名称\n
    msg: 当前的消息\n
    background: 背景消息
    """
    completion = client.chat.completions.create(
        model=f"{model}",
        messages=[
            {"role": "system", "content": f"{background}"},
            {"role": "user", "content": f"{msg}"}
        ],
        stream_options={"include_usage": True},
        stream=True
    )

    def generate():
        for chunk in completion:
            # 提取模型的生成结果
            delta = chunk.choices[0].delta
            data={}
            if hasattr(delta, "content"):  # 如果有内容返回
                data["message"]=delta.content

            if not chunk.usage is None:
                data["tokens"]=chunk.usage.total_tokens
            yield jsonify(data).data  # 持续传送数据

    # 使用 Flask 的 Response 对象来流式输出
    return Response(generate(), content_type='application/json')

