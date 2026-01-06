# BAŞLANGIÇ REHBERİ

## ⚡ Hızlı Başlangıç

### 1. İlk Kurulum (Sadece Bir Kez)

```bash
# 1. Python var mı kontrol edin
python --version

# Python yoksa indirin: https://www.python.org/downloads/

# 2. Ollama yükleyin
# https://ollama.ai/download
# Sonra:
ollama pull mistral

# 3. Bu klasördeyken:
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Sistemi Başlatın

**Kolay Yol (Windows):**
```
BASLA.bat dosyasına çift tıklayın
```

**Manuel Yol:**
```bash
streamlit run app.py
```

Tarayıcıda `http://localhost:8501` açılacak.

---

## 📱 Web Arayüzü Kullanımı

### Ana Özellikler

1. **🏠 Ana Sayfa**: Durum özeti
2. **📚 Training**: PDF yükle ve sistemi eğit
3. **💬 Sorgulama**: AI chat ile soru sor
4. **🔍 Arıza Kodları**: Hata kodu analizi
5. **⚙️ Ayarlar**: Veri yönetimi

### Training Nasıl Yapılır?

1. Sol menü → **📚 Training**
2. PDF dosyalarını seç ve **Kaydet**
3. **🚀 Training'i Başlat** tıkla
4. 2-10 dakika bekle
5. ✅ Tamamlandı!

### Sorgulama Nasıl Yapılır?

1. Sol menü → **💬 Sorgulama**
2. Alttaki kutucuğa sorunuzu yazın:
   - "500 saatlik bakımda neler yapılır?"
   - "Yağ seviyesi nasıl kontrol edilir?"
3. Enter'a basın
4. AI cevap verecek

### Arıza Kodu Nasıl Aranır?

1. Sol menü → **🔍 Arıza Kodları**
2. **Kod Ara** sekmesinde: `E101` yazın ve ara
3. **Belirti Ara** sekmesinde: `titreşim` yazın ve ara
4. Detaylı bilgi görülür

---

## ⚠️ Önemli Notlar

- **İlk kullanımda** bağımlılık yüklemesi 2-5 dakika sürer
- **Training sırasında** sayfayı kapatmayın
- **PDF'ler** `dokumanlar/manueller/` klasöründe saklanır
- **GitHub'a yüklenmeyen** hassas dosyalar: PDF'ler, .env, vektör DB

---

## 🔧 Sorun mu Var?

### Ollama Hatası
```bash
ollama pull mistral
```

### Python Hatası
Python'u PATH'e ekleyerek yeniden kurun

### Bağımlılık Hatası
```bash
pip install -r requirements.txt
```

Detaylı bilgi için: **KULLANIM_KILAVUZU.md**

---

**İyi Çalışmalar! 🚀**
