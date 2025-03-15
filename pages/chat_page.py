import streamlit as st
import streamlit.components.v1 as components

# 设置页面配置
st.set_page_config(layout="wide")

def chat_page():

    components.html(
        """
        <style>
            body {margin: 20; padding: 10}
            iframe {
                position: fixed;
                top: 0;
                left: 0;
                width: 90vw !important;
                height: 90vh !important;
                z-index: 9999;
            }
        </style>
        <iframe
            src="http://localhost/chatbot/x3ZGy60jU9Ve34vo"
            frameborder="0"
            allow="microphone">
        </iframe>
        """,
        height=680,
        scrolling=True
    )

