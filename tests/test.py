from utils.call_workflow import call_workflow_with_input
import streamlit as st
# 模拟用户输入
user_input = "波动光学多少知识点"
response_mode =  "blocking"
st.session_state['user'] = "gavin"
# 测试 call_workflow_with_input 方法
try:
    print("正在发送 POST 请求...")
    result = call_workflow_with_input(user_input, response_mode=response_mode)
    print("API 返回的结果:", result)
except Exception as e:
    print("测试失败:", str(e))
