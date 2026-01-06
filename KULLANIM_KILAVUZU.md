# 🚀 Mühendislik Asistanı - Kullanım Kılavuzu

Kod yazmadan jeneratör bilgi sistemini kullanmak için adım adım rehber.

---

## 📋 İçindekiler

1. [İlk Kurulum](#ilk-kurulum)
2. [Sistemin Başlatılması](#sistemin-başlatılması)
3. [PDF Manuel Yükleme ve Training](#pdf-manuel-yükleme-ve-training)
4. [Sistemin Kullanımı](#sistemin-kullanımı)
5. [Sorun Giderme](#sorun-giderme)

---

## İlk Kurulum

### Adım 1: Python Kurulumu

1. [Python İndirin](https://www.python.org/downloads/) (3.9 veya üstü)
2. Kurulum sırasında **"Add Python to PATH"** kutucuğunu işaretleyin
3. Kurulumu tamamlayın

**Kontrol:**
```bash
# Terminal/CMD açın ve yazın:
python --version
```
✅ `Python 3.x.x` görmelisiniz

### Adım 2: Ollama Kurulumu

1. [Ollama İndirin](https://ollama.ai/download)
2. Kurulumu tamamlayın
3. Terminal açın ve model indirin:

```bash
ollama pull mistral
```

**Kontrol:**
```bash
ollama list
```
✅ `mistral` modelini görmelisiniz

### Adım 3: Proje Klasörünü İndirin

GitHub'dan projeyi indirin ve istediğiniz yere çıkarın.

Örnek: `C:\MuhendislikAsistani\`

---

## Sistemin Başlatılması

### 🎯 Kolay Yöntem (Önerilen)

1. Proje klasörünü açın
2. **`BASLA.bat`** dosyasına çift tıklayın
3. İlk seferde bağımlılıklar yüklenecek (2-5 dakika)
4. Tarayıcınızda otomatik açılacak

### 📝 Manuel Yöntem

Terminal açın ve şu komutları çalıştırın:

```bash
cd C:\MuhendislikAsistani
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

---

## PDF Manuel Yükleme ve Training

Training olmadan sadece arıza kodları çalışır. Dokümanlardan bilgi çekmek için training gereklidir.

### 1️⃣ PDF'leri Hazırlayın

Jeneratör manuellerinizi (kullanım kılavuzu, bakım manueli vb.) bilgisayarda bulun.

**Desteklenen Format:** PDF

### 2️⃣ Web Arayüzünde Training Sayfasına Gidin

1. Sol menüden **📚 Training** seçin
2. **"PDF dosyalarınızı seçin"** butonuna tıklayın
3. Manuellerinizi seçin (birden fazla seçilebilir)
4. **💾 PDF'leri Kaydet** butonuna tıklayın

![Training Sayfası Örneği]

### 3️⃣ Training'i Başlatın

1. **🚀 Training'i Başlat** butonuna tıklayın
2. İşlem 2-10 dakika sürebilir (PDF sayısına göre)
3. **Sayfayı kapatmayın!**

**Tamamlandığında:**
```
🎉 Training Başarılı!
- X PDF işlendi
- Y chunk oluşturuldu
```

---

## Sistemin Kullanımı

### 🏠 Ana Sayfa

Sistem durumunu gösterir:
- ✅ Ollama çalışıyor mu?
- ✅ Training yapıldı mı?
- 📄 Kaç PDF yüklü?

### 💬 Sorgulama (Chat)

**Training sonrası** kullanılabilir.

1. Sol menüden **💬 Sorgulama** seçin
2. Alttaki metin kutusuna sorunuzu yazın
3. Enter'a basın

**Örnek Sorular:**
- "500 saatlik bakımda hangi filtreler değişir?"
- "Yağ seviyesi nasıl kontrol edilir?"
- "Radyatör soğutma suyu ne sıklıkla değiştirilmeli?"
- "Rulman kontrolü nasıl yapılır?"

AI asistan, yüklediğiniz PDF'lerden bilgi çekerek cevap verecek.

### 🔍 Arıza Kodları

Training **gerekmez**. Hemen kullanılabilir.

**3 sekme:**

#### 1. Kod Ara
- Arıza kodunu yazın (örn: `E101`)
- **Ara** butonuna tıklayın
- Detaylı bilgi görülür:
  - Belirtiler
  - Nedenler
  - Çözüm adımları
  - Bakım periyodu

#### 2. Belirti Ara
- Belirti yazın (örn: `titreşim`, `duman`, `voltaj`)
- İlgili tüm arıza kodları listelenir

#### 3. Tüm Kodlar
- 15 arıza kodunun hepsini gösterir
- Kategoriye göre filtrelenebilir

### ⚙️ Ayarlar

- **Vektör DB'yi Temizle**: Training'i sıfırlar
- **PDF'leri Sil**: Yüklü manuelleri siler
- **Sistem Bilgisi**: Durum özeti

---

## Sorun Giderme

### ❌ "Ollama bulunamadı" Hatası

**Çözüm:**
1. Ollama kurulu mu kontrol edin: `ollama --version`
2. Değilse: [Ollama İndirin](https://ollama.ai/download)
3. Model çekin: `ollama pull mistral`

### ❌ "Training Gerekli" Uyarısı

**Çözüm:**
PDF yükleyip training yapın (yukarıdaki adımlar).

### ❌ "Python bulunamadı" Hatası

**Çözüm:**
1. Python kurulu mu kontrol edin: `python --version`
2. PATH'e eklenmiş mi kontrol edin
3. Yeniden kurun ve "Add to PATH" seçeneğini işaretleyin

### ❌ Web Sayfası Açılmıyor

**Çözüm:**
1. Terminal çıktısında hata var mı bakın
2. Manuel olarak açın: http://localhost:8501
3. Port meşgulse farklı port kullanın:
   ```bash
   streamlit run app.py --server.port 8502
   ```

### ❌ "ModuleNotFoundError" Hatası

**Çözüm:**
Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

### ❌ PDF İşlenemedi

**Çözüm:**
1. PDF'in bozuk olmadığından emin olun
2. PDF'i başka bir programda açıp tekrar kaydedin
3. OCR'lanmış (taranan) PDF ise önce metne dönüştürün

### ❌ Cevaplar Yanlış/Eksik

**Sebep:**
- PDF'ler yeterli bilgi içermeyebilir
- PDF kalitesi düşük olabilir

**Çözüm:**
- Daha detaylı/kaliteli manueller ekleyin
- Training'i tekrarlayın

---

## 💡 İpuçları

1. **İlk kez kullanıyorsanız:**
   - Önce arıza kodlarını test edin (training gerektirmez)
   - Sonra 1-2 PDF ile training yapın
   - Başarılı olduktan sonra diğer PDF'leri ekleyin

2. **Performans:**
   - Çok büyük PDF'ler (>100 sayfa) yavaşlatabilir
   - Gerekirse bölüm bölüm ayırın

3. **PDF Kalitesi:**
   - Metin bazlı PDF'ler tercih edilir
   - Taranan (scanned) PDF'ler OCR gerektirir

4. **Soru Sorma:**
   - Spesifik sorular sorun
   - Örnek: "Bakım" yerine "500 saatlik bakımda neler yapılır?"

5. **Güvenlik:**
   - PDF'ler `dokumanlar/manueller/` klasöründe
   - GitHub'a yüklenmez (hassas bilgi korunur)

---

## 📞 Destek

Sorun yaşarsanız:
1. Bu kılavuzu kontrol edin
2. Hata mesajını not alın
3. Terminal çıktısını kaydedin

---

## 🎯 Özet Kullanım Akışı

```
1. BASLA.bat çalıştır
   ↓
2. Tarayıcıda açıldı
   ↓
3. 📚 Training → PDF Yükle → Training Başlat
   ↓
4. ✅ Training tamamlandı
   ↓
5. 💬 Sorgulama → Soru sor → Cevap al
   veya
   🔍 Arıza Kodları → Kod/Belirti ara
```

---

**Başarılar! 🚀**
