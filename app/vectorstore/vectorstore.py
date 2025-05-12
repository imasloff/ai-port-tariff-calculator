import os
from loguru import logger
from tqdm import tqdm
from typing import List
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from ..process_pdf import MD_CHUNKS_DIR_PATH


def load_chunks(dir_path: str) -> List[Document]:
    """Load chunks from a directory."""
    chunks = []
    logger.info(f"Loading chunks from {dir_path}")
    for file_name in tqdm(sorted(os.listdir(dir_path), key=lambda x: int(x.split(".")[0]))):
        if file_name.endswith(".md"):
            with open(os.path.join(dir_path, file_name), "r") as f:
                content = f.read()
                chunks.append(Document(page_content=content))
    logger.success(f"Loaded {len(chunks)} chunks from {dir_path}")
    return chunks


hf_embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    encode_kwargs={"normalize_embeddings": True},
)

vectorstore = FAISS.from_documents(load_chunks(MD_CHUNKS_DIR_PATH), hf_embedding_model)
