from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain import hub
import os
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.runnables import RunnablePassthrough


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


if __name__ == "__main__":
    embeddings = OpenAIEmbeddings()
    llm = ChatOpenAI()

    query = "What is the crayon analogy?"
    chain = PromptTemplate.from_template(template=query) | llm
    result = chain.invoke(input={})
    # print(result.content)

    vectorstore = PineconeVectorStore(
        index_name=os.environ['INDEX_NAME'], embedding=embeddings)

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    combine_docs_chain = create_stuff_documents_chain(
        llm, retrieval_qa_chat_prompt)

    retrieval_chain = create_retrieval_chain(
        vectorstore.as_retriever(), combine_docs_chain)

    result = retrieval_chain.invoke(input={"input": query})

    # print(result)

    template = """use the following pieces of context to answer the question. if you dont
     know the answer, just say you dont know. Dont make up an answer. At the end, always 
     say 'Thanks for the question!' 
     
     Context: {context}

     Question: {question}

     Helpful answer:
     
     """

    custom_rag_prompt = PromptTemplate.from_template(template=template)

    rag_chain = (
        {'context': vectorstore.as_retriever() | format_docs,
         'question': RunnablePassthrough()}
        | custom_rag_prompt
        | llm
    )

    result = rag_chain.invoke(query)
    print(result)
