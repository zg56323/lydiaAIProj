# 使用官方的 Python 镜像作为基础镜像
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码到容器中
COPY . .

# 暴露端口（如果需要）
EXPOSE 8501

# 运行 Streamlit 应用
CMD ["streamlit", "run", "main.py"]

