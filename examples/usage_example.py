"""
Kullanım Örnekleri

Bu script, mühendislik asistanının temel kullanımını gösterir.
"""

import sys
import os

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fault_code_manager import FaultCodeManager
from src.document_processor import DocumentProcessor
from src.assistant import EngineeringAssistant


def example_1_fault_code_search():
    """Örnek 1: Arıza kodu arama"""
    print("=" * 70)
    print("ÖRNEK 1: Arıza Kodu Arama")
    print("=" * 70 + "\n")
    
    manager = FaultCodeManager()
    
    # Specific kod arama
    print("1. E101 kodunu ara:\n")
    fault = manager.search_by_code("E101")
    print(manager.format_fault_info(fault))
    
    print("\n" + "-" * 70 + "\n")
    
    # Belirti ile arama
    print("2. 'titreşim' belirtisine göre ara:\n")
    results = manager.search_by_symptom("titreşim")
    for fault in results:
        print(f"  • {fault['code']}: {fault['name']} ({fault['severity']})")
    
    print("\n" + "-" * 70 + "\n")
    
    # Kritik arızalar
    print("3. Kritik arıza kodları:\n")
    critical = manager.get_critical_faults()
    for fault in critical:
        print(f"  • {fault['code']}: {fault['name']}")


def example_2_document_processing():
    """Örnek 2: PDF işleme (test metni ile)"""
    print("\n" + "=" * 70)
    print("ÖRNEK 2: Doküman İşleme")
    print("=" * 70 + "\n")
    
    processor = DocumentProcessor(chunk_size=500, overlap=100)
    
    # Test metni oluştur
    test_text = """
    Jeneratör Bakım Kılavuzu
    
    1. Günlük Kontroller
    - Yağ seviyesi kontrolü
    - Soğutma suyu kontrolü
    - Yakıt seviyesi kontrolü
    - Görsel kontrol (sızıntı, gevşek bağlantılar)
    
    2. Haftalık Kontroller
    - Akü voltajı kontrolü (12.6V olmalı)
    - Hava filtresi kontrolü
    - Kayış gerginlik kontrolü
    
    3. 500 Saatlik Bakım
    - Motor yağ değişimi (10W-40 mineral yağ, 8-10 litre)
    - Yağ filtresi değişimi
    - Yakıt filtresi değişimi
    - Hava filtresi değişimi
    
    4. 1000 Saatlik Bakım
    - Soğutma suyu değişimi (50% antifriz)
    - Supap ayarı (0.15mm giriş, 0.30mm egzoz)
    - Enjektör kontrolü
    - Türboşarj kontrolü
    """ * 3  # Daha uzun metin için
    
    # Chunk'lara böl
    chunks = processor.text_chunker.chunk_text(test_text, "bakim_klavuzu.pdf")
    
    print(f"📄 Test metni: {len(test_text)} karakter")
    print(f"✓ {len(chunks)} chunk oluşturuldu\n")
    
    # İlk 2 chunk'ı göster
    for i, chunk in enumerate(chunks[:2], 1):
        print(f"Chunk {i} (kaynak: {chunk['source']}):")
        print(f"  Uzunluk: {len(chunk['text'])} karakter")
        print(f"  İçerik: {chunk['text'][:100]}...")
        print()


def example_3_assistant_usage():
    """Örnek 3: Asistan kullanımı"""
    print("\n" + "=" * 70)
    print("ÖRNEK 3: Mühendislik Asistanı Kullanımı")
    print("=" * 70 + "\n")
    
    try:
        assistant = EngineeringAssistant()
        
        # Arıza kodu analizi
        print("1. Arıza Kodu Analizi:\n")
        result = assistant.analyze_fault("E101")
        print(result)
        
        print("\n" + "-" * 70 + "\n")
        
        # Belirti arama
        print("2. Belirti Arama:\n")
        result = assistant.search_faults_by_symptom("voltaj")
        print(result)
        
        print("\n" + "-" * 70 + "\n")
        
        # Kritik kodlar
        print("3. Kritik Arıza Kodları:\n")
        result = assistant.get_critical_faults()
        print(result)
        
        # RAG sorgusu (sadece vektör DB varsa çalışır)
        # print("\n" + "-" * 70 + "\n")
        # print("4. RAG Sorgusu:\n")
        # answer = assistant.query("500 saatlik bakımda neler yapılır?")
        # print(f"Cevap:\n{answer}")
    
    except Exception as e:
        print(f"⚠️  Asistan hatası: {str(e)}")
        print("\nNot: RAG sorguları için önce 'python scripts/train_rag.py' çalıştırın")


def example_4_workflow():
    """Örnek 4: Tipik kullanım senaryosu"""
    print("\n" + "=" * 70)
    print("ÖRNEK 4: Tipik Kullanım Senaryosu")
    print("=" * 70 + "\n")
    
    print("Senaryo: Operatör jeneratörde anormal titreşim farketti\n")
    
    manager = FaultCodeManager()
    
    # 1. Belirti ile ara
    print("1️⃣  'titreşim' belirtisine göre arama:")
    results = manager.search_by_symptom("titreşim")
    
    if results:
        print(f"   ✓ {len(results)} olası arıza bulundu:\n")
        for fault in results[:3]:  # İlk 3'ünü göster
            print(f"   • {fault['code']}: {fault['name']}")
            print(f"     Kategori: {fault['category']}")
            print(f"     Önem: {fault['severity']}\n")
    
    # 2. En olası arızanın detayını göster
    if results:
        print("\n2️⃣  En olası arıza (E401 - Aşırı Titreşim) detayları:\n")
        fault = manager.search_by_code("E401")
        
        print(f"   Belirtiler:")
        for symptom in fault['symptoms'][:3]:
            print(f"     • {symptom}")
        
        print(f"\n   İlk 3 Çözüm Adımı:")
        for i, solution in enumerate(fault['solutions'][:3], 1):
            print(f"     {i}. {solution}")
        
        print(f"\n   ⚠️  Önem Seviyesi: {fault['severity']}")
        print(f"   🔧 Bakım Periyodu: {fault['maintenance_interval_hours']} saat")


if __name__ == "__main__":
    print("\n")
    print("🚀 MÜHENDİSLİK ASİSTANI - KULLANIM ÖRNEKLERİ")
    print("=" * 70 + "\n")
    
    # Örnekleri çalıştır
    example_1_fault_code_search()
    example_2_document_processing()
    example_3_assistant_usage()
    example_4_workflow()
    
    print("\n" + "=" * 70)
    print("✅ Örnekler tamamlandı!")
    print("=" * 70)
    print("\n💡 İpucu:")
    print("   - PDF'lerinizi 'dokumanlar/manueller/' klasörüne ekleyin")
    print("   - 'python scripts/train_rag.py' ile training yapın")
    print("   - 'python main.py interactive' ile interaktif mod başlatın")
    print("\n")
