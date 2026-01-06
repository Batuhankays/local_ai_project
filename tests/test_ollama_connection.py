"""
Ollama Bağlantı Testi

Ollama servisinin çalıştığını ve model'in yüklü olduğunu kontrol eder.
"""

import sys
import os

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_ollama_connection():
    """Ollama bağlantısını test et"""
    try:
        import ollama
        
        print("🔍 Ollama bağlantısı kontrol ediliyor...\n")
        
        # Yüklü modelleri listele
        models = ollama.list()
        
        print("✓ Ollama servisine bağlanıldı")
        print(f"\n📋 Yüklü modeller:")
        
        if not models.get('models'):
            print("  ⚠️  Hiç model yüklü değil!")
            print("\n  Model yüklemek için:")
            print("    ollama pull mistral")
            print("    ollama pull llama2")
            return False
        
        for model in models['models']:
            model_name = model.get('name', 'Bilinmeyen')
            print(f"  • {model_name}")
        
        print("\n✅ Ollama hazır!")
        return True
    
    except ImportError:
        print("❌ 'ollama' paketi yüklü değil!")
        print("\n  Yüklemek için:")
        print("    pip install ollama")
        return False
    
    except Exception as e:
        print(f"❌ Ollama bağlantı hatası: {str(e)}")
        print("\n  Ollama servisini başlatmak için:")
        print("    ollama serve")
        print("\n  veya Ollama'yı yükleyin:")
        print("    https://ollama.ai/download")
        return False


def test_ollama_generation():
    """Basit bir prompt testi"""
    try:
        import ollama
        
        print("\n" + "=" * 60)
        print("🧪 Ollama cevap üretimi testi")
        print("=" * 60 + "\n")
        
        model = "mistral"
        prompt = "Merhaba! Bu bir test mesajıdır. Kısaca cevap ver."
        
        print(f"Model: {model}")
        print(f"Prompt: {prompt}\n")
        print("Cevap bekleniyor...\n")
        
        response = ollama.chat(
            model=model,
            messages=[
                {'role': 'user', 'content': prompt}
            ]
        )
        
        answer = response['message']['content']
        
        print(f"🤖 Cevap:\n{answer}\n")
        print("✅ Cevap üretimi başarılı!")
        
        return True
    
    except Exception as e:
        print(f"❌ Cevap üretim hatası: {str(e)}")
        
        if "model" in str(e).lower():
            print(f"\n  '{model}' modeli yüklü değil!")
            print(f"\n  Yüklemek için:")
            print(f"    ollama pull {model}")
        
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("OLLAMA BAĞLANTI TESTİ")
    print("=" * 60 + "\n")
    
    # Test 1: Bağlantı
    connection_ok = test_ollama_connection()
    
    # Test 2: Cevap üretimi (sadece bağlantı başarılıysa)
    if connection_ok:
        generation_ok = test_ollama_generation()
    else:
        print("\n⚠️  Bağlantı başarısız olduğu için cevap üretimi test edilmedi")
        generation_ok = False
    
    # Sonuç
    print("\n" + "=" * 60)
    if connection_ok and generation_ok:
        print("✅ TÜM TESTLER BAŞARILI!")
        print("\n🎯 Ollama kullanıma hazır")
    else:
        print("❌ BAZI TESTLER BAŞARISIZ")
        print("\n🔧 Yukarıdaki talimatları takip edin")
    print("=" * 60 + "\n")
