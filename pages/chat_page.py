import streamlit as st
import streamlit.components.v1 as components

# 设置页面配置
st.set_page_config(layout="wide")

def chat_page():

    components.html(
        """
        <style>
            body {
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }
            iframe {
                width: 100%;
                height: 100vh;
                border: none;
                margin: 0;
                padding: 0;
            }
            /* 媒体查询以适应小屏幕 */
            @media (max-width: 600px) {
                iframe {
                    width: 100%;
                    height: 100vh;
                }
            }
        </style>
        <iframe
            src="http://192.168.2.10/chatbot/x3ZGy60jU9Ve34vo"
            frameborder="0"
            allow="microphone">
        </iframe>
        """,
        height=680,
        scrolling=True
    )
