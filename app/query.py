# app/query.py

from app.config import OPENAI_API_KEY
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS

# Load FAISS vector store
def load_vectorstore(index_path="./embeddings/faiss_index"):
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

# Manually retrieve top documents and send to GPT
def manual_rag_answer(vectorstore, query_text, top_k=3):
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
    top_docs = retriever.get_relevant_documents(query_text)

    context = "\n\n".join([f"[{i+1}] {doc.metadata['filename']} ({doc.metadata['application']}):\n{doc.page_content}" for i, doc in enumerate(top_docs)])
    
    prompt = f"""You are an AI assistant helping a job seeker track their resume versions and content. Given the following documents retrieved as context, answer the user's question.

Context:
{context}

Question: {query_text}
Answer:"""

    llm = ChatOpenAI(model="gpt-4", temperature=0)
    response = llm.invoke(prompt)
    return response.content, top_docs

# CLI
if __name__ == "__main__":
    vs = load_vectorstore()

    print("\n🔍 Job App RAG Query Interface (Direct Mode)\nType your question below (or 'q' to quit):\n")
    while True:
        user_input = input("🧠 Ask: ")
        if user_input.lower() in ["q", "quit", "exit"]:
            break

        print("\n💬 Answer:")
        answer, docs = manual_rag_answer(vs, user_input)
        print(answer)

        print("\n📎 Sources:")
        for doc in docs:
            print(f"- {doc.metadata['filename']} (application: {doc.metadata['application']})")
        print("\n" + "-" * 50 + "\n")
