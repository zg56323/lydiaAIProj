import logging
import os
import time

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 提取文件目录为静态变量
MARKDOWN_DIR = 'mindMap/markdown'
HTML_DIR = 'mindMap/static/html'  # 修改：PNG_DIR 改为 HTML_DIR

def upload_markdown(content):
    print("正在上传 Markdown 内容:", content)
    time_name = str(int(time.time()))  # 生成时间戳作为文件名
    md_file_name = time_name + ".md"  # Markdown文件名
    html_file_name = time_name + ".html"  # 修改：文件名后缀改为html

    # 创建markdown和html文件夹，如果它们不存在的话
    os.makedirs(MARKDOWN_DIR, exist_ok=True)
    os.makedirs(HTML_DIR, exist_ok=True)  # 修改：创建HTML文件夹

    # 将Markdown内容写入文件
    with open(os.path.join(MARKDOWN_DIR, md_file_name), "w", encoding='utf-8') as f:
        f.write(content)

    logging.info(f"Markdown file created: {os.path.join(MARKDOWN_DIR, md_file_name)}")

    # 使用markmap生成HTML文件
    try:
        # 修改：调用markmap命令行工具生成HTML文件
        os.system(f"markmap {os.path.join(MARKDOWN_DIR, md_file_name)} --output {os.path.join(HTML_DIR, html_file_name)}")
        logging.info(f"HTML file created: {os.path.join(HTML_DIR, html_file_name)}")

        # 返回生成的HTML文件名
        return html_file_name
    except Exception as e:
        logging.error(f"Error generating HTML file: {e}")
        raise