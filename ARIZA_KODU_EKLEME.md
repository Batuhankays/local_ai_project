# 🔧 Arıza Kodu Ekleme ve Kullanım Kılavuzu

## ✅ Sistem Hazır - Arıza Kodları Temizlendi

Artık PDF'lerinizdeki arıza kodlarını sisteme ekleyebilirsiniz.

---

## 📝 Manuel Ekleme (Hızlı Başlangıç)

### 1. PDF'yi İnceleyin

Jeneratör manuelinizde arıza kodları bölümünü bulun.

**Örnek (PDF'den):**
```
Arıza Kodu: E-101
İsim: Yağ Basıncı Düşük
Çözüm:
1. Motoru durdurun
2. Yağ seviyesini kontrol edin
...
```

### 2. JSON'a Ekleyin

`dokumanlar/ariza_kodlari.json` dosyasını açın ve `fault_codes` array'ine ekleyin:

```json
{
  "code": "E-101",
  "generator_ids": ["caterpillar_3406"],
  "name": "Yağ Basıncı Düşük",
  "severity": "CRITICAL",
  "category": "Yağlama Sistemi",
  "symptoms": [
    "Kırmızı uyarı lambası",
    "Motor durabilir"
  ],
  "causes": [
    "Yağ seviyesi düşük",
    "Yağ pompası arızası"
  ],
  "solutions": [
    "1. Motoru durdurun",
    "2. Yağ seviyesini kontrol edin",
    "3. Gerekirse yağ ekleyin"
  ],
  "maintenance_interval_hours": 500,
  "priority": 1
}
```

### 3. Web Arayüzünde Görüntüleyin

1. Web arayüzünü yenileyin
2. **🔍 Arıza Kodları** → Jeneratör seçin
3. Eklediğiniz kodlar listelenir

---

## 🤖 AI ile Yarı-Otomatik Ekleme

### Kullanım (Web Arayüzünde)

Henüz geliştirilmedi. Şu an manuel ekleme öneriliyor.

**Planlanan Özellik:**
- PDF yükle
- "Arıza Kodlarını Çıkar" tıkla  
- AI analiz edip önizleme gösterir
- Onaylarsınız, sisteme eklenir

---

## 📋 Alan Açıklamaları

| Alan | Açıklama | Örnek |
|------|----------|-------|
| `code` | Arıza kodu (benzersiz) | `"E-101"`, `"CAT-500"` |
| `generator_ids` | Hangi jeneratörler için | `["caterpillar_3406"]` |
| `name` | Arıza adı | `"Yağ Basıncı Düşük"` |
| `severity` | Önem: CRITICAL, HIGH, MEDIUM | `"CRITICAL"` |
| `category` | Kategori | `"Yağlama Sistemi"` |
| `symptoms` | Belirtiler (array) | `["Kırmızı lamba", ...]` |
| `causes` | Nedenler (array) | `["Yağ az", ...]` |
| `solutions` | Çözümler (array) | `["1. Dur", "2. Kontrol et"]` |
| `maintenance_interval_hours` | Bakım periyodu | `500` |
| `priority` | Öncelik (1-5) | `1` |

---

## 🎯 Öncelik Kuralları

- **CRITICAL + priority:1** → Acil, anında müdahale
- **HIGH + priority:2** → Önemli, kısa sürede çöz
- **MEDIUM + priority:3** → Normal bakım

---

## 💡 İpuçları

**1. Kod Formatı:**
- Jeneratöre özgü: `CAT-101`, `CUM-201`
- Genel: `E-101`, `W-202`

**2. Kategori Önerileri:**
- Yağlama Sistemi
- Soğutma Sistemi
- Yakıt Sistemi
- Elektrik Sistemi
- Mekanik
- Jeneratör
- Egzoz Sistemi
- Kontrol Sistemi

**3. Çözümler:**
- Numaralı liste kullanın (1., 2., 3...)
- Adım adım yazın
- Güvenlik uyarılarını ekleyin

---

## 🚀 Hızlı Örnek

**Senaryo:** PDF'de "Low Oil Pressure - Code E-LP01" gördünüz

**JSON:**
```json
{
  "code": "E-LP01",
  "generator_ids": ["caterpillar_3406"],
  "name": "Düşük Yağ Basıncı",
  "severity": "CRITICAL",
  "category": "Yağlama Sistemi",
  "symptoms": ["Kırmızı uyarı", "Motor titreşimi"],
  "causes": ["Yağ seviyesi düşük", "Pompa arızası"],
  "solutions": [
    "1. Motoru hemen durdurun",
    "2. Yağ seviyesini kontrol edin",
    "3. Gerekirse DELO 10W-40 ekleyin"
  ],
  "maintenance_interval_hours": 500,
  "priority": 1
}
```

**Ekledikten sonra:**
- Web'de "Caterpillar 3406" seçin
- Arıza kodu gösterilir
- Sorgulama yaparken AI kullanabilir

---

## ⚠️ Önemli Notlar  

1. **Benzersiz kod:** Her kod bir kez tanımlanmalı
2. **generator_ids boş olamaz:** En az bir jeneratör ID'si gerekli
3. **JSON formatı:** Virgül, tırnak işaretlerine dikkat edin
4. **Test edin:** Ekledikten sonra web arayüzünde kontrol edin

---

**İyi çalışmalar! 🎉**
