# -*- coding: utf-8 -*-
import requests


# Flask 应用的 API 端点
url = 'http://localhost:5000/api/send'

# 聊天消息数据
data = {
	'data': '{"username": "user1", "msg": "你好呀"}'
}

# 发送 POST 请求到聊天 API
response = requests.post(url, data=data)

# 打印响应结果
print(response.text)