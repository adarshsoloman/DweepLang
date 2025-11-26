#!/bin/bash

echo "============================================================"
echo "   DweepLang Translation App"
echo "============================================================"
echo ""

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/server"

echo "[1/3] Starting FastAPI server..."
echo ""

python app.py &
SERVER_PID=$!

echo "[2/3] Waiting for server to start..."
sleep 5

echo "[3/3] Opening browser..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    open http://127.0.0.1:8000
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open http://127.0.0.1:8000 2>/dev/null
fi

echo ""
echo "============================================================"
echo "Server is running at: http://127.0.0.1:8000"
echo "Press Ctrl+C to stop"
echo "============================================================"
echo ""

trap "kill $SERVER_PID 2>/dev/null; exit" INT
wait $SERVER_PID
```

## 9. `README.txt`
```
DweepLang Translation App
=========================

English ↔ Hindi Translation using IndicTrans2

Setup Instructions:
------------------
1. Install dependencies:
   pip install -r requirements.txt

2. Ensure models are in the models/ folder:
   - models/en-hi/
   - models/hi-en/

3. Run the app:
   - Windows: Double-click run.bat
   - Linux/Mac: ./run.sh

The app will open in your browser at http://127.0.0.1:8000

Features:
---------
- Translate between English and Hindi
- Swap languages with one click
- Clean, modern interface
- Fast local translation

Enjoy! 🌏