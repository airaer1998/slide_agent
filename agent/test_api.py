from openai import OpenAI

client = OpenAI(
    base_url="http://35.220.164.252:3888/v1/",
    api_key="sk-CnqCf4NENTwZwLLQJwPuH4ZZ1uIGIRJSyTStRkSXNV1Hb2Kj"
)

response = client.chat.completions.create(
    model="moonshotai/kimi-k2",
    messages=[
        {
            "role": "user",
            "content":"自我介绍一下",
        }
    ],
    temperature = 1 # 自行修改温度等参数
)

print(response.choices[0].message.content)

json_response = client.chat.completions.create(
    model="moonshotai/kimi-k2",
    messages=[
        {
            "role": "user",
            "content": "请以JSON格式返回一个包含姓名、年龄、职业和爱好的个人信息示例"
        }
    ],
    temperature=0.7,
    response_format={"type": "json_object"}  # 强制JSON格式输出
)

print(json_response.choices[0].message.content)
