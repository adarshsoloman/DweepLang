import torch
from transformers import MarianMTModel, MarianTokenizer
import os
from tqdm import tqdm

# Models to download
MODELS = {
    "en-hi": {
        "name": "Helsinki-NLP/opus-mt-en-hi",
        "info": {
            "dataset": "opus",
            "model": "transformer-align",
            "source": "English",
            "target": "Hindi",
            "preprocessing": "normalization + SentencePiece (spm32k,spm32k)"
        }
    },
    "hi-en": {
        "name": "Helsinki-NLP/opus-mt-hi-en",
        "info": {
            "dataset": "opus",
            "model": "transformer",
            "source": "Hindi",
            "target": "English",
            "preprocessing": "normalization + tokenization + BPE"
        }
    }
}

BASE_PATH = "./models"

def print_model_info(direction, info):
    """Print model information"""
    print(f"\n📋 Model Information:")
    print(f"   Direction:      {info['source']} → {info['target']}")
    print(f"   Dataset:        {info['dataset']}")
    print(f"   Architecture:   {info['model']}")
    print(f"   Preprocessing:  {info['preprocessing']}")

def download_and_save_model(model_name, save_folder, model_info):
    """Download Helsinki-NLP OPUS-MT model with progress"""
    
    os.makedirs(save_folder, exist_ok=True)
    
    print(f"\n📥 Downloading {model_name}")
    print(f"📂 Save location: {save_folder}")
    
    print_model_info(None, model_info)
    
    print("\n⏳ Downloading...")
    print("-" * 60)
    
    try:
        # Download tokenizer
        print("   [1/2] Downloading tokenizer...")
        with tqdm(total=100, desc="   Tokenizer", unit="%", ncols=70, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
            tokenizer = MarianTokenizer.from_pretrained(model_name)
            pbar.update(50)
            tokenizer.save_pretrained(save_folder)
            pbar.update(50)
        print("   ✓ Tokenizer saved")
        
        # Download model
        print("   [2/2] Downloading model weights...")
        with tqdm(total=100, desc="   Model", unit="%", ncols=70, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
            model = MarianMTModel.from_pretrained(model_name)
            pbar.update(50)
            model.save_pretrained(save_folder)
            pbar.update(50)
        print("   ✓ Model saved")
        
        # Get model size
        model_size = sum(
            os.path.getsize(os.path.join(save_folder, f)) 
            for f in os.listdir(save_folder) 
            if os.path.isfile(os.path.join(save_folder, f))
        )
        model_size_mb = model_size / (1024 * 1024)
        print(f"   ℹ Model size: {model_size_mb:.2f} MB")
        
        return True
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_model(model_path, direction):
    """Test the downloaded model"""
    print(f"\n   🧪 Testing model...")
    
    try:
        tokenizer = MarianTokenizer.from_pretrained(model_path)
        model = MarianMTModel.from_pretrained(model_path)
        
        # Test sentences
        tests = {
            "en-hi": [
                "Hello, how are you?",
                "Good morning!",
                "Thank you very much."
            ],
            "hi-en": [
                "नमस्ते, आप कैसे हैं?",
                "शुभ प्रभात!",
                "बहुत बहुत धन्यवाद।"
            ]
        }
        
        test_sentences = tests.get(direction, ["Hello"])
        
        print(f"   Testing with {len(test_sentences)} sentences:")
        
        for i, test_text in enumerate(test_sentences, 1):
            inputs = tokenizer(test_text, return_tensors="pt", padding=True)
            with torch.no_grad():
                outputs = model.generate(**inputs, max_length=128)
            translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            print(f"   [{i}] {test_text}")
            print(f"       → {translation}")
        
        print(f"   ✓ All tests passed!")
        return True
        
    except Exception as e:
        print(f"   ✗ Test failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("📦 Helsinki-NLP OPUS-MT Model Downloader")
    print("=" * 60)
    print("\nThis script will download:")
    for direction, model_data in MODELS.items():
        info = model_data["info"]
        print(f"  • {info['source']} → {info['target']} ({model_data['name']})")
    print("\n" + "=" * 60)
    
    # Ask for confirmation
    proceed = input("\n🤔 Proceed with download? (y/n): ").strip().lower()
    if proceed != 'y':
        print("❌ Download cancelled")
        exit(0)
    
    success_count = 0
    
    for direction, model_data in MODELS.items():
        model_name = model_data["name"]
        model_info = model_data["info"]
        save_path = os.path.join(BASE_PATH, direction)
        
        print("\n" + "=" * 60)
        print(f"🔄 Processing: {direction}")
        print("=" * 60)
        
        # Check if already exists
        if os.path.exists(save_path) and os.listdir(save_path):
            print(f"📁 Model already exists at: {save_path}")
            user_input = input(f"   Re-download? (y/n): ").strip().lower()
            if user_input != 'y':
                print(f"   ⏭ Skipping download")
                
                # Test existing model
                if test_model(save_path, direction):
                    success_count += 1
                    print(f"   ✅ {direction} verified!")
                continue
            else:
                # Remove old files
                import shutil
                shutil.rmtree(save_path)
                print(f"   🗑 Removed old files")
        
        # Download
        if download_and_save_model(model_name, save_path, model_info):
            # Test the model
            if test_model(save_path, direction):
                success_count += 1
                print(f"   ✅ {direction} complete!")
            else:
                print(f"   ⚠ {direction} downloaded but test failed")
        else:
            print(f"   ❌ {direction} download failed")
    
    # Final summary
    print("\n" + "=" * 60)
    print("📊 Download Summary")
    print("=" * 60)
    print(f"✓ Successfully downloaded: {success_count}/2 models")
    
    if success_count == 2:
        print("\n✅ All models ready to use!")
        print(f"📂 Models location: {os.path.abspath(BASE_PATH)}")
        print("\n" + "=" * 60)
        print("🚀 Next Steps:")
        print("=" * 60)
        print("1. Run the translation app:")
        print("   Windows: run.bat")
        print("   Linux/Mac: ./run.sh")
        print("\n2. Or test directly:")
        print("   python server/app.py")
    else:
        print("\n⚠ Some models failed. Please check errors above.")
        print("💡 You can try running the script again.")
    
    print("=" * 60)