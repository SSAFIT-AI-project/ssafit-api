from fastapi import APIRouter
from pydantic import BaseModel
from langchain_chroma import Chroma
from langchain_upstage import UpstageEmbeddings, ChatUpstage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
import os

router = APIRouter()

# API 키 확인
if not os.getenv("UPSTAGE_API_KEY"):
    print("경고: UPSTAGE_API_KEY가 설정되지 않았습니다.")
    print("환경변수 UPSTAGE_API_KEY를 설정하거나 .env 파일에 추가하세요.")

# 벡터스토어 초기화 함수
def get_retriever():
    """API 키가 설정된 후에 벡터스토어를 초기화합니다."""
    if not os.getenv("UPSTAGE_API_KEY"):
        raise ValueError("UPSTAGE_API_KEY가 설정되지 않았습니다.")
    
    db_directory = "./chroma_db"
    chroma_vectorstore = Chroma(
        persist_directory=db_directory,
        embedding_function=UpstageEmbeddings(model="embedding-query")
    )
    return chroma_vectorstore.as_retriever(
        search_type='mmr',
        search_kwargs={"k": 10, "score_threshold": 0.8}
    )

class AskRequest(BaseModel):
    question: str

@router.post("/ask")
def ask(request: AskRequest):
    """사용자의 질문에 대해 AI가 답변합니다."""
    try:
        # API 키 확인 및 retriever 초기화
        retriever = get_retriever()
        
        # LLM 초기화
        llm = ChatUpstage(model="solar-1-mini-chat")
        
        # 데이터 저장용 딕셔너리 초기화
        data = {
            "question": [],
            "answer": [],
            "contexts": [],
            "ground_truth": []
        }
        
        # fill_data 함수를 사용하여 답변 생성
        fill_data(request.question, "", data, retriever)
        
        # 마지막 답변 반환
        if data["answer"]:
            return {
                "answer": data["answer"][-1],
            }
        else:
            return {
                "error": "답변을 생성할 수 없습니다."
            }
            
    except ValueError as e:
        return {
            "error": str(e)
        }
    except Exception as e:
        return {
            "error": f"서버 오류가 발생했습니다: {str(e)}"
        } 

# RAG Retrieve 결과를 Context로 사용하도록 포맷팅
def format_context(docs: list[Document]):
    formatted_chunks = []

    for i, doc in enumerate(docs):
        metadata_str = ", ".join([f"{k}: {v}" for k, v in doc.metadata.items()])
        formatted_chunks.append(
            f"--- 문서 {i + 1} ---\n"
            f"메타데이터: {metadata_str}\n"
            f"내용: {doc.page_content}"
        )
    
    return '\n\n'.join(formatted_chunks)


# 컨텍스트와 사용자 질의를 기반으로 프롬프트 작성
def generate_prompt(query: str, context: str):
  prompt_str = f'''
    당신은 신용카드 전문가입니다.
    아래 제공된 카드 정보와 가이드라인을 바탕으로 사용자의 질문에 대해 정확하고 친절하게 답변해주세요.

    ## 참고할 카드 정보
    {context}

    ---

    ## 답변 가이드라인
    1. **카드 식별**: 메타데이터에서 카드명(cardName)과 카드사(cardCompany)를 정확히 파악하여 언급
    2. **구체적 정보 제공**: 연회비, 혜택, 서비스 등 구체적인 수치와 내용을 포함
    3. **비교 분석**: 여러 카드가 언급된 경우 각각의 특징을 비교하여 설명
    4. **사용자 친화적**: 복잡한 정보도 쉽게 이해할 수 있도록 설명
    5. **실용적 조언**: 사용자의 질문에 맞는 실용적인 조언 제공
    6. 모든 답변은 마크 다운 형식으로 작성해주세요.
    7. 모든 답변은 반드시 한국어로 하세요.
    8. 답변에 '어떠한 문서에 따르면,' 이라는 말을 포함하지 마세요.
    9. 카드와 관련된 질문이 아니라면 답변하지 마세요.
    10. 같은 카드가 여러번 언급되지 않게 하세요. 한 번에 같은 카드를 소개하지 마세요.
    ---

    ## 사용자의 질문
    {query}
    '''

  prompt = ChatPromptTemplate.from_template(prompt_str)

  return prompt


# RAG retrieve, LLM 질의 후 결과를 data에 저장
def fill_data(query, ground_truth, data, retr):
    # LLM 초기화
    llm = ChatUpstage(model="solar-1-mini-chat")
    
    # RAG Retrieve
    try:
      retrieve_results = retr.invoke(query)
      if retrieve_results:
        context = format_context(retrieve_results)
      else:
        print(f"질문 '{query[:30]}...'에 대한 검색 결과가 없습니다.")
        context = "검색된 관련 문서가 없습니다."
    except Exception as e:
        print(f"Retriever 호출 중 오류 발생 (질문: {query[:30]}...): {e}")
        context = "검색 오류로 인해 컨텍스트를 가져올 수 없습니다."

    # LLM 질의
    try:
        prompt = generate_prompt(query, context)
        chain = prompt | llm | StrOutputParser()

        answer = chain.invoke({"history": [], "context": context, "input": query})

    except Exception as e:
        print(f"LLM 체인 호출 중 오류 발생 (질문: {query[:30]}...): {e}")
        answer = f"LLM 답변 생성 중 오류 발생: {e}"

    # data 변수에 저장
    data["question"].append(query)
    data["answer"].append(answer)
    data["contexts"].append([doc.page_content for doc in retrieve_results] if retrieve_results else [])
    data["ground_truth"].append(ground_truth)