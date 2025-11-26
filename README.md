# 🌊 DweepLang: Your Offline English–Hindi AI Translator

A **proof-of-concept**, full-stack, **offline-first** Large Language Model interface that runs completely on your local machine — no internet required after setup.

Perfect for privacy-sensitive workflows, regional language processing (English ↔ Hindi), translation, summarization, and custom prompting — all powered locally.

---

## 🌟 1. What is DweepLang?

**DweepLang** is a lightweight, extensible wrapper that lets you interact with powerful language models **entirely offline**.  
It combines a simple web-based UI with a local Python backend, enabling seamless use of transformer models for tasks like:

- English ↔ Hindi bidirectional translation (core feature)
- Designed to be extensible for adding other tasks (e.g., summarization or custom prompts), but those are not included in this release
- Local data analysis without sending anything to the cloud

Built for **privacy**, **speed**, and **accessibility** in low-connectivity environments.

---

## 🏗️ 2. Project File Structure

```
DweepLingo/
├── models/                  # Downloaded model checkpoints (not in repo)
│   ├── en-hi/               # English → Hindi model
│   │   ├── config.json
│   │   ├── generation_config.json
│   │   ├── pytorch_model.bin    # Large file (~1–7 GB)
│   │   ├── tokenizer.json
│   │   ├── tokenizer_config.json
│   │   ├── special_tokens_map.json
│   │   └── sentencepiece.bpe.model (if applicable)
│   │
│   └── hi-en/               # Hindi → English model
│       └── (same structure as en-hi)
│
├── server/                  # Backend logic
│   ├── app.py               # Main server (Flask or FastAPI)
│   └── utils.py             # Model loading & inference helpers
│
├── frontend/                # User interface
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── run.bat                  # One-click start (Windows)
├── run.sh                   # One-click start (Linux/macOS)
├── download.py              # Downloads models automatically
├── requirements.txt         # Python dependencies
└── README.md                # Legacy notes (optional)
```

> **Important**: Large model files (`pytorch_model.bin`, `.safetensors`, etc.) are **not** included in the repository due to size. They are downloaded automatically via `download.py`.

---

## 🚀 3. Getting Started: Installation & Setup

### Step 3a: Install Dependencies

We recommend using **`uv`** (blazingly fast Python package manager):

```bash
# Optional: install uv if you don't have it
pip install uv

# Install all dependencies
uv sync
```
#                                                                                                       OR
### 1. Create a virtual environment (highly recommended)
```bash
python -m venv .venv
```
### 2. Activate the virtual environment
### Windows:
```bash
.\.venv\Scripts\activate
```

### Linux/macOS:
```bash
source .venv/bin/activate
```

And then install using pip:

```bash
pip install -r requirements.txt
```

### Step 3b: Download Models (One-Time Only)

This script downloads and organizes the required models into the `models/` folder:

```bash
python download.py
```

> This step requires internet. After completion, **DweepLang works 100% offline**.

---

## 💻 4. Running the Application

### Option 4a: Recommended — Use Convenience Scripts

**Windows**:
```cmd
.\run.bat
```

**Linux / macOS**:
```bash
./run.sh
```

### Option 4b: Manual Start

```bash
cd server
python app.py
```

The app will launch a local web server. Open your browser and go to the URL shown in the terminal (usually):

**http://127.0.0.1:8000**

Enjoy fully private, offline AI in your language!

---

## ✨ Features

- Fully offline after initial setup
- English ↔ Hindi bidirectional support
- Clean, responsive web interface
- No data leaves your machine
- Easy to extend with new models or tasks

---
## ⚠️ Dependencies & offline packaging note

- Installing Python packages from `requirements.txt` typically requires internet access. To create a fully-offline installer for end users, build a portable bundle (e.g., wheelhouse, Python embeddable, or a packaged EXE).  
- If you plan to distribute the project as a ZIP to offline users, include the downloaded `models/` folder and either a portable Python runtime or a pre-built binary so the recipient does not need to run `pip` on their machine.

---

## 🏅 Credits


DweepLang uses open-source translation models from the Helsinki-NLP / OPUS-MT project:

- [Helsinki-NLP/opus-mt-en-hi](https://huggingface.co/Helsinki-NLP/opus-mt-en-hi) (English → Hindi)  
- [Helsinki-NLP/opus-mt-hi-en](https://huggingface.co/Helsinki-NLP/opus-mt-hi-en) (Hindi → English)

These models are developed by the University of Helsinki and the OPUS community. Please follow their licenses when redistributing model weights.
---

Made with ❤️ for privacy-first, local AI in Indian languages.

For any queries email at : adarshsoloman196@gmail.com
