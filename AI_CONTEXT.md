# AI_CONTEXT - Mühendislik Asistanı Projesi

## Proje Özeti

**Tam Adı:** Offline Mühendislik Asistanı - RAG Tabanlı Jeneratör Bilgi Sistemi

**Amaç:** Askeri jeneratörlerin bakım, arıza tespiti ve teknik bilgi yönetimi için tamamen offline çalışan, yapay zeka destekli bir bilgi sistemi.

**Teknoloji:** RAG (Retrieval-Augmented Generation) mimarisi, Ollama (offline LLM), Python, Streamlit

**Hedef Kullanıcı:** Teknik personel ve mühendisler (kod bilgisi gerektirmez)

---

## Mimari Genel Bakış

### Sistem Bileşenleri

```
┌─────────────────────────────────────────────────┐
│          Kullanıcı Arayüzleri                   │
│  ┌──────────────┐      ┌──────────────┐        │
│  │ Web GUI      │      │ CLI          │        │
│  │ (Streamlit)  │      │ (argparse)   │        │
│  └──────────────┘      └──────────────┘        │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│          EngineeringAssistant                   │
│  (Ana Orkestrasyon Katmanı)                     │
└────┬──────────────────────────────────────┬────┘
     │                                       │
┌────▼──────────────┐            ┌──────────▼─────┐
│ RAGEngine         │            │ FaultCodeManager│
│ - Embedder        │            │ - JSON DB      │
│ - VectorStore     │            │ - Search       │
│ - OllamaLLM       │            │ - Formatting   │
└───────┬───────────┘            └────────────────┘
        │
┌───────▼───────────┐
│ DocumentProcessor │
│ - PDFReader       │
│ - TextChunker     │
└───────────────────┘
```

### Veri Akışı

**Training (Offline Setup):**
```
PDF Manueller → DocumentProcessor → Chunks → Embedder → VectorStore → Disk (vectordb.pkl)
```

**Sorgulama (Inference):**
```
Kullanıcı Sorusu → Embedder → VectorStore (similarity search) → Top-k Chunks
                                                                      ↓
Arıza Kodları (opsiyonel) ────────────────────────────────→ Context Birleştirme
                                                                      ↓
                                                              Ollama LLM
                                                                      ↓
                                                              Türkçe Cevap
```

---

## Klasör Yapısı ve Sorumluluklar

```
local_ai_project/
│
├── src/                          # Core modüller
│   ├── assistant.py              # Ana orkestrasyon, tüm bileşenleri birleştirir
│   ├── rag_engine.py             # RAG pipeline (Embedder, VectorStore, OllamaLLM)
│   ├── document_processor.py    # PDF okuma ve chunking
│   └── fault_code_manager.py    # JSON arıza kodu CRUD
│
├── dokumanlar/                   # Veri katmanı
│   ├── ariza_kodlari.json        # 15 jeneratör arıza kodu veritabanı
│   ├── manueller/                # Hassas PDF'ler (.gitignore ile korunur)
│   │   └── .gitkeep
│   └── README.md
│
├── scripts/
│   └── train_rag.py              # Training script (PDF → Vektör DB)
│
├── tests/
│   ├── test_fault_codes.py       # Pytest testleri
│   └── test_ollama_connection.py # Ollama bağlantı testi
│
├── examples/
│   └── usage_example.py          # Kullanım örnekleri
│
├── data/                         # Generated (training sonrası oluşur)
│   └── vector_store/
│       └── vectordb.pkl          # FAISS vektör index + chunk metadata
│
├── app.py                        # Streamlit web arayüzü (5 sayfa)
├── main.py                       # CLI arayüzü
├── BASLA.bat                     # Windows kolay başlatma
├── requirements.txt              # Python bağımlılıkları
├── .env.example                  # Konfigürasyon şablonu
├── .gitignore                    # Hassas dosya koruması
├── README.md                     # Genel dokümantasyon
├── KULLANIM_KILAVUZU.md         # Detaylı kullanım rehberi
└── BASLANGIC.md                  # Hızlı başlangıç
```

---

## Core Modül Detayları

### `src/assistant.py`

**Sınıf:** `EngineeringAssistant`

**Sorumluluk:** Tüm bileşenleri orkestre eder. Kullanıcı sorusunu alır, arıza kodlarında arar, RAG'den context çeker, Ollama ile cevap üretir.

**Önemli Metodlar:**
- `query(question, top_k=3)` → Kullanıcı sorusuna cevap ver
- `analyze_fault(code)` → Arıza kodu detaylı analizi
- `search_faults_by_symptom(symptom)` → Belirti arama
- `interactive_mode()` → CLI interaktif mod

**Bağımlılıklar:**
- `RAGEngine` (RAG sistemi)
- `FaultCodeManager` (arıza kodları)

### `src/rag_engine.py`

**Sınıflar:**
1. `Embedder` - sentence-transformers (all-MiniLM-L6-v2, 384 dim)
2. `VectorStore` - FAISS benzeri (cosine similarity, numpy-based)
3. `OllamaLLM` - Ollama Python SDK ile entegrasyon
4. `RAGEngine` - Ana pipeline

