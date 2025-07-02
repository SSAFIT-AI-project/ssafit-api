from dotenv import load_dotenv
load_dotenv()
import os
from langchain_chroma import Chroma
from langchain_upstage import UpstageEmbeddings
# ... (데이터 로드 및 분할 로직은 Colab 코드 그대로 가져오기) ...

# 상수 정의
db_directory = "./chroma_db"

chroma_vectorstore = Chroma(
    persist_directory=db_directory,
    embedding_function=UpstageEmbeddings(model="embedding-query")
)
# Retriever 예시
retriever = chroma_vectorstore.as_retriever(
    search_type= 'similarity', # default : similarity(유사도) / mmr 알고리즘
    search_kwargs={"k": 5} # 쿼리와 관련된 chunk를 3개 검색하기 (default : 4)
)

retrieved_documents = retriever.invoke("연회비가 가장 싼 카드는 뭐야")
print(retrieved_documents)