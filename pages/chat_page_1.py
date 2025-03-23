import streamlit as st

from config.config import API_KEY
from utils.call_workflow import call_workflow_with_input


def chat_page_1():
    st.write("### 知识解答")
    # 固定输入框在标题下方
    input_container = st.container()
    with input_container:
        if prompt := st.chat_input("请输入你的问题"):
            # 添加用户消息
            st.session_state.messages.append({"role": "user", "content": prompt})
            # 添加临时助理消息
            st.session_state.messages.append({"role": "assistant", "content": None})

    # 初始化对话历史
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 消息显示区域（在输入框下方）
    messages_container = st.container()
    with messages_container:
        for i, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                # 处理临时状态
                if message["content"] is None:
                    # 显示加载状态并获取结果
                    placeholder = st.empty()
                    placeholder.markdown("⏳ 正在思考中...")
                    try:
                        result = call_workflow_with_input(st.session_state.messages[i-1]["content"], API_KEY)
                        placeholder.markdown(result)
                        message["content"] = result  # 更新消息内容
                    except Exception as e:
                        placeholder.error(str(e))
                        message["content"] = f"错误：{str(e)}"
                else:
                    st.markdown(message["content"])
