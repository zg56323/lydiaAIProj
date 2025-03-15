import streamlit as st

def chat_page():
    st.title("思维导图生成器")

    markdown_content = """
    # 思维导图示例
    - 主题1
        - 子主题1.1
        - 子主题1.2
    - 主题2
        - 子主题2.1
            - 子子主题2.1.1
            - 子子主题2.1.2
        - 子主题2.2
    """

    mermaid_code = """
    graph TD;
        A[主题] --> B[主题1];
        B --> C[子主题1.1];
        B --> D[子主题1.2];
        A --> E[主题2];
        E --> F[子主题2.1];
        F --> G[子子主题2.1.1];
        F --> H[子子主题2.1.2];
        E --> I[子主题2.2];
    """

    st.markdown("## Markdown 内容")
    st.write(markdown_content)

    st.markdown("## 思维导图")
    st.markdown(mermaid_code, unsafe_allow_html=True)

if __name__ == "__main__":
    chat_page()
