# CT200 Document Intelligence System

A FastAPI-based Document Intelligence System that supports intelligent PDF versioning, reusable document selections, AI-powered QA test case generation using Google Gemini, and automatic staleness detection of generated outputs after document updates.

---

## Features

- Upload and parse PDF documents
- Maintain multiple document versions
- Intelligent versioning using persistent Logical Node IDs
- Browse document hierarchy
- Full-text search across document sections
- Compare document versions
- Create reusable document selections
- Generate QA test case ideas using Google Gemini
- Prevent duplicate AI generations using content hashing
- Detect stale generations after document updates

---

## Tech Stack

**Backend**
- FastAPI
- Python 3.12
- SQLite
- Pydantic

**AI**
- Google Gemini 2.5 Flash
- google-generativeai SDK

**Libraries**
- PyMuPDF
- hashlib
- json

---

## Project Structure

```
CT200-Document-Intelligence-System/
│
├── app/
│   ├── api/
│   │   ├── documents.py
│   │   ├── search.py
│   │   ├── compare.py
│   │   ├── selection.py
│   │   └── generation.py
│   │
│   ├── services/
│   │   ├── parser_service.py
│   │   ├── version_service.py
│   │   ├── search_service.py
│   │   ├── generation_service.py
│   │   ├── llm_service.py
│   │   └── staleness_service.py
│   │
│   ├── database.py
│   └── main.py
│
├── documents.db
├── requirements.txt
└── README.md
```

---

## System Architecture

```
                PDF Upload
                     │
                     ▼
              PDF Parser Service
                     │
                     ▼
            Document Versioning
                     │
      ┌──────────────┴──────────────┐
      ▼                             ▼
 Browse/Search APIs          Compare Versions
      │
      ▼
 Document Selection
      │
      ▼
 Context Reconstruction
      │
      ▼
 Duplicate Detection (SHA-256)
      │
      ▼
 Google Gemini
      │
      ▼
 QA Test Case Generation
      │
      ▼
 Store Generation
      │
      ▼
 Staleness Detection
```

---

## Intelligent Versioning

Each document section is assigned a persistent **Logical Node ID**.

When a new version is uploaded:

- Unchanged sections reuse their Logical Node IDs.
- Modified sections are updated.
- New sections receive new Logical Node IDs.

This allows the system to track document changes while maintaining logical relationships across versions.

---

## Generation Workflow

1. Retrieve the selected document sections.
2. Reconstruct the document context.
3. Generate a SHA-256 hash of the context.
4. Check for an existing generation with the same hash.
5. If found, return the existing generation.
6. Otherwise, send the prompt to Google Gemini.
7. Validate the JSON response.
8. Store the generation and metadata.

---

## Staleness Detection

Each generation stores a SHA-256 hash of the document content used during generation.

When retrieving a generation:

- Rebuild the selection using the latest document version.
- Generate a new hash.
- Compare it with the stored hash.

If they differ:

```
stale = true
```

Otherwise:

```
stale = false
```

---

# API Endpoints

## Document APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/documents/upload` | Upload a PDF |
| GET | `/documents/{id}` | Browse document |
| GET | `/search` | Search document |
| GET | `/compare` | Compare document versions |

---

## Selection APIs

| Method | Endpoint |
|---------|----------|
| POST | `/selections` |
| GET | `/selections/{id}` |

---

## Generation APIs

| Method | Endpoint |
|---------|----------|
| POST | `/generations/{selection_id}` |
| GET | `/generations/{generation_id}` |
| GET | `/generations/selection/{selection_id}` |
| GET | `/generations/node/{logical_node_id}` |

---

# Setup

Clone the repository:

```bash
git clone <repository-url>
cd CT200-Document-Intelligence-System
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

**Windows (PowerShell)**

```powershell
venv\Scripts\Activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure the Gemini API key:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

Run the application:

```bash
uvicorn app.main:app --reload
```

Open Swagger:

```
http://127.0.0.1:8000/docs
```

---

# Testing

### Upload a Document

Upload a PDF using:

```
POST /documents/upload
```

Verify:

- Document created
- Version 1 stored
- Sections parsed successfully

---

### Create a Selection

```
POST /selections
```

Choose the logical nodes to include.

---

### Generate Test Cases

```
POST /generations/{selection_id}
```

If the Gemini API key is configured, the system returns 3–5 QA test case ideas in JSON format.

---

### Retrieve a Generation

```
GET /generations/{generation_id}
```

The response includes:

- Generated test cases
- Status
- Model name
- Creation timestamp
- Staleness information

---

# Re-ingestion Workflow (Version 1 → Version 2)

1. Upload a document (**Version 1**).
2. Create a selection.
3. Generate QA test cases.
4. Modify the PDF (add, remove, or update content).
5. Upload the modified PDF using the same document.
6. The system creates **Version 2**.
7. Compare versions using:

```
GET /compare
```

8. Retrieve the existing generation:

```
GET /generations/{generation_id}
```

If any selected content has changed, the response will indicate:

```json
{
    "stale": true
}
```

---

# Current Limitations

- Supports PDF documents only.
- Requires a Gemini API key for AI generation.
- Staleness detection is based on SHA-256 hashes of normalized text and cannot distinguish semantic from cosmetic changes.
- Duplicate detection is limited to identical document content.

---

# Future Improvements

- Embedding-based semantic search
- Semantic staleness detection
- Authentication and authorization
- PostgreSQL support
- Background generation jobs
- Support for DOCX and HTML documents
- Multiple LLM providers

---

# Author

**Rashmi**

CT200 – Document Intelligence System
