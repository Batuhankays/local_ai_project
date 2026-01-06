"""
PDF Doküman İşleme Modülü

Bu modül PDF dosyalarını okur, metinleri çıkarır,
overlap'li chunk'lara böler ve RAG sistemi için hazırlar.
"""

import os
from typing import List, Dict
import PyPDF2
from pathlib import Path


class PDFReader:
    """PDF dosyalarını oku ve metin çıkar"""
    
    @staticmethod
    def extract_text(pdf_path: str) -> str:
        """
        PDF'den metin çıkar
        
        Args:
            pdf_path: PDF dosya yolu
        
        Returns:
            Çıkarılan metin
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF bulunamadı: {pdf_path}")
        
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
        
        except Exception as e:
            print(f"❌ PDF okuma hatası: {pdf_path}")
            print(f"   Hata: {str(e)}")
            return ""
        
        return text.strip()


class TextChunker:
    """Metni overlap'li parçalara böl"""
    
    def __init__(self, chunk_size: int = 800, overlap: int = 200):
        """
        Args:
            chunk_size: Her parçanın karakter sayısı
            overlap: Parçalar arası örtüşme miktarı
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str, source: str = "") -> List[Dict[str, str]]:
        """
        Metni chunk'lara böl
        
        Args:
            text: Bölünecek metin
            source: Kaynak dosya adı (metadata için)
        
        Returns:
            Chunk listesi, her biri {'text': ..., 'source': ..., 'chunk_id': ...}
        """
        if not text or len(text.strip()) == 0:
            return []
        
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(text):
            # Chunk sonunu bul
            end = start + self.chunk_size
            
            # Son chunk mu?
            if end >= len(text):
                chunk_text = text[start:].strip()
                if chunk_text:
                    chunks.append({
                        'text': chunk_text,
                        'source': source,
                        'chunk_id': chunk_id,
                        'start_char': start,
                        'end_char': len(text)
                    })
                break
            
            # Cümle sınırında kes (nokta, soru işareti, ünlem)
            # Son 100 karakterde ara
            search_start = max(start + self.chunk_size - 100, start)
            sentence_end = -1
            
            for i in range(end, search_start, -1):
                if i < len(text) and text[i] in '.!?\n':
                    sentence_end = i + 1
                    break
            
            if sentence_end != -1:
                end = sentence_end
            
            # Chunk'ı ekle
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append({
                    'text': chunk_text,
                    'source': source,
                    'chunk_id': chunk_id,
                    'start_char': start,
                    'end_char': end
                })
            
            # Sonraki chunk'a geç (overlap ile)
            start = end - self.overlap
            chunk_id += 1
        
        return chunks


class DocumentProcessor:
    """PDF dokümanları işle ve chunk'la"""
    
    def __init__(self, chunk_size: int = 800, overlap: int = 200):
        """
        Args:
            chunk_size: Chunk boyutu (karakter)
            overlap: Overlap miktarı (karakter)
        """
        self.pdf_reader = PDFReader()
        self.text_chunker = TextChunker(chunk_size=chunk_size, overlap=overlap)
    
    def process_pdf(self, pdf_path: str) -> List[Dict[str, str]]:
        """
        Bir PDF'i işle ve chunk'lara böl
        
        Args:
            pdf_path: PDF dosya yolu
        
        Returns:
            Chunk listesi
        """
        print(f"📄 İşleniyor: {os.path.basename(pdf_path)}")
        
        # Metni çıkar
        text = self.pdf_reader.extract_text(pdf_path)
        
        if not text:
            print(f"   ⚠️  Metin çıkarılamadı")
            return []
        
        # Chunk'lara böl
        chunks = self.text_chunker.chunk_text(
            text=text,
            source=os.path.basename(pdf_path)
        )
        
        print(f"   ✓ {len(chunks)} chunk oluşturuldu ({len(text)} karakter)")
        return chunks
    
    def process_all_pdfs(self, folder_path: str) -> List[Dict[str, str]]:
        """
        Bir klasördeki tüm PDF'leri işle
        
        Args:
            folder_path: Klasör yolu
        
        Returns:
            Tüm chunk'ların listesi
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Klasör bulunamadı: {folder_path}")
        
        all_chunks = []
        pdf_files = list(Path(folder_path).rglob("*.pdf"))
        
        if not pdf_files:
            print(f"⚠️  {folder_path} klasöründe PDF bulunamadı")
            return []
        
        print(f"\n📂 {len(pdf_files)} PDF bulundu\n")
        
        for pdf_path in pdf_files:
            chunks = self.process_pdf(str(pdf_path))
            all_chunks.extend(chunks)
        
        print(f"\n✓ Toplam {len(all_chunks)} chunk oluşturuldu")
        return all_chunks


if __name__ == "__main__":
    # Test
    processor = DocumentProcessor(chunk_size=500, overlap=100)
    
    # Test metni
    test_text = """
    Jeneratör Bakım Klavuzu
    
    1. Yağ Kontrolü
    Motor yağ seviyesi her çalıştırmadan önce kontrol edilmelidir.
    Yağ ölçüm çubuğunu çıkarın, temizleyin ve tekrar takın.
    Seviye MIN ve MAX işaretleri arasında olmalıdır.
    
    2. Soğutma Suyu
    Radyatör kapağını asla sıcak motorda açmayın.
    Soğutma suyu seviyesi rezervuar işaretlerinde olmalıdır.
    Antifriz oranı %50 olmalıdır.
    """ * 5  # Daha uzun bir test metni için
    
    chunks = processor.text_chunker.chunk_text(test_text, "test_manual.pdf")
    
    print(f"\nTest metni {len(test_text)} karakter")
    print(f"{len(chunks)} chunk oluşturuldu\n")
    
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i}: {len(chunk['text'])} karakter")
        print(f"  Başlangıç: {chunk['text'][:50]}...")
