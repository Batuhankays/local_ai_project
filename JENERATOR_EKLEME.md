# Jeneratör Ekleme Kılavuzu

## 🏭 Yeni Jeneratör Nasıl Eklenir?

### Adım 1: JSON Dosyasını Açın

`dokumanlar/ariza_kodlari.json` dosyasını text editör ile açın.

### Adım 2: Generators Bölümüne Ekleyin

```json
"generators": [
  {
    "id": "general",
    "manufacturer": "Genel",
    "model": "Tüm Modeller",
    "power_kva": null,
    "description": "Tüm jeneratörler için geçerli genel arıza kodları",
    "notes": "Bu kodlar çoğu dizel jeneratörde ortak"
  },
  {
    "id": "caterpillar_3406",
    "manufacturer": "Caterpillar",
    "model": "3406",
    "power_kva": 500,
    "description": "Caterpillar 3406 Dizel Jeneratör - 500 kVA",
    "notes": "Askeri kamplarda kullanılan ana jeneratör"
  },
  {
    "id": "cummins_qsx15",
    "manufacturer": "Cummins",
    "model": "QSX15",
    "power_kva": 600,
    "description": "Cummins QSX15 Dizel Jeneratör - 600 kVA",
    "notes": "Yüksek güç gerektiren uygulamalar için"
  }
],
```

### Adım 3: Arıza Kodlarını İlişkilendirin

Her arıza koduna `generator_ids` ekleyin:

```json
{
  "code": "E101",
  "generator_ids": ["general", "caterpillar_3406", "cummins_qsx15"],
  "name": "Düşük Yağ Basıncı",
  ...
}
```

veya sadece bir jeneratöre özel:

```json
{
  "code": "CAT-401",
  "generator_ids": ["caterpillar_3406"],
  "name": "Turboşarj Basınç Düşüklüğü (Caterpillar Spesifik)",
  ...
}
```

### Adım 4: Web Arayüzünde Test Edin

1. Web arayüzünü yenileyin
2. **🔍 Arıza Kodları** sekmesine gidin
3. **🏭 Jeneratör Seçimi** dropdown'ında yeni jeneratörlerinizi göreceksiniz
4. Bir jeneratör seçin → Sadece o jeneratöre ait kodlar gösterilir

---

## 📝 Örnek Kullanım

### Senaryo 1: Genel Kod (Tüm Jeneratörler)

```json
{
  "code": "E101",
  "generator_ids": ["general"],
  "name": "Düşük Yağ Basıncı"
}
```
→ "Genel - Tüm Modeller" seçildiğinde görünür

### Senaryo 2: Çok Jeneratörlü Kod

```json
{
  "code": "E201",
  "generator_ids": ["caterpillar_3406", "cummins_qsx15"],
  "name": "Yakıt Filtresi Tıkanması"
}
```
→ Hem Caterpillar hem Cummins seçildiğinde görünür

### Senaryo 3: Jeneratör-Spesifik Kod

```json
{
  "code": "CAT-999",
  "generator_ids": ["caterpillar_3406"],
  "name": "CAT Engine ECM Arızası"
}
```
→ Sadece Caterpillar 3406 seçildiğinde görünür

---

## ✅ Hızlı Başlangıç

**Minimum 3 jeneratör öneririz:**
1. `general` (mevcut)
2. Sizin ana jeneratörünüz (örn: Caterpillar)
3. Yedek jeneratörünüz (örn: Cummins)

**Web arayüzünden kullanım:**
- Dropdown'dan jeneratör seçin
- Arıza kodları otomatik filtrelenir
- Jeneratör bilgileri (üretici, model, güç) gösterilir

🎉 **Artık sistem çok jeneratörlü!**
