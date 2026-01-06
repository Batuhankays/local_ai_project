"""
RAG (Retrieval-Augmented Generation) Motoru

Bu modül, vektör veritabanı kullanarak doküman chunk'larını saklar,
sorgu embedding'i oluşturur, en yakın chunk'ları bulur ve
Ollama ile cevap üretir.
"""

import os
import pickle
from typing import List, Dict, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
import ollama


class Embedder:
    """Metin embedding oluşturma"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Args:
            model_name: Sentence-transformers model adı
        """
        print(f"🤖 Embedding modeli yükleniyor: {model_name}")
        self.model = SentenceTransformer(model_name)
        print("   ✓ Model yüklendi")
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """
        Metinleri embedding'e çevir
        
        Args:
            texts: Metin listesi
        
        Returns:
            Embedding matrisi (n_texts x embedding_dim)
        """
        return self.model.encode(texts, show_progress_bar=True)
    
    def encode_single(self, text: str) -> np.ndarray:
        """Tek bir metni embedding'e çevir"""
        return self.model.encode([text])[0]


class VectorStore:
    """FAISS tabanlı vektör veritabanı (basitleştirilmiş)"""
    
    def __init__(self, embedding_dim: int = 384):
        """
        Args:
            embedding_dim: Embedding boyutu (all-MiniLM-L6-v2 için 384)
        """
        self.embedding_dim = embedding_dim
        self.embeddings = []
        self.chunks = []
        self.index_built = False
    
    def add_documents(self, chunks: List[Dict], embeddings: np.ndarray):
        """
        Dokümanları ve embedding'leri ekle
        
        Args:
            chunks: Chunk metadata listesi
            embeddings: Chunk embedding'leri
        """
        if len(chunks) != len(embeddings):
            raise ValueError("Chunk sayısı embedding sayısına eşit olmalı")
        
        self.chunks.extend(chunks)
        self.embeddings.append(embeddings)
        self.index_built = False
    
    def build_index(self):
        """Embedding matrisini oluştur"""
        if self.embeddings:
            self.embeddings = np.vstack(self.embeddings)
            self.index_built = True
            print(f"✓ Vektör indeksi oluşturuldu: {len(self.chunks)} chunk")
    
    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Dict]:
        """
        En yakın chunk'ları bul (cosine similarity)
        
        Args:
            query_embedding: Sorgu embedding'i
            top_k: Kaç sonuç döndürülecek
        
        Returns:
            En yakın chunk'lar
        """
        if not self.index_built:
            self.build_index()
        
        if len(self.chunks) == 0:
            return []
        
        # Cosine similarity hesapla
        query_norm = query_embedding / np.linalg.norm(query_embedding)
        embeddings_norm = self.embeddings / np.linalg.norm(
            self.embeddings, axis=1, keepdims=True
        )
        
        similarities = np.dot(embeddings_norm, query_norm)
        
        # En yüksek skorları al
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            result = self.chunks[idx].copy()
            result['similarity'] = float(similarities[idx])
            results.append(result)
        
        return results
    
    def save(self, path: str):
        """Vektör DB'yi kaydet"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        data = {
            'embeddings': self.embeddings,
            'chunks': self.chunks,
            'embedding_dim': self.embedding_dim
        }
        
        with open(path, 'wb') as f:
            pickle.dump(data, f)
        
        print(f"💾 Vektör DB kaydedildi: {path}")
    
    def load(self, path: str):
        """Vektör DB'yi yükle"""
        if not os.path.exists(path):
            raise FileNotFoundError(f"Vektör DB bulunamadı: {path}")
        
        with open(path, 'rb') as f:
            data = pickle.load(f)
        
        self.embeddings = data['embeddings']
        self.chunks = data['chunks']
        self.embedding_dim = data['embedding_dim']
        self.index_built = True
        
        print(f"✓ Vektör DB yüklendi: {len(self.chunks)} chunk")


