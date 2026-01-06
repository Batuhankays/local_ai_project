# Mühendislik Asistanı - Offline RAG Sistemi

**Tamamen offline çalışan** bir mühendislik bilgi asistanı. Jeneratör teknik dokümanlarını (PDF) okuyup, arıza kodlarını analiz eder ve Ollama kullanarak akıllı öneriler sunar.

## ✨ Özellikler

- 🔒 **Tamamen Offline**: İnternet bağlantısı gerektirmez (Ollama ile)
- 📚 **RAG Sistemi**: PDF manuellerden bilgi çıkarma
- 🔧 **Arıza Kodu Analizi**: Jeneratör hata kodları ve çözümleri
- 🤖 **Akıllı Sorgulama**: Doğal dilde soru sorma
- 🔐 **Güvenli**: Hassas PDF'ler GitHub'a yüklenmez

## 📋 Gereksinimler

### 1. Ollama Kurulumu

```bash
# Ollama'yı indirin: https://ollama.ai/download
# Kurulum sonrası model çekin:
ollama pull mistral
# veya
ollama pull llama2
```

### 2. Python Bağımlılıkları

```bash
pip install -r requirements.txt
```

## 🚀 Kurulum

### Adım 1: Sanal Ortam Oluşturun

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### Adım 2: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### Adım 3: Konfigürasyon

```bash
# .env dosyası oluşturun
copy .env.example .env
# veya Linux/Mac:
cp .env.example .env
```

## 🌐 Web Arayüzü (Önerilen)

**Kodlama bilmeden kullanmak için:**

### Kolay Başlatma (Windows)

```bash
# BASLA.bat dosyasına çift tıklayın
BASLA.bat
```

### Manuel Başlatma

```bash
streamlit run app.py
```

Tarayıcınızda `http://localhost:8501` açılacak.

### Web Arayüzü Özellikleri

- 📚 **Training Sayfası**: PDF yükleme ve training (sürükle-bırak)
- 💬 **Chat Arayüzü**: Soru-cevap (WhatsApp tarzı)
- 🔍 **Arıza Kodu Arama**: Görsel arayüz ile kod analizi
- ⚙️ **Ayarlar**: Veri yönetimi

**Detaylı bilgi:** [KULLANIM_KILAVUZU.md](KULLANIM_KILAVUZU.md)

---

## 💻 Komut Satırı (İleri Seviye)

Terminalden kullanmak için:

### 1. PDF Manuellerini Ekleme

Jeneratör manuellerinizi `dokumanlar/manueller/` klasörüne kopyalayın:

```
dokumanlar/
  └── manueller/
      ├── jenerator_manual_1.pdf
      ├── bakim_klavuzu.pdf
      └── ...
```

> ⚠️ **Önemli**: Bu dosyalar `.gitignore` ile korunuyor ve GitHub'a yüklenmeyecek.

### 2. RAG Sistemini Eğitme (Training)

```bash
python scripts/train_rag.py
```

Bu komut:
- `dokumanlar/manueller/` içindeki tüm PDF'leri okur
- Metinleri parçalara böler (chunking)
- Her parça için embedding oluşturur
- Vektör veritabanına kaydeder

**Beklenen Çıktı:**
```
✓ 5 PDF işlendi
✓ 234 chunk oluşturuldu
✓ Vektör DB kaydedildi: ./data/vector_store
```

### 3. Asistanı Kullanma

#### Arıza Kodu Sorgulama

```bash
python main.py fault E101
```

#### Doküman Tabanlı Sorgulama

```bash
python main.py query "500 saatlik bakımda hangi filtreler değişir?"
```

#### İnteraktif Mod

```bash
python main.py interactive
```

İnteraktif modda çalıştıktan sonra sorularınızı yazabilirsiniz:
```
🤖 Merhaba! Nasıl yardımcı olabilirim?
> E101 ne demek?
> Titreşim yüksekse ne yapmalıyım?
> exit (çıkmak için)
```

## 📁 Proje Yapısı

```
local_ai_project/
├── dokumanlar/
│   ├── ariza_kodlari.json      # Arıza kodları veritabanı
│   ├── manueller/              # Hassas PDF'ler (gitignore'da)
│   │   └── .gitkeep
│   └── README.md
├── src/
│   ├── assistant.py            # Ana asistan sınıfı
│   ├── document_processor.py   # PDF işleme
│   ├── fault_code_manager.py   # Arıza kodu yönetimi
│   └── rag_engine.py           # RAG motoru
├── scripts/
│   └── train_rag.py            # Training scripti
├── tests/
│   ├── test_fault_codes.py
│   └── test_ollama_connection.py
├── main.py                     # CLI arayüzü
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🧪 Testler

```bash
# Tüm testler
pytest tests/ -v

# Ollama bağlantı testi
python tests/test_ollama_connection.py

# Arıza kodu testleri
pytest tests/test_fault_codes.py -v
```

## 🔒 Güvenlik

- **Hassas PDF'ler**: `dokumanlar/manueller/` klasörü `.gitignore` ile korunur
- Her yeni ortamda (deployment, yeni makine) PDF'leri manuel olarak kopyalamanız gerekir
- `.env` dosyası da GitHub'a yüklenmez

## 🛠️ Sorun Giderme

### Ollama Bağlantı Hatası

```bash
# Ollama servisinin çalıştığından emin olun:
ollama list
# Model yoksa çekin:
ollama pull mistral
```

### PDF Okuma Hatası

PyPDF2 bazı PDF'leri okuyamayabilir. Alternatif olarak PDF'i tekrar export edin veya OCR kullanın.

### Embedding Hatası

İlk çalıştırmada sentence-transformers modeli indirecektir (~100MB). İnternet bağlantınızın olduğundan emin olun. İndirildikten sonra offline çalışır.

## 📝 Lisans

MIT License

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

---

**Not**: Bu sistem askeri jeneratör bakımı için tasarlanmıştır. Kendi dokümanlarınızı ekleyerek farklı alanlarda da kullanabilirsiniz.
