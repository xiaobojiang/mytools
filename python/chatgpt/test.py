import openai
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_base = 'https://aicedev.openai.azure.com/'  # Your Azure OpenAI resource's endpoint value.


openai.api_key  = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, engine="chatgpt35"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        engine=engine,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

text = """
    User:> "你好",
    Assistant:> "你好！有什么我可以帮助你的吗？"
    User:> "你是谁",
    Assistant:> "我是一个客服聊天机器人，专门为WiZ智能灯系统提供帮助和支持。如果您有任何关于WiZ智能灯系统的问题，请随时问我。"
    User:> "我的灯好像坏了",
    Assistant:> "很抱歉听到这个问题。您能否提供更多细节信息，例如灯的型号和问题的具体表现？这样我才能更好地帮助您解决问题。"
    User:> "我的灯在闪烁着紫色的光",
    Assistant:> "当灯处于“手动设置”模式并发出Wi-Fi信号时，它应该会闪烁紫色光。请打开手机的Wi-Fi设置并连接到Wi-Fi：“WiZConfig_XXXX”。一旦手机连接到WiZ灯发出的Wi-Fi，返回WiZ应用程序并等待过程完成。请注意，某些手机在连接到没有互联网连接的Wi-Fi时可能需要确认。如果您尝试了这些确切的步骤2或3次后仍然遇到问题，请使用应用内聊天联系我们的支持团队，并告诉我们您在哪个步骤遇到问题。我们会尽快回复您。"
    User:> "好的，谢谢",
    Assistant:> "不客气，有其他问题可以随时问我。"
    User:> "我的遥控器好像很烫，有点不正常",
    Assistant:> "很抱歉听到这个问题。Wi-Fi WiZmote使用Wi-Fi与单个房间的灯进行通信。如果您的墙壁非常厚，会完全阻止Wi-Fi信号，这可能会导致Wi-Fi WiZmote过热。如果您的Wi-Fi WiZmote过热，请将其放置在通风良好的地方，以便它可以冷却。如果您的Wi-Fi WiZmote仍然过热，请联系我们的支持团队以获取更多帮助。"
    User:> "请把上面的回答翻译成英文"
"""

prompt = f"""
Your task is to perform the following actions: 
1 - extract core inputs of user in following text delimited by tripple backticks, in the text, text after User:> is user inputs, and Assistance:> is previous replies.
2 - print the last user input
3 - print the last assistant reply 
4 - is the last user input a follow up to previous assistant reply
5 - print the last extracted input topic


Use the following format:
topics: <core topics>
last user input: <last user input>
last assistant reply: <last assistant reply>
is follow up: <yes or no>
last topic: <last topic>


Text: ```{text}```
"""
response = get_completion(prompt)
print("\nCompletion for prompt 2:")
print(response)