**Kritik Detaylar:**
- **Offline:** Embedding modeli ilk çalıştırmada indirilir, sonra offline
- **Vektör DB:** Pickle ile kaydedilir (`vectordb.pkl`)
- **Top-k:** Varsayılan 3 chunk döndürür
- **Prompt Template:** System prompt Türkçe, jeneratör uzmanı persona

**Metodlar:**
- `add_documents(chunks)` → Training sırasında chunk'ları ekle
- `retrieve_context(query, top_k)` → Query için en yakın chunk'ları bul
- `generate_answer(query, context, fault_info)` → Ollama ile cevap üret

### `src/document_processor.py`

**Sınıflar:**
1. `PDFReader` - PyPDF2 ile PDF okuma
2. `TextChunker` - Overlap'li chunking (800 char, 200 overlap)
3. `DocumentProcessor` - Toplu işleme

**Chunking Stratejisi:**
- Chunk size: 800 karakter
- Overlap: 200 karakter
- Cümle sınırında kesme (nokta, soru işareti, ünlem)
- Metadata: source, chunk_id, start_char, end_char

**Metodlar:**
- `process_pdf(pdf_path)` → Tek PDF işle
- `process_all_pdfs(folder_path)` → Klasördeki tüm PDF'leri işle

### `src/fault_code_manager.py`

**Sınıf:** `FaultCodeManager`

**Veri Kaynağı:** `dokumanlar/ariza_kodlari.json`

**Şema:**
```json
{
  "code": "E101",
  "name": "Düşük Yağ Basıncı",
  "severity": "CRITICAL|HIGH|MEDIUM",
  "category": "Yağlama Sistemi",
  "symptoms": [...],
  "causes": [...],
  "solutions": [...],
  "maintenance_interval_hours": 500,
  "priority": 1
}
```

**Metodlar:**
- `search_by_code(code)` → Direkt kod arama
- `search_by_symptom(symptom)` → Belirti metni arama (fuzzy)
- `search_by_category(category)` → Kategori filtreleme
- `format_fault_info(fault)` → Okunabilir metin formatlama

---

## Teknoloji Stack

### Backend
- **Python:** 3.9+
- **LLM:** Ollama (mistral veya llama2)
- **Embedding:** sentence-transformers (all-MiniLM-L6-v2)
- **Vektör DB:** FAISS-compatible (numpy-based cosine similarity)
- **PDF:** PyPDF2
- **RAG Framework:** Langchain (opsiyonel helper)

### Frontend
- **Web:** Streamlit 1.28+
- **CLI:** argparse

### Data
- **Arıza Kodları:** JSON (15 adet)
- **Manueller:** PDF (kullanıcı ekler)
- **Vektör DB:** Pickle (FAISS index + metadata)

### Dependencies
```
PyPDF2>=3.0.0
sentence-transformers>=2.2.0
faiss-cpu>=1.7.4
ollama>=0.1.0
langchain>=0.1.0
streamlit>=1.28.0
python-dotenv>=1.0.0
pytest>=7.4.0
```

---

## Konfigürasyon (.env)

```env
# Ollama
OLLAMA_MODEL=mistral
OLLAMA_URL=http://localhost:11434

# RAG
CHUNK_SIZE=800
CHUNK_OVERLAP=200
TOP_K_RESULTS=3
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Paths
VECTOR_DB_PATH=./data/vector_store/vectordb.pkl
MANUALS_FOLDER=dokumanlar/manueller
```

---

## Workflow'lar

### Training Workflow

```python
# 1. PDF'ler manueller/ klasöründe olmalı
# 2. scripts/train_rag.py çalıştır

processor = DocumentProcessor(chunk_size=800, overlap=200)
chunks = processor.process_all_pdfs("dokumanlar/manueller")

rag = RAGEngine(embedding_model="all-MiniLM-L6-v2")
rag.add_documents(chunks)  # Embedding oluştur
rag.save_vector_db("./data/vector_store/vectordb.pkl")
```

### Query Workflow

```python
assistant = EngineeringAssistant()

# Arıza kodlarında ara
fault_results = assistant.fault_manager.search_by_symptom(question)

# RAG'den context al
context = assistant.rag_engine.retrieve_context(question, top_k=3)

# Ollama ile cevap üret
answer = assistant.rag_engine.generate_answer(
    query=question,
    context_chunks=context,
    fault_info=fault_results[0] if fault_results else None
)
```

---

## Önemli Kısıtlamalar ve Kararlar

### Güvenlik
- **Hassas PDF'ler:** `dokumanlar/manueller/**/*.pdf` `.gitignore`'da
- **Vektör DB:** Generated, `.gitignore`'da
- **Ortam değişkenleri:** `.env` `.gitignore`'da

### Offline-First
- **LLM:** Ollama (internet gerektirmez)
- **Embedding:** İlk indirmeden sonra offline
- **Tüm işlemler:** Yerel (API key yok)

