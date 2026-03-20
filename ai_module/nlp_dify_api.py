import json
import requests
import time
from utils import config_util as cfg
from utils import util


def question(cont):
    print(cfg)
    print(cfg.dify_base_url)
    print(cfg.dify_api_key)
    url = f"http://{cfg.dify_base_url}/v1/chat-messages"
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {cfg.dify_api_key}",
        "Content-Type": "application/json",
    })
    body = {
        "query": cont,
        "response_mode": "blocking",
        "user": "user-123",
        "inputs": {}



    }

    starttime = time.time()

    try:
        resp = session.post(url, json=body)
        resp.raise_for_status()
        data = resp.json()
        # Dify Chatflow 的标准回复里，answer 字段或 choices 列表都可能
        answer = data.get("answer")
        if answer is None and "choices" in data:
            answer = data["choices"][0].get("message", {}).get("content")
        response_text = answer

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        response_text = "抱歉，我现在太忙了，休息一会，请稍后再试。"
    util.log(1, "接口调用耗时 :" + str(time.time() - starttime))
    return response_text.strip()


if __name__ == "__main__":
    for i in range(3):
        query = "爱情是什么"
        response = question(query)
        print("\n The result is ", response)