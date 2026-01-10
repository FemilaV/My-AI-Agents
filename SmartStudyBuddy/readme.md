# 📚 Smart Study Buddy (Contextual RAG with Pinecone)

Smart Study Buddy is a **context-aware Retrieval-Augmented Generation (RAG)** system designed to help grade 8 students to study from their PDFs (notes, chapters, textbooks). It enhances each chunk with **LLM-generated context**, stores them in **Pinecone**, and lets you have a **conversational study session** using GPT.

---

## 🚀 Features

- 📄 Load and process multiple PDFs
- ✂️ Smart chunking with overlap
- 🧠 **Contextual retrieval** (LLM-generated summaries per chunk)
- 🔎 Vector search using Pinecone
- 💬 Conversational Q&A with memory
- 🗂️ Filter by source or topic
- ♻️ Easy index reset

---

## 🧱 Tech Stack

| Component | Used Technology |
|---------|----------------|
| LLM | OpenAI GPT (chat + summarization) |
| Embeddings | OpenAI `text-embedding-3-small` |
| Vector DB | Pinecone (Serverless) |
| Framework | LangChain |
| Files | PDF |

---

## 📂 Project Structure

```
.
├── main.py                # Core RAG pipeline + chat interface
├── create_embedding.py    # One-time (or manual) PDF indexing script
├── clear_pinecone.py      # Utility to clear Pinecone index
├── study_materials/       # Folder containing PDF files
├── .env                   # API keys
└── README.md
```

---

## 🔐 Environment Setup

Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## 🧠 How It Works (High Level)

1. PDFs are loaded and split into chunks
2. Each chunk is sent to GPT to generate **contextual metadata**
3. Context + content is embedded
4. Embeddings are stored in Pinecone
5. User questions retrieve relevant chunks
6. GPT answers using retrieved context

---

## 🧩 File Explanations

### 1️⃣ `create_embedding.py`

**Purpose:**
- One-time (or occasional) script to process PDFs and upload embeddings

**What it does:**
- Checks if Pinecone index already has vectors
- Skips re-indexing if data exists
- Calls `process_all_pdfs()` from `main.py`
- Waits for Pinecone index propagation

**When to run:**
- First time setup
- After adding new PDFs
- After clearing the index

**Run command:**
```
python create_embedding.py
```

---

### 2️⃣ `clear_pinecone.py`

**Purpose:**
- Utility script to completely clear the Pinecone index

**What it does:**
- Connects to Pinecone
- Checks if index exists
- Deletes **all vectors** inside the index

⚠️ **Warning:** This does NOT delete the index itself — only the data.

**Run command:**
```
python clear_pinecone.py
```

---

### 3️⃣ `main.py` (Core Logic)

This is the heart of the project.

#### 🔹 PDF Processing
- Loads PDFs using `PyPDFLoader`
- Splits text using `RecursiveCharacterTextSplitter`
- Adds metadata (source, type, filename)

#### 🔹 Contextual Retrieval (Key Feature)
Each chunk is enhanced using GPT:
- Topic of the chunk
- Relation to the document
- Important concepts

This improves retrieval accuracy significantly.

#### 🔹 Pinecone Setup
- Creates index if missing
- Ensures correct embedding dimension (1536)
- Recreates index if dimension mismatch

#### 🔹 Conversational RAG
- Uses `ConversationSummaryMemory`
- History-aware retriever
- Maintains context across questions

#### 🔹 Interactive Study Session
Run:
```
python main.py
```
Then ask questions naturally:
```
You: Explain binary search
You: Give an example
You: How is it different from linear search?
```

---

## 🔍 Advanced Utilities

### 🔹 Search by Topic
Retrieve chunks related to a topic:
```python
search_by_topic("Operating Systems")
```

### 🔹 Filter by Source
Query only notes or a specific file:
```python
filter_by_source("Explain paging", file_type="notes")
```

---

## 🔄 Typical Workflow

1️⃣ Add PDFs to `study_materials/`

2️⃣ (Optional) Clear old data
```
python clear_pinecone.py
```

3️⃣ Create embeddings
```
python create_embedding.py
```

4️⃣ Start study session
```
python main.py
```

---

## ⚠️ Notes & Tips

- Pinecone indexing may take a few seconds to become searchable
- Contextual chunking increases indexing time but improves quality
- Costs depend on OpenAI + Pinecone usage

---

## ✅ Future Improvements

- Web UI (Streamlit / Next.js)
- Multi-user sessions
- Source citations in chat
- Support for non-PDF documents

---

## 🤝 Credits

Built using:
- LangChain
- OpenAI
- Pinecone

Happy studying! 🎓

