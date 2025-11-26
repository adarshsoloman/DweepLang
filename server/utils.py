import torch
from transformers import MarianMTModel, MarianTokenizer
import os

# Get the directory where utils.py is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up one level to DweepLingo root, then into models
BASE_PATH = os.path.join(SCRIPT_DIR, "..", "models")

# Different models for each direction
MODELS = {
    "en-hi": os.path.join(BASE_PATH, "en-hi"),   # English → Hindi
    "hi-en": os.path.join(BASE_PATH, "hi-en"),   # Hindi → English
}

class TranslationModel:
    def __init__(self, direction, device="cuda"):
        self.device = device if torch.cuda.is_available() else "cpu"
        self.direction = direction
        self.model_name = MODELS.get(direction)
        self.tokenizer = None
        self.model = None
        
        if not self.model_name:
            raise ValueError(f"Unknown direction: {direction}")
        
        # Check if local model exists
        if not os.path.exists(self.model_name):
            raise FileNotFoundError(
                f"❌ Model not found at: {self.model_name}\n"
                f"Please run download.py first to download the models!"
            )
        
        print(f"🔧 Device: {self.device}")
        print(f"📦 Model: {self.model_name} (LOCAL)")
        
    def load_model(self):
        """Load model from local path (OFFLINE)"""
        try:
            print(f"📂 Loading from local path: {self.model_name}")
            
            # Load tokenizer - OFFLINE MODE
            self.tokenizer = MarianTokenizer.from_pretrained(
                self.model_name,
                local_files_only=True  # ✅ Force offline
            )
            print("✓ Tokenizer loaded")
            
            # Load model - OFFLINE MODE
            if self.device == "cuda":
                self.model = MarianMTModel.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float16,
                    local_files_only=True  # ✅ Force offline
                ).to(self.device)
                print("✓ Model loaded (GPU - FP16)")
            else:
                self.model = MarianMTModel.from_pretrained(
                    self.model_name,
                    local_files_only=True  # ✅ Force offline
                )
                print("✓ Model loaded (CPU)")
            
            self.model.eval()
            print("✓ Model ready")
            return True
            
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def translate(self, text, max_length=128):
        """Translate text"""
        try:
            if not self.model or not self.tokenizer:
                raise Exception("Model not properly initialized")
            
            if not text or not text.strip():
                raise Exception("Empty text provided")
            
            # Tokenize
            inputs = self.tokenizer(
                text, 
                return_tensors="pt", 
                padding=True, 
                truncation=True, 
                max_length=512
            )
            
            # Move to device
            if self.device == "cuda":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate translation
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    num_beams=4,
                    early_stopping=True
                )
            
            # Decode
            translation = self.tokenizer.decode(
                outputs[0], 
                skip_special_tokens=True
            )
            
            return translation
            
        except Exception as e:
            raise Exception(f"Translation error: {str(e)}")