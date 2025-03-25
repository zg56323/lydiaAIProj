import streamlit as st

from pages.chat_page import chat_page
from pages.faq_or_message_page import faq_or_message_page
from pages.knowledge_graph_page import knowledge_graph_page
from pages.login_page import login_page
from pages.learning_suggestions_page import learning_suggestions_page
from pages.political_education_page import political_education_page
from pages.query_paper_page import query_paper_page
from pages.test_page import test_page

st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        .stButton > button {
            margin-right: 5px; /* 增加按钮之间的水平间距 */
            margin-bottom: 5px; /* 增加按钮之间的垂直间距 */
            padding: 3px 3px; /* 调整按钮的内边距 */
            min-width: 50px; /* 设置最小宽度以防止按钮过小 */
            font-size: 10px; /* 减小按钮字体大小 */
            white-space: nowrap; /* 确保按钮中的文字不换行 */
        }
        .stContainer {
            padding: 20px; /* 增加容器的内边距 */
            width: 100%; /* 增加界面宽度 */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def display_pages():
    """根据当前页面显示相应的内容"""
    page = st.session_state.current_page
    if page == "知识讲解":
        chat_page()
    elif page == "相关论文":
        query_paper_page()
    elif page == "知识图谱":
        knowledge_graph_page()
    elif page == "答疑/留言":
        faq_or_message_page()
    elif page == "题目自测":
        test_page()
    elif page == "学习建议":
        learning_suggestions_page()
    elif page == "思政案例":
        political_education_page()
    else:
        st.error("未知页面")

def main():
    # 初始化登录状态
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # 如果未登录，显示登录页面
    if not st.session_state.logged_in:
        login_page()
    else:
        # 初始化默认页面
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "知识讲解"
        st.markdown("<h3 style='font-weight: bold;'>医理智驭教辅</h3>", unsafe_allow_html=True)

        # 使用 st.container 来包裹内容，并增加内边距
        with st.container():
            col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

            with col1:
                if st.button("💡 知识讲解", key="chat_button"):
                    st.session_state.current_page = "知识讲解"

            with col2:
                if st.button("📄 相关论文", key="query_paper_button"):
                    st.session_state.current_page = "相关论文"

            with col3:
                if st.button("📊 知识图谱", key="knowledge_graph_button"):
                    st.session_state.current_page = "知识图谱"

            with col4:
                if st.button("📝 答疑/留言", key="faq_or_message_button"):
                    st.session_state.current_page = "答疑/留言"

            with col5:
                if st.button("✍️ 题目自测", key="test_button"):
                    st.session_state.current_page = "题目自测"

            with col6:
                if st.button("📚 学习建议", key="plan_button"):
                    st.session_state.current_page = "学习建议"
            with col7:
                if st.button("🌟 思政案例", key="political_button"):
                    st.session_state.current_page = "思政案例"

        # 根据选择的页面显示内容
        display_pages()

if __name__ == "__main__":
    main()