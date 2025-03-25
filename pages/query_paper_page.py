import streamlit as st

from utils.call_workflow import call_workflow_with_input

# 查询论文页面
def query_paper_page():
    message = st.text_input("请输入你想查询的论文")
    if st.button("提交"):  # 添加提交按钮
        if message:
            # 使用 st.spinner 显示提示文字
            with st.spinner('正在查询，请耐心等待...') as spinner:
                try:
                    result = call_workflow_with_input(message, "app-uFK7vFs0DvH7bzN1AMGj0OUB")
                    st.write(result)
                except Exception as e:
                    spinner.empty()  # 确保在异常情况下也能关闭 spinner
                    st.error(f"生成失败: {str(e)}")
        else:
            st.warning("请输入内容后再提交！")  # 如果未输入内容，提示用户