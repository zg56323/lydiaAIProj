import streamlit as st


# 知识图谱页面
def knowledge_graph_page():
    message = st.text_area("请输入你想查询的思维导图知识点")
    if st.button("提交"):  # 添加提交按钮
        if message:
            st.write(f"学号：{st.session_state['user']} 你的留言已提交")
            # 模拟调用 JavaScript 方法
            st.write("模拟调用 JavaScript 进行留言处理...")
        else:
            st.warning("请输入内容后再提交！")  # 如果未输入内容，提示用户