class OllamaLLM:
    """Ollama LLM entegrasyonu"""
    
    def __init__(self, model: str = "llama3.1:8b", url: str = "http://localhost:11434"):
        """
        Args:
            model: Ollama model adı (llama3.1:8b önerilen)
            url: Ollama API URL
        """
        self.model = model
        self.url = url
        self._check_connection()
    
    def _check_connection(self):
        """Ollama bağlantısını kontrol et"""
        try:
            ollama.list()
            print(f"✓ Ollama bağlantısı başarılı (Model: {self.model})")
        except Exception as e:
            print(f"⚠️  Ollama bağlantı hatası: {e}")
            print("   Ollama'nın çalıştığından emin olun: ollama serve")
    
    def generate(
        self, 
        prompt: str, 
        system: str = "",
        temperature: float = 0.3,
        top_p: float = 0.9,
        max_tokens: int = 1024
    ) -> str:
        """
        Ollama ile cevap üret
        
        Args:
            prompt: Kullanıcı prompt'u
            system: Sistem prompt'u
            temperature: Yaratıcılık (0.0-1.0, düşük = daha deterministik)
            top_p: Nucleus sampling
            max_tokens: Maksimum token sayısı
        
        Returns:
            Üretilen cevap
        """
        try:
            messages = []
            
            if system:
                messages.append({
                    'role': 'system',
                    'content': system
                })
            
            messages.append({
                'role': 'user',
                'content': prompt
            })
            
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options={
                    'temperature': temperature,
                    'top_p': top_p,
                    'num_predict': max_tokens,
                }
            )
            
            return response['message']['content']
        
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg:
                return (f"Ollama hatası: model '{self.model}' not found (status code: 404)\n\n"
                       f"Model indirmek için terminalde çalıştırın:\n"
                       f"  ollama pull {self.model}\n\n"
                       f"Veya farklı bir model kullanın (mistral, gemma2:9b vb.)")
            return f"Ollama hatası: {str(e)}\n\nOllama'nın çalıştığından ve '{self.model}' modelinin yüklü olduğundan emin olun."


