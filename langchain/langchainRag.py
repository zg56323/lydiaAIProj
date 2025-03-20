from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

def upload_and_process_file(openai_api_key, uploaded_file):
    # 读取并保存上传的文件内容
    file_content = uploaded_file.read()
    temp_file_path = "temp.pdf"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file_content)

    # 加载 PDF 文件
    loader = PyPDFLoader(temp_file_path)
    docs = loader.load()

    # 分割文本
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=50,
        separators=["\n", " ", "!", "?", ".", ",", "\\", ""]
    )
    texts = text_splitter.split_documents(docs)

    # 创建嵌入模型和向量存储
    embeddings_model = OpenAIEmbeddings(openai_api_key=openai_api_key)
    db = FAISS.from_documents(texts, embeddings_model)
    retriever = db.as_retriever()

    return retriever

def call_qa_chain(openai_api_key, memory, retriever, question):
    # 初始化模型
    model = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key)

    # 创建 QA 链
    qa = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        memory=memory
    )

    # 调用 QA 链并获取响应
    response = qa.invoke({"chat_history": memory, "question": question})
    return response

def qa_agent(openai_api_key, memory, uploaded_file, question):
    # 处理上传的文件并获取检索器
    retriever = upload_and_process_file(openai_api_key, uploaded_file)

    # 调用 QA 链并返回响应
    response = call_qa_chain(openai_api_key, memory, retriever, question)
    return response
