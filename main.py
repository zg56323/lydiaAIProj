import streamlit as st

from pages.chat_page import chat_page
from pages.faq_or_message_page import faq_or_message_page
from pages.knowledge_graph_page import knowledge_graph_page
from pages.login_page import login_page
from pages.query_paper_page import query_paper_page

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
# 主函数
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_page()
    else:
        # 初始化默认页面
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "聊天"

        # 创建顶部导航栏
        st.title("24小时智能学伴")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("💬 聊天"):
                st.session_state.current_page = "聊天"
        with col2:
            if st.button("📄 查询论文"):
                st.session_state.current_page = "查询论文"
        with col3:
            if st.button("📊 知识图谱"):
                st.session_state.current_page = "知识图谱"
        with col4:
            if st.button("📝 答疑或留言"):
                st.session_state.current_page = "答疑或留言"

        # 根据选择的页面显示内容
        page = st.session_state.current_page
        if page == "聊天":
            chat_page()
        elif page == "查询论文":
            query_paper_page()
        elif page == "知识图谱":
            knowledge_graph_page()
        elif page == "答疑或留言":
            faq_or_message_page()


if __name__ == "__main__":
    main()
