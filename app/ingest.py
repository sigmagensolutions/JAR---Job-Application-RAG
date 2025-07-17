# app/ingest.py

import os
from pathlib import Path
import fitz  # PyMuPDF
from unstructured.partition.docx import partition_docx
from docx2pdf import convert
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from app.config import OPENAI_API_KEY


def read_text_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def read_pdf_file(path):
    try:
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"❌ Error reading PDF {path}: {e}")
        return ""


def read_docx_file(path):
    elements = partition_docx(filename=str(path))
    return "\n".join([el.text for el in elements if el.text])


def load_documents(application_dir):
    app_path = Path(application_dir)
    documents = []

    # Build a set of base names for .docx files to avoid ingesting duplicate PDFs
    docx_basenames = {file.stem for file in app_path.iterdir() if file.suffix == ".docx"}

    for file in app_path.iterdir():
        print(f"Checking file: {file.name}")
        content = ""

        if file.suffix == ".txt" and file.name != "metadata.json":
            content = read_text_file(file)

        elif file.suffix == ".pdf":
            if file.stem in docx_basenames:
                print(f"⚠️ Skipping PDF {file.name} because a corresponding .docx exists")
                continue
            content = read_pdf_file(file)

        elif file.suffix == ".docx":
            pdf_path = file.with_suffix(".pdf")
            print(f"🔄 Converting {file.name} to {pdf_path.name}...")

            try:
                convert(str(file), str(pdf_path))
                if pdf_path.exists():
                    content = read_pdf_file(pdf_path)
                    pdf_path.unlink()  # Clean up after reading
                else:
                    print(f"⚠️ Conversion failed or PDF not created for {file.name}")
            except Exception as e:
                print(f"❌ Failed to convert {file.name}: {e}")
                continue

        else:
            print(f"Skipping unsupported file: {file.name}")
            continue

        if content.strip():
            documents.append(
                Document(
                    page_content=content,
                    metadata={"filename": file.name, "application": app_path.name}
                )
            )
            print(f"✅ Extracted from {file.name} ({len(content)} chars)\n")
        else:
            print(f"⚠️ No content found in {file.name}")

    return documents


def embed_documents(documents, save_path="./embeddings/faiss_index"):
    embedding_model = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embedding_model)
    vectorstore.save_local(save_path)
    print(f"✅ Saved FAISS index to {save_path}")


if __name__ == "__main__":
    base_dir = Path("data/applications")
    all_documents = []

    for subdir in base_dir.iterdir():
        if subdir.is_dir():
            print(f"Ingesting: {subdir.name}")
            docs = load_documents(subdir)
            all_documents.extend(docs)

    if all_documents:
        embed_documents(all_documents)
    else:
        print("⚠️ No documents found to embed.")
