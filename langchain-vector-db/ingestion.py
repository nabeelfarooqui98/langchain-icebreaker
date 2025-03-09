from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
import os

if __name__ == "__main__":
    loader = TextLoader("mediumblog1.txt", encoding="utf-8")
    document = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    texts = text_splitter.split_documents(document)

    print(f'Created {len(texts)} text chunks')

    embeddings = OpenAIEmbeddings()

    PineconeVectorStore.from_documents(
        texts, embeddings, index_name=os.environ['INDEX_NAME'])