### Dil
- **UI:** Türkçe
- **Kod:** İngilizce (docstring'ler Türkçe)
- **Dokümanlar:** Türkçe
- **LLM Promptları:** Türkçe

### Design Decisions
1. **FAISS yerine Numpy:** Basitlik için (küçük veri setleri)
2. **Pickle VectorDB:** Taşınabilirlik
3. **Streamlit:** Hızlı geliştirme, kod gerektirmez
4. **Ollama:** Offline, ücretsiz

---

## Kullanım Senaryoları

### Senaryo 1: Arıza Kodu Analizi
```
Kullanıcı: "E101 ne demek?"
→ FaultCodeManager.search_by_code("E101")
→ Formatlanmış çıktı (belirtiler, nedenler, çözümler)
```

### Senaryo 2: Belirti Bazlı Arama
```
Kullanıcı: "Jeneratörde titreşim var"
→ FaultCodeManager.search_by_symptom("titreşim")
→ İlgili arıza kodları listesi (E401, E402)
```

### Senaryo 3: Doküman Tabanlı Sorgulama
```
Kullanıcı: "500 saatlik bakımda hangi filtreler değişir?"
→ RAGEngine.retrieve_context(query, top_k=3)
→ PDF'lerden ilgili chunk'lar
→ OllamaLLM.generate(system + context + query)
→ "500 saatlik bakımda motor yağ filtresi ve yakıt filtresi değiştirilmelidir..."
```

---

## Test Stratejisi

### Unit Tests
```bash
pytest tests/test_fault_codes.py -v
```
- JSON yükleme
- Kod arama
- Belirti arama
- Formatlama

### Integration Tests
```bash
python tests/test_ollama_connection.py
```
- Ollama bağlantı
- Model varlık
- Cevap üretimi

### Manual Tests
```bash
python examples/usage_example.py
python main.py fault E101
python main.py query "test sorusu"
```

---

## Deployment Notları

### Kullanıcı Setup (Windows)
1. Python 3.9+ kurulu
2. Ollama kurulu (`ollama pull mistral`)
3. `BASLA.bat` çalıştır
4. PDF'leri web arayüzünden yükle
5. Training yap
6. Kullan

### Production Considerations
- **Veri Boyutu:** 100+ PDF için FAISS kullanılmalı
- **Performans:** GPU-accelerated embedding için CUDA
- **Ölçekleme:** Çok kullanıcılı ise FastAPI + Redis cache

---

## Gelecek İyileştirmeler

### Kısa Vadeli
- [ ] Gerçek FAISS entegrasyonu (büyük veri için)
- [ ] OCR desteği (taranan PDF'ler)
- [ ] Excel/Word doküman desteği
- [ ] Vektör DB istatistikleri (kaç chunk, coverage vb.)

### Orta Vadeli
- [ ] Çok dilli destek (İngilizce manual okuma)
- [ ] Sesli komut (speech-to-text)
- [ ] Raporlama modülü (bakım geçmişi)
- [ ] Veritabanı entegrasyonu (PostgreSQL)

### Uzun Vadeli
- [ ] OpenProject entegrasyonu (kestirimci bakım)
- [ ] Mobil uygulama
- [ ] Multi-tenant SaaS

---

## Sorun Giderme Referansı

### "Ollama bulunamadı"
→ `ollama pull mistral` çalıştır
→ `ollama serve` kontrolü

### "Training başarısız"
→ PDF'lerin `dokumanlar/manueller/` klasöründe olduğunu kontrol et
→ PyPDF2 bazı PDF'leri okuyamayabilir (re-export et)

### "Cevaplar alakasız"
→ Training yap (RAG olmadan sadece arıza kodları çalışır)
→ PDF kalitesini kontrol et
→ Daha fazla PDF ekle

### Web arayüzü açılmıyor
→ `streamlit run app.py --server.port 8502` (farklı port dene)
→ Firewall/antivirus kontrolü

---

## AI Asistan Notları

**Bu dosyayı okurken:**
1. Mimari anla → Modüller arası bağlantıları gör
2. Veri akışını takip et → Training vs. Inference
3. Hassas dosyalara dikkat → .gitignore kuralları
4. Offline-first yaklaşımı → API key yok, Ollama kullan
5. Türkçe öncelik → UI ve dokümanlar Türkçe

**Kod değişikliği yaparken:**
- `src/` modülleri bağımsız (unit test edilebilir)
- `EngineeringAssistant` orkestrasyon katmanı (değişiklik buradan)
- Yeni özellik → Önce `assistant.py`'a ekle
- UI değişikliği → `app.py` (Streamlit) veya `main.py` (CLI)

**Yeni özellik eklerken:**
1. `src/` altında yeni modül
2. `assistant.py`'a entegre et
3. `app.py` ve/veya `main.py`'a UI ekle
4. Test yaz (`tests/`)
5. Doküman güncelle (`README.md`)

---

**Son Güncelleme:** 2026-01-06
**Versiyon:** 1.0
**Maintainer:** AI Engineering Team
