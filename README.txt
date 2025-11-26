============================================================
                  DweepLang
     Localized • Offline-First • LLM Interface
============================================================

1. What is DweepLang?
============================================================
DweepLang is a proof-of-concept, full-stack application that
provides a completely localized and offline-first interface
for Large Language Models (LLMs).

It works as a lightweight wrapper so you can run powerful
language models directly on your own computer — no internet
required after the initial setup.

Key benefits:
• 100% private — your data never leaves your machine
• Works offline forever after one-time model download
• Supports English ↔ Hindi translation & processing
• Easy to extend for summarization, Q&A, custom prompts, etc.

============================================================
2. Project File Structure
============================================================

DweepLingo/
├── models/                  # Downloaded model files (not in repo)
│   ├── en-hi/               # English → Hindi model
│   │   ├── config.json
│   │   ├── generation_config.json
│   │   ├── pytorch_model.bin        # ← huge file
│   │   ├── tokenizer.json
│   │   ├── tokenizer_config.json
│   │   ├── special_tokens_map.json
│   │   └── sentencepiece.bpe.model (if used)
│   │
│   └── hi-en/               # Hindi → English model
│       └── (same files as above)
│
├── server/
│   ├── app.py               # Main backend server (Flask/FastAPI)
│   └── utils.py             # Model loading & inference helpers
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── run.bat                  # One-click start for Windows
├── run.sh                   # One-click start for Linux/macOS
├── download.py              # Automatically downloads models
├── requirements.txt         # Python dependencies
└── README.txt               # ← You are reading this file

Note: Large model files (pytorch_model.bin, .safetensors, etc.)
      are NOT in the Git repository because of size limits.
      They are downloaded automatically by download.py.

============================================================
3. Getting Started – Installation & Setup
============================================================

Step 3a – Install Python dependencies
------------------------------------
Recommended (fastest):
    pip install uv          # (one-time only if you don't have uv)
    uv sync

Alternative (standard):
    pip install -r requirements.txt

Step 3b – Download models (one-time, requires internet)
-------------------------------------------------------
    python download.py

This script will create the models/ folder and place all
necessary files in the right places. After this step you can
disconnect from the internet forever.

============================================================
4. Running the Application
============================================================

Option A – Recommended (one-click)

Windows:
    .\run.bat

Linux / macOS:
    ./run.sh

Option B – Manual

    cd server
    python app.py

Open your browser and go to the address shown in the terminal
(usually http://127.0.0.1:5000).

You now have a fully private, offline AI assistant running
locally in English and Hindi!

============================================================
Enjoy your private, local LLM experience!
Made with love for offline-first AI in Indian languages.
============================================================
