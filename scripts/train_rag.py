"""
RAG Sistemi Training Script

PDF manuellerini işler, embedding oluşturur ve vektör veritabanına kaydeder.
Kullanıcı PDF'leri dokumanlar/manueller/ klasörüne ekledikten sonra çalıştırır.
"""

import os
import sys
from dotenv import load_dotenv

# Proje kök dizinini Python path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.document_processor import DocumentProcessor
from src.rag_engine import RAGEngine


def main():
    """Ana training fonksiyonu"""
    
    # .env dosyasını yükle
    load_dotenv()
    
    # Konfigürasyon
    MANUALS_FOLDER = os.getenv('MANUALS_FOLDER', 'dokumanlar/manueller')
    VECTOR_DB_PATH = os.getenv('VECTOR_DB_PATH', './data/vector_store/vectordb.pkl')
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', '800'))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', '200'))
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
    
    print("=" * 70)
    print("🚀 RAG Sistemi Training")
    print("=" * 70)
    print(f"\n📂 Manüeller klasörü: {MANUALS_FOLDER}")
    print(f"💾 Vektör DB yolu: {VECTOR_DB_PATH}")
    print(f"📏 Chunk boyutu: {CHUNK_SIZE} karakter")
    print(f"🔄 Overlap: {CHUNK_OVERLAP} karakter")
    print(f"🤖 Embedding model: {EMBEDDING_MODEL}\n")
    print("=" * 70 + "\n")
    
    # 1. PDF'leri kontrol et
    if not os.path.exists(MANUALS_FOLDER):
        print(f"❌ Manüeller klasörü bulunamadı: {MANUALS_FOLDER}")
        print(f"\nLütfen önce PDF manuellerinizi '{MANUALS_FOLDER}' klasörüne ekleyin.")
        return
    
    pdf_count = len([f for f in os.listdir(MANUALS_FOLDER) if f.endswith('.pdf')])
    
    if pdf_count == 0:
        print(f"⚠️  '{MANUALS_FOLDER}' klasöründe PDF bulunamadı!")
        print(f"\nLütfen PDF manuellerinizi bu klasöre ekleyin ve tekrar çalıştırın.")
        print(f"\nÖrnek:")
        print(f"  copy jenerator_manual.pdf {MANUALS_FOLDER}/")
        return
    
    print(f"✓ {pdf_count} PDF dosyası bulundu\n")
    
    # 2. Doküman işleyicisi oluştur
    print("📄 PDF'ler işleniyor...\n")
    processor = DocumentProcessor(chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
    
    try:
        chunks = processor.process_all_pdfs(MANUALS_FOLDER)
    except Exception as e:
        print(f"\n❌ PDF işleme hatası: {str(e)}")
        return
    
    if not chunks:
        print("\n❌ Hiç chunk oluşturulamadı!")
        return
    
    # 3. RAG engine oluştur ve embedding yap
    print("\n" + "=" * 70)
    print("🧠 RAG Engine başlatılıyor...\n")
    
    try:
        rag = RAGEngine(embedding_model=EMBEDDING_MODEL, llm_model="mistral")
    except Exception as e:
        print(f"\n❌ RAG engine hatası: {str(e)}")
        return
    
    print("\n" + "=" * 70)
    print("🔄 Dokümanlar vektör veritabanına ekleniyor...\n")
    
    try:
        rag.add_documents(chunks)
    except Exception as e:
        print(f"\n❌ Embedding oluşturma hatası: {str(e)}")
        return
    
    # 4. Vektör DB'yi kaydet
    print("\n" + "=" * 70)
    print("💾 Vektör veritabanı kaydediliyor...\n")
    
    try:
        rag.save_vector_db(VECTOR_DB_PATH)
    except Exception as e:
        print(f"\n❌ Kaydetme hatası: {str(e)}")
        return
    
    # 5. Özet bilgi
    print("\n" + "=" * 70)
    print("✅ TRAINING TAMAMLANDI!")
    print("=" * 70)
    print(f"\n📊 Özet:")
    print(f"   • {pdf_count} PDF işlendi")
    print(f"   • {len(chunks)} chunk oluşturuldu")
    print(f"   • Vektör DB kaydedildi: {VECTOR_DB_PATH}")
    print(f"\n🎯 Sistem kullanıma hazır!")
    print(f"\nTest etmek için:")
    print(f'   python main.py query "Yağ değişimi nasıl yapılır?"')
    print(f'   python main.py fault E101')
    print(f'   python main.py interactive')
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Training iptal edildi")
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {str(e)}")
        import traceback
        traceback.print_exc()
