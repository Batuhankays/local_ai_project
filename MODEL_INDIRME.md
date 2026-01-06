# 🎯 Hemen Yapılacaklar - Model İndirme

## Llama3.1:8b Modeli İndirme

### Terminal/CMD Açın ve Çalıştırın:

```bash
ollama pull llama3.1:8b
```

**Süre:** 2-3 dakika (4.7GB ind model)

**İndirme Başladığında:**
```
pulling manifest
pulling model... ██████████ 100%
```

### İndirme Tamamlandıktan Sonra:

1. **Web arayüzünü yenileyin** (F5)
   - Veya BASLA.bat'ı kapatıp tekrar açın

2. **Bir soru sorun** (PDF yüklediyseniz):
   ```
   "Jeneratörde yağ basıncı düşük. Ne yapmalıyım?"
   ```

3. **Yeni format göreceksiniz:**
   ```
   📋 ÖZET:
   ...

   🔧 ADIMLAR:
   1. ...
   2. ...

   ⚠️ GÜVENLİK:
   ...

   📚 KAYNAK:
   ...
   ```

---

## Farklar (Mistral vs Llama3.1)

### ÖNCE (Mistral):
```
jeneratörde yağ basıncı düşükse birkaç neden olabillir...
[yazım hataları, genel cevap]
```

### SONRA (Llama3.1:8b):
```
📋 ÖZET:
Yağ seviyesini kontrol edip gerekirse ekleyin, filtre değiştirin.

🔧 ADIMLAR:
1. Motoru durdurun ve soğumasını bekleyin
2. Yağ ölçüm çubuğu ile seviyeyi kontrol edin
...
```

---

## Sorun Yaşarsanız

**"Model not found" hatası:**
```bash
ollama list
# llama3.1 görünmüyorsa
ollama pull llama3.1:8b
```

**Streamlit hataları:**
- Web arayüzünü kapatıp BASLA.bat'ı tekrar çalıştırın

---

**Model indirmeyi başlatın!** 🚀
