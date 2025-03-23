import streamlit as st
from mindMap.markmap import upload_markdown
from pages.query_paper_page import query_paper_page
from utils.call_workflow import call_workflow_with_input

# 模拟用户输入
user_input = "波动光学"
response_mode =  "blocking"
st.session_state['user'] = "gavin"
apikey = "app-uFK7vFs0DvH7bzN1AMGj0OUB"
# 测试 call_workflow_with_input 方法
try:
    print("正在发送 POST 请求...")
    result = call_workflow_with_input(user_input, "app-uFK7vFs0DvH7bzN1AMGj0OUB")
    print("API 返回的结果:", result)
except Exception as e:
    print("测试失败:", str(e))
