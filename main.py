# main.py

import argparse
from app.ingest import load_documents, embed_documents
from app.query import manual_rag_answer, load_vectorstore

def run_ingest():
    base_dir = "data/applications"
    from pathlib import Path
    all_documents = []

    print(f"\n📥 Starting ingestion from: {base_dir}\n")

    app_base = Path(base_dir)
    if not app_base.exists():
        print(f"⚠️ Folder not found: {base_dir}")
        return

    subdirs = [d for d in app_base.iterdir() if d.is_dir()]
    print(f"📂 Found {len(subdirs)} application folders.\n")

    for subdir in subdirs:
        print(f"🔍 Ingesting folder: {subdir.name}")
        docs = load_documents(subdir)
        print(f"   ➡️ Found {len(docs)} documents in {subdir.name}\n")
        all_documents.extend(docs)

    if all_documents:
        print(f"🗂 Total documents to embed: {len(all_documents)}\n")
        embed_documents(all_documents)
        print("\n✅ Ingestion complete. FAISS index saved.\n")
    else:
        print("\n⚠️ No documents found in any folder. Nothing was embedded.\n")


def run_query():
    vs = load_vectorstore()
    print("\n🔍 Job App Tracker — Query Mode\nType 'q' to quit.\n")
    while True:
        user_input = input("🧠 Ask: ")
        if user_input.lower() in ["q", "quit", "exit"]:
            break
        answer, docs = manual_rag_answer(vs, user_input)
        print(f"\n💬 Answer:\n{answer}\n")
        print("📎 Sources:")
        for doc in docs:
            print(f"- {doc.metadata['filename']} (application: {doc.metadata['application']})")
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Job Application Tracker CLI")
    parser.add_argument("--mode", choices=["ingest", "query"], required=True, help="Mode to run: ingest or query")
    args = parser.parse_args()

    if args.mode == "ingest":
        run_ingest()
    elif args.mode == "query":
        run_query()
