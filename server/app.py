from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from utils import TranslationModel
import os

app = FastAPI(title="DweepLingo Translation API")

# Models dictionary
models = {}

class TranslationRequest(BaseModel):
    text: str
    src_lang: str
    tgt_lang: str

class TranslationResponse(BaseModel):
    translation: str
    src_lang: str
    tgt_lang: str

@app.on_event("startup")
async def load_models():
    """Load translation models on startup"""
    print("="*60)
    print("🚀 DweepLingo Translation API Starting...")
    print("="*60)
    
    for direction in ["en-hi", "hi-en"]:
        print(f"\n📦 Loading {direction}...")
        try:
            model = TranslationModel(direction=direction, device="cpu")
            if model.load_model():
                models[direction] = model
                print(f"✓ {direction} ready")
            else:
                print(f"✗ {direction} failed")
        except Exception as e:
            print(f"✗ {direction} error: {e}")
    
    if not models:
        print("\n⚠ No models loaded!")
    
    print("\n" + "="*60)
    print("🌐 Frontend: http://127.0.0.1:8000")
    print("📖 API Docs: http://127.0.0.1:8000/docs")
    print("="*60)

@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """Translate text between English and Hindi"""
    try:
        # Determine direction
        if request.src_lang == "en" and request.tgt_lang == "hi":
            direction = "en-hi"
        elif request.src_lang == "hi" and request.tgt_lang == "en":
            direction = "hi-en"
        else:
            raise HTTPException(400, "Only en↔hi translation supported")
        
        # Check if model is loaded
        if direction not in models:
            raise HTTPException(503, f"Model {direction} not available")
        
        # Translate
        translation = models[direction].translate(request.text)
        
        return TranslationResponse(
            translation=translation,
            src_lang=request.src_lang,
            tgt_lang=request.tgt_lang
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Translation failed: {str(e)}")

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "models_loaded": list(models.keys()),
        "mode": "offline"
    }

# Serve frontend
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
async def root():
    """Serve the frontend"""
    return FileResponse(os.path.join(frontend_path, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)