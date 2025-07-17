JAR — Job Application RAG

A Python-based tool for tracking your job applications using Retrieval-Augmented Generation (RAG). This system indexes your resumes, cover letters, and job postings, enabling semantic search and GPT-based summarization across all your application materials.

✨ Features
✅ Automatically ingests .docx, .pdf, and .txt files from application folders
✅ Converts .docx files to .pdf for reliable text extraction
✅ Embeds documents into a FAISS vector store for semantic search
✅ GPT-4 powered query interface for answering questions about your applications
✅ Supports tracking multiple applications across structured folders

📂 Folder Structure Example
data/
└── applications/
    ├── CompanyA/
    │   ├── Resume.docx
    │   ├── CoverLetter.docx
    │   └── JobPosting.txt
    └── CompanyB/
        ├── Resume.pdf
        └── cover_letter.txt

🚀 Setup Instructions
Clone the Repo & Set Up Virtual Environment
git clone https://github.com/sigmagensolutions/JAR---Job-Application-RAG
cd job_application_rag
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

Install Requirements
pip install -r requirements.txt
Set Up OpenAI API Key
Create a .env file:
OPENAI_API_KEY=your_openai_key_here

🛠️ Usage

Ingest All Applications
python main.py --mode ingest
Important: Make sure no .docx files are open in Word during ingestion, as docx2pdf requires exclusive access.

Query Your Applications
python main.py --mode query

Example queries:
"Summarize my cover letters that mention leadership."
"What experience did I highlight in AI roles?"

📝 Notes
PDFs are prioritized over .docx if both exist with the same name.
The ingestion process skips empty or unreadable files.
The system uses OpenAI’s GPT models — you’ll need API access.

🤖 Built with
Python 3.10+
LangChain & OpenAI APIs
FAISS for vector search
PyMuPDF, docx2pdf, unstructured for document parsing

📄 License
MIT — Feel free to fork, modify, and contribute!