class RAGEngine:
    """RAG sistemi ana motoru"""
    
    def __init__(
        self,
        embedding_model: str = "all-MiniLM-L6-v2",
        llm_model: str = "mistral",
        vector_db_path: Optional[str] = None
    ):
        """
        Args:
            embedding_model: Sentence-transformers model
            llm_model: Ollama model
            vector_db_path: Vektör DB yolu (varsa yükle)
        """
        self.embedder = Embedder(model_name=embedding_model)
        self.vector_store = VectorStore(embedding_dim=384)
        self.llm = OllamaLLM(model=llm_model)
        
        # Vektör DB varsa yükle
        if vector_db_path and os.path.exists(vector_db_path):
            self.vector_store.load(vector_db_path)
    
    def add_documents(self, chunks: List[Dict]):
        """
        Dokümanları RAG sistemine ekle
        
        Args:
            chunks: Chunk listesi (document_processor'dan)
        """
        if not chunks:
            print("Eklenecek chunk yok")
            return
        
        print(f"\n🔄 {len(chunks)} chunk için embedding oluşturuluyor...")
        
        # Embedding oluştur
        texts = [chunk['text'] for chunk in chunks]
        embeddings = self.embedder.encode(texts)
        
        # Vektör DB'ye ekle
        self.vector_store.add_documents(chunks, embeddings)
        self.vector_store.build_index()
    
    def retrieve_context(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Sorguya en yakın doküman parçalarını getir
        
        Args:
            query: Kullanıcı sorusu
            top_k: Kaç chunk döndürülecek
        
        Returns:
            En yakın chunk'lar
        """
        # Query embedding oluştur
        query_embedding = self.embedder.encode_single(query)
        
        # Benzer chunk'ları bul
        results = self.vector_store.search(query_embedding, top_k=top_k)
        
        return results
    
    def generate_answer(
        self,
        query: str,
        context_chunks: Optional[List[Dict]] = None,
        fault_info: Optional[Dict] = None,
        top_k: int = 3
    ) -> str:
        """
        Sorguya cevap üret (RAG)
        
        Args:
            query: Kullanıcı sorusu
            context_chunks: Önceden alınmış context (yoksa otomatik al)
            fault_info: Arıza kodu bilgisi (varsa)
            top_k: Kaç chunk kullanılacak
        
        Returns:
            Üretilen cevap
        """
        # Context yoksa al
        if context_chunks is None:
            context_chunks = self.retrieve_context(query, top_k=top_k)
        
        # System prompt - Gelişmiş versiyon
        system_prompt = """Sen askeri jeneratör bakım ve arıza giderme konusunda uzman bir teknisyensin.

GÖREVİN:
1. Verilen teknik dokümanlara SADECE dayanarak cevap ver
2. Emin olmadığın konularda "Bu bilgi dokümanlarımda yok" de
3. Adım adım, net ve uygulanabilir çözümler sun
4. Güvenlik önlemleri varsa MUTLAKA belirt

CEVAP FORMATI:
- Kısa özet ile başla (1-2 cümle)
- Adım adım çözüm sun (numaralı liste)
- Güvenlik uyarısı varsa belirt
- Hangi doküman/bölümden aldığını belirt

YAPMA:
- Genel tavsiyeler verme, spesifik ol
- Speküla

syon yapma, sadece dokümanlara dayanarak cevap ver
- Uzun giriş paragrafları yazma, direkt konuya gir
- İngilizce kelime karıştırma

Türkçe dil bilgisi kurallarına DİKKAT ET. Yazım hatası yapma."""

        # Context metni oluştur
        context_parts = []
        
        if context_chunks:
            context_parts.append("📚 İLGİLİ DOKÜMAN BİLGİLERİ:\n")
            for i, chunk in enumerate(context_chunks, 1):
                context_parts.append(f"[Kaynak {i}: {chunk['source']}]")
                context_parts.append(f"{chunk['text']}\n")
        
        if fault_info:
            context_parts.append("\n🔧 ARIZA KODU BİLGİSİ:")
            context_parts.append(f"Kod: {fault_info.get('code')}")
            context_parts.append(f"İsim: {fault_info.get('name')}")
            context_parts.append(f"Kategori: {fault_info.get('category')}")
            context_parts.append(f"Önem: {fault_info.get('severity')}\n")
        
        context_text = "\n".join(context_parts) if context_parts else "Not: İlgili doküman bulunamadı."
        
        # Yapılandırılmış user prompt
        user_prompt = f"""SORU: {query}

{context_text}

CEVABINI ŞU FORMATTA VER:

📋 ÖZET:
[Tek cümle ile sorunun çözümü]

🔧 ADIMLAR:
1. [İlk adım - spesifik ve uygulanabilir]
2. [İkinci adım - spesifik ve uygulanabilir]
3. [Devam eden adımlar...]

⚠️ GÜVENLİK:
[Varsa güvenlik uyarıları, yoksa "Standart güvenlik önlemleri yeterli"]

📚 KAYNAK:
[Hangi doküman/bölümden - eğer dokümanda yoksa "Dokümanlarda bu bilgi yok" de]"""
        
        # Cevap üret (düşük temperature = daha tutarlı)
        answer = self.llm.generate(
            prompt=user_prompt, 
            system=system_prompt,
            temperature=0.3,  # Düşük = deterministik
            top_p=0.9,
            max_tokens=1024
        )
        
        return answer
    
    def save_vector_db(self, path: str):
        """Vektör DB'yi kaydet"""
        self.vector_store.save(path)


if __name__ == "__main__":
    # Test
    print("RAG Engine Test\n")
    
    # Test chunk'ları
    test_chunks = [
        {
            'text': 'Motor yağ seviyesi her çalıştırmadan önce kontrol edilmelidir. Yağ ölçüm çubuğunu çıkarın, temizleyin ve tekrar takın.',
            'source': 'test_manual.pdf',
            'chunk_id': 0
        },
        {
            'text': 'Radyatör kapağını asla sıcak motorda açmayın. Soğutma suyu seviyesi rezervuar işaretlerinde olmalıdır.',
            'source': 'test_manual.pdf',
            'chunk_id': 1
        }
    ]
    
    # RAG engine oluştur
    rag = RAGEngine(llm_model="mistral")
    
    # Dokümanları ekle
    rag.add_documents(test_chunks)
    
    # Sorgu
    query = "Yağ seviyesi nasıl kontrol edilir?"
    print(f"\n📝 Sorgu: {query}\n")
    
    # Context al
    context = rag.retrieve_context(query, top_k=2)
    print("🔍 Bulunan Context:")
    for c in context:
        print(f"  - {c['source']}: {c['text'][:60]}... (skor: {c['similarity']:.3f})")
    
    # Cevap üret (opsiyonel - Ollama gerekli)
    # answer = rag.generate_answer(query)
    # print(f"\n💬 Cevap:\n{answer}")
