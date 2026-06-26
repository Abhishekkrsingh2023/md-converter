<div align="center"># md → export</div>
<div align="center">
### A minimal self-hosted Markdown → PDF / DOCX converter

Convert raw Markdown or `.md` files into **PDF** and **DOCX** using **FastAPI**, **Pandoc**, and **XeLaTeX** — all packaged in a **single Docker container**.

<p>
  <img src="https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Pandoc-enabled-6f42c1?style=for-the-badge" alt="Pandoc">
  <img src="https://img.shields.io/badge/XeLaTeX-ready-orange?style=for-the-badge" alt="XeLaTeX">
  <img src="https://img.shields.io/badge/Docker-ready-2496ED?style=for-the-badge&logo=docker" alt="Docker">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT">
</p>

</div>

---

## ✨ Overview

**md → export** is a lightweight document conversion service for people who want a **simple, self-hosted Markdown-to-document pipeline** without dealing with heavyweight editors or cloud tooling.

It provides:

* a **clean browser UI** for pasting Markdown or uploading `.md` files
* **PDF export** through **Pandoc + XeLaTeX**
* **DOCX export** through **Pandoc**
* support for **inline and block LaTeX math**
* a **single-container deployment** with no database, worker queue, or extra services

---

## 📸 What it does

* **Paste Markdown** directly into the web UI
* **Upload `.md` files**
* Export to:

  * **PDF**
  * **DOCX**
* Automatically download the generated file
* Render **LaTeX math**:

  * Inline: `$E = mc^2$`
  * Block:

    ```md
    $$
    \int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
    $$
    ```

---

## 🚀 Features

* **Minimal self-hosted setup**

  * No external SaaS
  * No database
  * No Redis / queue / background worker

* **Multiple input modes**

  * Paste raw Markdown
  * Upload a `.md` file

* **Multiple output formats**

  * **PDF** via XeLaTeX
  * **DOCX** via Pandoc

* **Math-friendly**

  * Supports inline and block LaTeX math syntax

* **Container-first deployment**

  * One Docker image
  * Easy local or server deployment

* **Simple API**

  * Integrate with scripts, editors, or other internal tools

---

## 🧱 Tech Stack

| Layer                   | Technology                    |
| ----------------------- | ----------------------------- |
| **Backend**             | Python 3.13, FastAPI, Uvicorn |
| **Document conversion** | pypandoc                        |
| **PDF engine**          | XeLaTeX (`texlive-xetex`)     |
| **Frontend**            | Vanilla HTML / CSS / JS       |
| **Packaging**           | Docker                        |

---

## 📂 Project Structure

```bash
md-converter/
├── main.py                 # FastAPI app + API routes
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── frontend/
    └── index.html          # Static web UI served by FastAPI
```

---

## ⚙️ Getting Started
## ⚙️ Docker Compose Tuning

The service is intentionally packaged as a **single backend container**, so most runtime customization happens in `docker-compose.yml`.

## Increase memory for large Markdown / PDF conversions

If users are converting larger documents with heavy LaTeX content, you may want to increase the memory limit:

```yaml
deploy:
  resources:
    limits:
      cpus: "1.0"
      memory: 1G
```

This gives the container more room for **Pandoc** and **XeLaTeX**, which can be memory-intensive during PDF generation.

---

## Suggested default for this project

For a small self-hosted Markdown converter, a sensible starting point is:

```yaml
deploy:
  resources:
    limits:
      cpus: "0.5"
      memory: 512M
```

That is usually enough for:

* normal Markdown documents
* moderate PDF generation workloads
* light personal / internal use

If you expect **large PDFs**, **many images**, or **heavier LaTeX documents**, increase memory first before increasing CPU.


## 1) Clone the repository

```bash
git clone https://github.com/Abhishekkrsingh2023/md-converter.git
cd md-converter
```

## 2) Start with Docker Compose

```bash
docker compose up --build
```

Then open:

```text
http://localhost:8000
```

---

## 🔁 Rebuild from scratch

If you want to rebuild the image without using Docker cache:

```bash
docker compose build --no-cache
docker compose up
```

---

## 🌐 API Reference

The service exposes both a **web UI** and **direct HTTP endpoints**.

---

## `POST /convert_text`

Convert raw Markdown text to **PDF** or **DOCX**.

### Query Parameters

| Name   | Type   | Required | Description                              |
| ------ | ------ | -------- | ---------------------------------------- |
| `type` | string | No       | Output format: `pdf` (default) or `docx` |

### Request Body

Raw Markdown content as plain text.

### Example

```bash
curl -X POST "http://localhost:8000/convert_text?type=pdf" \
  -H "Content-Type: text/plain" \
  --data "# Hello\n\nThis is **Markdown**." \
  --output output.pdf
```

---

## `POST /convert`

Convert an uploaded `.md` file to **PDF** or **DOCX**.

### Query Parameters

| Name   | Type   | Required | Description                              |
| ------ | ------ | -------- | ---------------------------------------- |
| `type` | string | No       | Output format: `pdf` (default) or `docx` |

### Form Data

| Field  | Type | Required | Description              |
| ------ | ---- | -------- | ------------------------ |
| `file` | file | Yes      | Markdown file to convert |

### Example

```bash
curl -X POST "http://localhost:8000/convert?type=docx" \
  -F "file=@document.md" \
  --output output.docx
```

---

## `GET /health`

Returns service health status and the installed Pandoc version.

### Example response

```json
{
  "status": "ok",
  "pandoc": "3.x.x"
}
```

---

## 🧮 Math Support

LaTeX math is supported out of the box when exporting to PDF.

### Inline math

```md
Einstein’s equation: $E = mc^2$
```

### Block math

```md
$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$
```

---

## 🐳 Why Docker?

This project is designed around a **single-container workflow**:

* FastAPI serves the UI and API
* Pandoc handles conversion
* XeLaTeX renders PDFs
* everything runs in one place

That makes deployment straightforward for:

* local development
* self-hosted internal tools
* small utility servers
* homelab setups

---

## 💡 Example Use Cases

* Convert class notes written in Markdown to **PDF**
* Export technical documentation to **DOCX** for sharing
* Build a small internal **Markdown export service**
* Add a document conversion backend to another application

---
<div align="center">
## 📄 License

MIT © 2026 [Abhishek](https://github.com/Abhishekkrsingh2023)
</div>
