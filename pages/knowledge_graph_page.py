import streamlit as st
from mindMap.markmap import upload_markdown
import streamlit.components.v1 as components
from utils.call_workflow import call_workflow_with_input

# 知识图谱页面
def knowledge_graph_page():
    message = st.text_input("请输入你想查询的思维导图知识点")
    if st.button("提交"):  # 添加提交按钮
        if message:
            # 使用 st.spinner 显示提示文字
            with st.spinner('正在生成，请耐心等待...') as spinner:
                try:
                    result = call_workflow_with_input(message, "app-nSodA3hYkxuBylg0l2HFmpKI")
                    filename = upload_markdown(result)
                    html_filename = "mindMap/static/html/" + filename.replace('.md', '.html')  # 修改：路径改为HTML

                    # 使用markmap生成的HTML文件
                    with open(html_filename, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    components.html(html_content, height=600)
                except Exception as e:
                    spinner.empty()  # 确保在异常情况下也能关闭 spinner
                    st.error(f"生成失败: {str(e)}")
        else:
            st.warning("请输入内容后再提交！")  # 如果未输入内容，提示用户