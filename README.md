# Offline Mühendislik Asistanı

Jeneratör teknik dokümanlarını işleyen ve arıza analizi yapan yapay zeka destekli offline bilgi sistemi.

## Genel Bakış

Bu sistem, PDF formatındaki teknik manüelleri analiz ederek RAG (Retrieval-Augmented Generation) teknolojisi ile sorulara yanıt verir. Tüm işlemler yerel ortamda gerçekleştirilir ve internet bağlantısı gerektirmez.

## Temel Özellikler

- Tamamen offline çalışma - Veri güvenliği
- PDF doküman işleme ve indeksleme
- Çok jeneratörlü arıza kodu yönetimi
- Doğal dil sorgu desteği
- Web tabanlı kullanıcı arayüzü
- Türkçe dil desteği

## Hızlı Başlangıç

### Ön Gereksinimler

**Ollama Kurulumu**

Sistem, local LLM çalıştırmak için Ollama kullanmaktadır:

1. [Ollama](https://ollama.ai/download) indirip kurun
2. Kurulum tamamlandıktan sonra devam edin

### Kurulum

**Windows Kullanıcıları İçin**

Projeyi indirdikten sonra `BASLA.bat` dosyasını çalıştırın. Script otomatik olarak:

- Python sanal ortamı oluşturur
- Gerekli bağımlılıkları yükler
- Ollama modellerini kontrol eder (eksik modelleri indirme seçeneği sunar)
- Web arayüzünü başlatır

İlk çalıştırmada model indirme sürecinden dolayı kurulum 5-10 dakika sürebilir. Sonraki çalıştırmalarda sistem birkaç saniye içinde hazır hale gelir.

**Diğer Platformlar veya Manuel Kurulum**

```bash
# Sanal ortam oluştur
python -m venv venv

# Sanal ortamı aktifleştir
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Ollama modellerini yükle
ollama pull mistral
ollama pull llama3.2:3b

# Web arayüzünü başlat
streamlit run app.py
```

### Kullanım

Web arayüzü `http://localhost:8501` adresinde açılacaktır.

**Training İşlemi**

1. Training sekmesine gidin
2. PDF dokümanları yükleyin (sürükle-bırak veya dosya seçici)
3. "Training Başlat" butonuna tıklayın
4. İşlem tamamlandığında sistem kullanıma hazırdır

**Sorgulama**

Sorgulama sekmesinden sisteme soru sorabilirsiniz:

Örnek:
- "E101 arıza kodunun anlamı nedir?"
- "Cos 0.9 güç faktöründe voltaj düşüşünün nedenleri nelerdir?"
- "500 saatlik bakım periyodunda yapılması gereken işlemler"

Detaylı kullanım bilgisi için `KULLANIM_KILAVUZU.md` dosyasına bakınız.

---

## Sistem Özellikleri

**Offline Çalışma**  
Tüm işlemler yerel sistemde gerçekleştirilir. Veri güvenliği sağlanmıştır.

**RAG Sistemi**  
Retrieval-Augmented Generation teknolojisi ile dokümanlardan ilgili bilgiler çıkarılır ve yanıtlarda kullanılır.

**Çok Jeneratör Desteği**  
Farklı jeneratör modellerine özel arıza kodları tanımlanabilir ve filtrelenebilir.

**Arıza Kodu Yönetimi**  
Jeneratöre özgü arıza kodları JSON formatında saklanır ve kategorize edilir.

---

## Gelişmiş Kullanım

### Komut Satırı

Terminalden kullanmak için:

**PDF Manuellerini Ekleme**

Jeneratör manuellerinizi `dokumanlar/manueller/` klasörüne kopyalayın:

```
dokumanlar/
  └── manueller/
      ├── jenerator_manual_1.pdf
      ├── bakim_klavuzu.pdf
      └── ...
```

**RAG Sistemini Eğitme (Training)**

```bash
python scripts/train_rag.py
```

Bu komut:
- `dokumanlar/manueller/` içindeki tüm PDF'leri okur
- Metinleri parçalara böler (chunking)
- Her parça için embedding oluşturur
- Vektör veritabanına kaydeder

**Asistanı Kullanma**

Arıza kodu sorgulama:
```bash
python main.py fault E101
```

Doküman tabanlı sorgulama:
```bash
python main.py query "500 saatlik bakımda hangi filtreler değişir?"
```

İnteraktif mod:
```bash
python main.py interactive
```

---

## Proje Yapısı

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
├── app.py                      # Web arayüzü
├── BASLA.bat                   # Windows başlatma scripti
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Testler

```bash
# Tüm testler
pytest tests/ -v

# Ollama bağlantı testi
python tests/test_ollama_connection.py

# Arıza kodu testleri
pytest tests/test_fault_codes.py -v
```

---

## Sorun Giderme

### Ollama Bağlantı Hatası

Sistem Ollama servisine bağlanamıyorsa:

1. Ollama'nın kurulu olduğundan emin olun: [https://ollama.ai/download](https://ollama.ai/download)
2. `BASLA.bat` dosyasını tekrar çalıştırın
3. Manuel kontrol için terminal açın ve `ollama list` komutunu çalıştırın

### Model Bulunamadı Hatası

Gerekli modeller yüklü değilse:

```bash
ollama pull mistral
ollama pull llama3.2:3b
```

Alternatif olarak, `BASLA.bat` ilk çalıştırmada model indirme seçeneği sunacaktır.

### PDF İşleme Hataları

Bazı PDF dosyaları şifreli veya taranmış görüntü formatında olabilir. Bu durumda PDF'i yeniden dışa aktarmayı deneyin.

### Training Performansı

İlk training işleminde embedding modeli indirilir (yaklaşık 100MB). Bu işlem bir kerelik olup sonraki trainingler daha hızlı tamamlanır.

### Ek Destek

Detaylı troubleshooting bilgisi için `KULLANIM_KILAVUZU.md` dosyasına başvurunuz.

---

## Güvenlik

- PDF dokümanları `dokumanlar/manueller/` dizininde saklanır ve `.gitignore` ile versiyon kontrol sistemine dahil edilmez
- Tüm işlemler local sistemde gerçekleştirilir
- Hassas veriler harici bir sunucuya iletilmez

---

## Katkıda Bulunma

1. Projeyi fork edin
2. Feature branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni özellik eklendi'`)
4. Branch'i push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request oluşturun

---

## Lisans

MIT License

---

**Not:** Bu sistem jeneratör bakım uygulamaları için geliştirilmiştir ancak farklı teknik doküman türleri için de kullanılabilir.
