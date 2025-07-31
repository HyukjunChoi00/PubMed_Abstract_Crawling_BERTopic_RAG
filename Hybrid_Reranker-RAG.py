import os
os.environ["OPENAI_API_KEY"] = 'your api key'
from langchain.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain.retrievers import ContextualCompressionRetriever


#2 RAG
loader = CSVLoader(file_path="Pubmed_Liposome_2020_2023.csv",source_column='abstract')
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1500,
    chunk_overlap  = 100,
    length_function = len,
)

splits = text_splitter.split_documents(docs)
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(splits,
                                   embedding = embeddings)
faiss_retriever = db.as_retriever(# 검색 유형을 "유사도 점수 임계값"으로 설정
    search_type="similarity_score_threshold",
    # 검색 인자로 점수 임계값을 0.5로 지정
    search_kwargs={"score_threshold": 0.75})

bm25_retriever = BM25Retriever.from_documents(docs)
bm25_retriever.k = 30
ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever,faiss_retriever],weights=[0.5,0.5])
llm = ChatOpenAI(model='gpt-4o-mini')


template = """
You are given a scientific article abstract along with retrieved context.  
Your task is to construct a structured table summarizing the information.  
If the answer is not available in the provided context, respond with "I don't know."

### Instructions:
1. Use the given context to create a table with the following columns:
   - LNP Formulation: Provide the exact name of the lipid nanoparticle.
   - Therapeutic Strategy: Summarize the therapeutic approach.
   - PMID: Include the unique PMID related to the information. Each PMID should appear in only one row.

2. Provide up to four cases in the table:
   - If the context does not provide enough information for four cases, include as many cases as possible (up to four).

3. Treat liposomes as a type of lipid nanoparticle.

### Output Format:
| LNP Formulation              | Therapeutic Strategy                                       | PMID      |
|-----------------------------|-------------------------------------------------------------|-----------|
| RGD-modified PEGylated liposome | Targeting BCL-2 for tumor apoptosis                         | 12345678  |
| Cationic liposome           | Gene delivery targeting PD-L1 for cancer immunotherapy     | 23456789  |

### Context:
{context}
"""
model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
compressor = CrossEncoderReranker(model=model, top_n=3)


# 문맥 압축 검색기 설정
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=ensemble_retriever
)

#doc_retrieved = compression_retriever.invoke("")  # 검색할 내용 입력 --> 검색된 문서 출력

from langchain import hub
prompt = hub.pull("langchain-ai/retrieval-qa-chat")

combine_docs_chain = create_stuff_documents_chain(
    llm, prompt
)

retrieval_chain = create_retrieval_chain(compression_retriever, combine_docs_chain)
query="Cancer therapy strategies"
retrieval_chain.invoke({"input": query})


## Prompt 부분 수정 필요
