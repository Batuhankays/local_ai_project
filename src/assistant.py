"""
Mühendislik Asistanı - Ana Sınıf

RAG engine, arıza kodu yöneticisi ve Ollama'yı birleştirerek
kullanıcı sorgularına cevap veren ana asistan sınıfı.
"""

import os
from typing import Optional, Dict, List
from src.rag_engine import RAGEngine
from src.fault_code_manager import FaultCodeManager


class EngineeringAssistant:
    """Offline çalışan mühendislik asistanı"""
    
    def __init__(
        self,
        vector_db_path: str = './data/vector_store/vectordb.pkl',
        fault_db_path: str = 'dokumanlar/ariza_kodlari.json',
        ollama_model: str = 'mistral'
    ):
        """
        Args:
            vector_db_path: Vektör veritabanı yolu
            fault_db_path: Arıza kodları JSON yolu
            ollama_model: Ollama model adı
        """
        print("🤖 Mühendislik Asistanı başlatılıyor...\n")
        
        # Arıza kodu yöneticisi
        self.fault_manager = FaultCodeManager(db_path=fault_db_path)
        
        # RAG engine
        self.rag_engine = RAGEngine(
            llm_model=ollama_model,
            vector_db_path=vector_db_path if os.path.exists(vector_db_path) else None
        )
        
        self.vector_db_path = vector_db_path
        
        print("\n✓ Asistan hazır!\n")
    
    def query(self, question: str, top_k: int = 3, use_rag: bool = True) -> str:
        """
        Kullanıcı sorusuna cevap ver
        
        Args:
            question: Kullanıcı sorusu
            top_k: RAG'den kaç chunk alınacak
            use_rag: RAG kullanılacak mı (False ise sadece LLM)
        
        Returns:
            Cevap metni
        """
        print(f"💭 Sorgu: {question}\n")
        
        # 1. Arıza kodlarında ara (soru kod içeriyorsa veya belirtiler varsa)
        fault_info = None
        fault_results = self.fault_manager.search_by_symptom(question)
        
        if fault_results:
            print(f"🔧 {len(fault_results)} arıza kodu bulundu")
            # İlk sonucu kullan
            fault_info = fault_results[0]
        
        # 2. RAG ile dokümanlardan context al
        context_chunks = None
        if use_rag:
            context_chunks = self.rag_engine.retrieve_context(question, top_k=top_k)
            if context_chunks:
                print(f"📚 {len(context_chunks)} ilgili doküman chunk'ı bulundu")
                for i, chunk in enumerate(context_chunks, 1):
                    print(f"   {i}. {chunk['source']} (benzerlik: {chunk['similarity']:.2f})")
        
        # 3. Cevap üret
        print(f"\n🤔 Cevap üretiliyor...\n")
        answer = self.rag_engine.generate_answer(
            query=question,
            context_chunks=context_chunks,
            fault_info=fault_info,
            top_k=top_k
        )
        
        return answer
    
    def analyze_fault(self, code: str) -> str:
        """
        Arıza kodu detaylı analizi
        
        Args:
            code: Arıza kodu (örn: "E101")
        
        Returns:
            Formatlanmış arıza bilgisi
        """
        fault = self.fault_manager.search_by_code(code)
        
        if not fault:
            return f"❌ Arıza kodu bulunamadı: {code}\n\n" \
                   f"Mevcut kodlar: {', '.join(self.fault_manager.get_all_codes())}"
        
        return self.fault_manager.format_fault_info(fault)
    
    def search_faults_by_symptom(self, symptom: str) -> str:
        """
        Belirtiye göre arıza ara
        
        Args:
            symptom: Belirti (örn: "titreşim", "duman")
        
        Returns:
            Bulunan arıza kodları
        """
        results = self.fault_manager.search_by_symptom(symptom)
        
        if not results:
            return f"❌ '{symptom}' belirtisi için arıza kodu bulunamadı"
        
        output = [f"🔍 '{symptom}' belirtisi için {len(results)} arıza kodu bulundu:\n"]
        
        for fault in results:
            output.append(
                f"  • {fault['code']}: {fault['name']} "
                f"({fault['severity']}, {fault['category']})"
            )
        
        return "\n".join(output)
    
    def get_critical_faults(self) -> str:
        """Kritik arıza kodlarını listele"""
        faults = self.fault_manager.get_critical_faults()
        
        output = [f"⚠️  {len(faults)} KRİTİK arıza kodu:\n"]
        
        for fault in faults:
            output.append(
                f"  • {fault['code']}: {fault['name']} "
                f"({fault['category']})"
            )
        
        return "\n".join(output)
    
    def interactive_mode(self):
        """İnteraktif soru-cevap modu"""
        print("=" * 60)
        print("🤖 Mühendislik Asistanı - İnteraktif Mod")
        print("=" * 60)
        print("\nKomutlar:")
        print("  - Soru sorun: Normal olarak yazın")
        print("  - Arıza kodu: 'fault E101' veya 'kod E101'")
        print("  - Belirtiye göre ara: 'belirti titreşim'")
        print("  - Kritik kodlar: 'kritik' veya 'critical'")
        print("  - Çıkış: 'exit', 'quit' veya 'çıkış'\n")
        print("=" * 60 + "\n")
        
        while True:
            try:
                user_input = input("💬 Siz: ").strip()
                
                if not user_input:
                    continue
                
                # Çıkış komutları
                if user_input.lower() in ['exit', 'quit', 'çıkış', 'q']:
                    print("\n👋 Görüşmek üzere!")
                    break
                
                # Arıza kodu sorgusu
                if user_input.lower().startswith(('fault ', 'kod ')):
                    code = user_input.split(maxsplit=1)[1].strip()
                    print(f"\n{self.analyze_fault(code)}\n")
                    continue
                
                # Belirtiye göre arama
                if user_input.lower().startswith('belirti '):
                    symptom = user_input.split(maxsplit=1)[1].strip()
                    print(f"\n{self.search_faults_by_symptom(symptom)}\n")
                    continue
                
                # Kritik kodlar
                if user_input.lower() in ['kritik', 'critical']:
                    print(f"\n{self.get_critical_faults()}\n")
                    continue
                
                # Normal sorgu
                answer = self.query(user_input)
                print(f"\n🤖 Asistan:\n{answer}\n")
                print("-" * 60 + "\n")
            
            except KeyboardInterrupt:
                print("\n\n👋 Görüşmek üzere!")
                break
            except Exception as e:
                print(f"\n❌ Hata: {str(e)}\n")


if __name__ == "__main__":
    # Test
    assistant = EngineeringAssistant()
    
    # Test 1: Arıza kodu analizi
    print("\n" + "=" * 60)
    print("TEST 1: Arıza Kodu Analizi")
    print("=" * 60)
    result = assistant.analyze_fault("E101")
    print(result)
    
    # Test 2: Belirti arama
    print("\n" + "=" * 60)
    print("TEST 2: Belirti Arama")
    print("=" * 60)
    result = assistant.search_faults_by_symptom("titreşim")
    print(result)
    
    # Test 3: Normal sorgu (RAG gerektirir)
    # print("\n" + "=" * 60)
    # print("TEST 3: Normal Sorgu")
    # print("=" * 60)
    # result = assistant.query("Yağ değişimi nasıl yapılır?")
    # print(result)
