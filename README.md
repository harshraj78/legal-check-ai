
# 📄 Legal-Check AI

A **production-ready backend system** for uploading, processing, and analyzing legal documents asynchronously.  
Designed with **real-world backend patterns**, scalability, and clean architecture principles.

---

## 🚀 Features

### 📥 Contract Upload & Secure Storage
- REST API to upload legal documents (**PDF**).
- Files stored using **UUID-based filenames** to prevent guessing and path traversal attacks.
- Immediate database record creation with **status tracking**.

---

### ⚡ Asynchronous Processing (Non-Blocking Architecture)
- Uses **FastAPI BackgroundTasks** to offload heavy processing.
- API responds instantly with **202 Accepted**.
- Prevents request timeouts under concurrent uploads.

---

### 📄 PDF Text Extraction Pipeline
- Extracts raw text from uploaded PDFs.
- Stores extracted content in **PostgreSQL** for auditability and traceability.
- Modular service design allows future OCR or preprocessing enhancements.

---

### 🧠 AI Analysis Layer (Abstracted & Pluggable)
- AI logic encapsulated behind a **clean service interface**.
- Currently **mocked** for stability, cost control, and local development.
- Can be seamlessly replaced with:
  - Hugging Face Inference API
  - OpenAI
  - Internal LLMs
- Designed to **avoid vendor lock-in**.

---

### 📊 Structured Analysis Results
- Normalized relational schema:
  - **Contract ↔ AnalysisResult (one-to-one)**
- Stores:
  - Risk score
  - Summarized insights
- Results exposed via REST API for easy client consumption.

---

### 🔄 Status-Driven Workflow
Each contract follows a predictable lifecycle:

```

pending → processing → completed / failed

```

- Clients poll using `contract_id`
- Results returned once processing completes

---

### 🔐 Security & Best Practices
- UUID-based resource isolation
- Environment-based secret management
- Database integrity constraints
- Clean separation of:
  - API layer
  - Services
  - Integrations
  - Models

---

## 🧱 Architecture Overview

```

Client
↓
FastAPI API
↓
PostgreSQL
↓
Background Task
↓
PDF Text Extraction → AI Analysis → Persist Result

````

---

## 🛠 Tech Stack
- **FastAPI**
- **Python 3.13**
- **SQLAlchemy 2.0**
- **PostgreSQL**
- **PyMuPDF**
- Docker-ready architecture

---

## ▶️ How to Run Locally

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/harshraj78/legal-check-ai.git
cd legal-check-ai
````

---

### 2️⃣ Create Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

> If using Poetry:

```bash
poetry install
poetry shell
```

---

### 3️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```env
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=legal_ai

HF_API_TOKEN=your_token_if_used
```

---

### 4️⃣ Start PostgreSQL

Ensure PostgreSQL is running locally and the database exists:

```sql
CREATE DATABASE legal_ai;
```

---

### 5️⃣ Run the Application

```bash
uvicorn app.main:app --reload
```

---

### 6️⃣ Open API Documentation

Visit Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 🔍 How to Verify PDF Processing

1. Upload a PDF via `/api/v1/contracts/upload`
2. Copy the returned `contract_id`
3. Poll:

```
GET /api/v1/contracts/{contract_id}
```

4. Check extracted text and analysis in PostgreSQL:

```sql
SELECT raw_text FROM contracts;
SELECT * FROM analysis_results;
```

---

## 📌 Future Improvements

* Replace BackgroundTasks with **Celery + Redis** for high-scale workloads
* Add retries and task persistence
* Authentication & role-based access control
* Frontend dashboard for monitoring contracts - need to deploy

