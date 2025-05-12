import os
import json
from loguru import logger
from typing import List
from tqdm import tqdm
from langchain_pymupdf4llm import PyMuPDF4LLMLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


RAW_DATA_PATH = os.path.abspath("./data/raw")
MD_CHUNKS_DIR_PATH = os.path.abspath("./data/processed/md_chunks")
os.makedirs(MD_CHUNKS_DIR_PATH, exist_ok=True)


def to_markdown_chunks(file_path: str) -> List[str]:
    """Load PDF pages from a file."""
    logger.info(f"Loading PDF file: {file_path}")
    loader = PyMuPDF4LLMLoader(
        file_path,
        table_strategy="lines_strict",
    )
    text_aplitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=500,
        chunk_overlap=20,
    )
    chunks = loader.load_and_split(text_splitter=text_aplitter)
    logger.success(f"Loaded {len(chunks)} chunks from {file_path}:\n")
    return chunks

def save_chunks(chunks: List[str], dir_path: str):
    """Save chunks to a directory."""
    logger.info(f"Saving chunks to {dir_path}")
    for i, chunk in tqdm(enumerate(chunks), total=len(chunks)):
        with open(os.path.join(dir_path, f"{i}.md"), "w") as f:
            f.write(chunk.page_content)
    logger.success(f"Saved {len(chunks)} chunks to {dir_path}")


if __name__ == "__main__":
    file_path = os.path.join(RAW_DATA_PATH, "Port Tariff.pdf")
    chunks = to_markdown_chunks(file_path)
    save_chunks(chunks, MD_CHUNKS_DIR_PATH)
