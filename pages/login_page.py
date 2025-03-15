import streamlit as st


# 模拟用户数据，实际应从数据库等获取
users = {
    "gavin": "gavin",
    "lydia": "lydia"
}

# 登录页面
def login_page():
    st.title("登录界面")
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    if st.button("登录"):
        if username in users and users[username] == password:
            st.session_state['user'] = username
            st.session_state.logged_in = True
        else:
            st.error("用户名或密码错误")