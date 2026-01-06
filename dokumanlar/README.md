# Dokümanlar Klasörü

Bu klasör, mühendislik asistanının kullanacağı tüm teknik dokümanları içerir.

## 📁 İçerik

### `ariza_kodlari.json`
Askeri jeneratör arıza kodları veritabanı. Bu dosya GitHub'a yüklenebilir (hassas bilgi içermez).

**İçeriği:**
- 15 yaygın jeneratör arıza kodu
- Her kod için: belirtiler, nedenler, çözüm adımları
- Bakım periyotları
- Öncelik seviyeleri

### `manueller/` klasörü
**Hassas PDF manuellerinizi bu klasöre ekleyin.**

⚠️ **Önemli Güvenlik Notu:**
- Bu klasördeki PDF dosyaları `.gitignore` ile korunur
- GitHub'a asla yüklenmez
- Her yeni ortamda (deployment, yeni makine) manuel olarak kopyalamanız gerekir

**Desteklenen formatlar:**
- PDF (`.pdf`)
- Text (`.txt`)
- Word dokümanları (`.docx`) - gelecekte desteklenecek

## 🚀 Kullanım

### 1. Manuel Ekleme

```bash
# PDF'lerinizi kopyalayın:
copy jenerator_manual.pdf dokumanlar/manueller/
copy bakim_klavuzu.pdf dokumanlar/manueller/
```

### 2. RAG Sistemini Eğitme

Manuellerinizi ekledikten sonra:

```bash
python scripts/train_rag.py
```

Bu komut:
- `manueller/` klasöründeki tüm PDF'leri tarar
- Metinleri çıkarır ve parçalara böler
- Embedding oluşturur
- Vektör veritabanına kaydeder

### 3. Sorgulama

```bash
python main.py query "Yağ değişim aralığı nedir?"
```

Asistan, eklediğiniz PDF'lerden ilgili bilgiyi bulup cevap verecektir.

## 📋 Örnek Klasör Yapısı

```
dokumanlar/
├── ariza_kodlari.json          # Arıza kodları DB (GitHub'da)
├── README.md                    # Bu dosya
└── manueller/                   # Hassas PDF'ler (GitHub'da DEĞİL)
    ├── .gitkeep
    ├── jenerator_teknik_manual.pdf
    ├── bakim_planlama.pdf
    ├── parca_katalog.pdf
    └── elektrik_semasi.pdf
```

## 🔒 Güvenlik

`.gitignore` kuralı:
```
dokumanlar/manueller/**/*.pdf
dokumanlar/manueller/**/*.txt
dokumanlar/manueller/**/*.docx
```

Bu, `manueller/` klasöründeki tüm hassas dokümanları korur.

## 💡 İpuçları

1. **Net isimlendirme**: PDF'lere açıklayıcı isimler verin
   - ✅ `M250_jenerator_kullanim_klavuzu.pdf`
   - ❌ `dokuman1.pdf`

2. **Organize etme**: Alt klasörler kullanabilirsiniz
   ```
   manueller/
   ├── kullanim_klavuzlari/
   ├── bakim_manuelleri/
   └── parca_kataloglari/
   ```

3. **Güncel tutma**: Eski manuelleri silip yenilerini ekleyin, sonra tekrar train edin

4. **Test etme**: Her yeni manuel ekledikten sonra basit bir sorgu ile test edin
