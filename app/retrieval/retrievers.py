from langchain.retrievers import ContextualCompressionRetriever, MultiQueryRetriever
from langchain_cohere import CohereRerank
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from ..vectorstore import vectorstore


# llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# QUERY_PROMPT = PromptTemplate(
#     input_variables=["question"],
#     template="""You are an expert AI assistant, specialized in maritime operations and port tariff calculations.
#     Your task is to generate 3 different versions of the given user question 
#     to retrieve the most relevant tariff documents from a vector database. 
#     By generating multiple perspectives on the user question, your goal is to help the user overcome some of the limitations
#     of distance-based similarity search.
#     Provide these alternative questions separated by newlines.
#     Original question: {question}""",
# )

# multi_query_retriever = MultiQueryRetriever.from_llm(
#     retriever=base_retriever,
#     llm=llm,
#     prompt=QUERY_PROMPT,
#     include_original=True,
# )

def get_retriever(rerank: bool = True, top_n: int = 25, **kwargs):
    base_retriever = vectorstore.as_retriever(**kwargs)
    compressor = CohereRerank(
        model="rerank-english-v3.0",
        top_n=top_n,
    )
    retriever = ContextualCompressionRetriever(
        base_retriever=base_retriever,
        base_compressor=compressor,
    )
    return retriever if rerank else base_retriever