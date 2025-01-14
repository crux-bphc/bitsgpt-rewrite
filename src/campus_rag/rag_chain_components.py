from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEmbeddings

model_id = "sentence-transformers/all-MiniLM-L6-v2"
model_kwargs = {"device": "cpu"}
embeddings = HuggingFaceEmbeddings(model_name=model_id, model_kwargs=model_kwargs)


def get_retriever(**kwargs):
    db = Chroma(persist_directory="chroma", embedding_function=embeddings)
    retriever = db.as_retriever(**kwargs)
    return retriever


output_parser = StrOutputParser()
