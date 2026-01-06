"""
Mühendislik Asistanı - Web Arayüzü
Streamlit tabanlı kullanıcı dostu arayüz

Kullanım: streamlit run app.py
"""

import streamlit as st
import os
import sys
from pathlib import Path
import shutil
from datetime import datetime

# Proje kök dizinini path'e ekle
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.assistant import EngineeringAssistant
from src.fault_code_manager import FaultCodeManager
from src.document_processor import DocumentProcessor
from src.rag_engine import RAGEngine


# Sayfa konfigürasyonu
st.set_page_config(
    page_title="Mühendislik Asistanı",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS ile özelleştirme
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        color: #155724;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        border-radius: 5px;
        color: #856404;
    }
    .error-box {
        padding: 1rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Session state başlat"""
    if 'assistant' not in st.session_state:
        st.session_state.assistant = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'training_done' not in st.session_state:
        st.session_state.training_done = check_training_status()


def check_training_status():
    """Training yapılmış mı kontrol et"""
    vector_db_path = './data/vector_store/vectordb.pkl'
    return os.path.exists(vector_db_path)


def check_ollama():
    """Ollama servisini kontrol et"""
    try:
        import ollama
        models = ollama.list()
        return True, models.get('models', [])
    except:
        return False, []


def load_assistant():
    """Asistanı yükle"""
    if st.session_state.assistant is None:
        try:
            with st.spinner('🤖 Asistan yükleniyor...'):
                st.session_state.assistant = EngineeringAssistant()
            return True
        except Exception as e:
            st.error(f"❌ Asistan yüklenemedi: {str(e)}")
            return False
    return True


# 📱 SIDEBAR - Navigasyon
with st.sidebar:
    st.markdown("## 🔧 Mühendislik Asistanı")
    st.markdown("---")
    
    page = st.radio(
        "Menü",
        ["🏠 Ana Sayfa", "📚 Training", "💬 Sorgulama", "🔍 Arıza Kodları", "⚙️ Ayarlar"],
        index=0
    )
    
    st.markdown("---")
    
    # Durum göstergeleri
    st.markdown("### 📊 Sistem Durumu")
    
    # Ollama kontrolü
    ollama_ok, ollama_models = check_ollama()
    if ollama_ok:
        st.success("✅ Ollama Çalışıyor")
        if ollama_models:
            st.caption(f"Model: {ollama_models[0].get('name', 'N/A')}")
    else:
        st.error("❌ Ollama Bulunamadı")
        st.caption("[Nasıl kurulur?](#)")
    
    # Training durumu
    if st.session_state.training_done:
        st.success("✅ Training Tamamlandı")
    else:
        st.warning("⚠️ Training Gerekli")
    
    # PDF sayısı
    pdf_folder = "dokumanlar/manueller"
    if os.path.exists(pdf_folder):
        pdf_count = len([f for f in os.listdir(pdf_folder) if f.endswith('.pdf')])
        st.info(f"📄 {pdf_count} PDF yüklü")
    else:
        st.caption("📄 0 PDF yüklü")


# 🏠 ANA SAYFA
if page == "🏠 Ana Sayfa":
    st.markdown('<div class="main-header">🔧 Mühendislik Asistanı</div>', unsafe_allow_html=True)
    st.markdown("### Offline Jeneratör Bilgi Sistemi")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📚 Doküman İşleme")
        st.write("✓ PDF manuel okuma")
        st.write("✓ Akıllı metin analizi")
        st.write("✓ Vektör veritabanı")
    
    with col2:
        st.markdown("#### 🔧 Arıza Kodları")
        st.write("✓ 15+ jeneratör arızası")
        st.write("✓ Detaylı çözümler")
        st.write("✓ Bakım periyotları")
    
    with col3:
        st.markdown("#### 🤖 AI Asistan")
        st.write("✓ Offline çalışır (Ollama)")
        st.write("✓ Türkçe destekli")
        st.write("✓ Teknik sorulara cevap")
    
    st.markdown("---")
    
    # Hızlı başlangıç
    st.markdown("### 🚀 Hızlı Başlangıç")
    
    if not ollama_ok:
        st.markdown('<div class="error-box">❌ Ollama yüklü değil veya çalışmıyor!</div>', unsafe_allow_html=True)
        st.markdown("""
        **Çözüm:**
        1. [Ollama'yı indirin](https://ollama.ai/download)
        2. Kurulum sonrası terminal açın
        3. `ollama pull mistral` komutunu çalıştırın
        """)
    elif not st.session_state.training_done:
        st.markdown('<div class="warning-box">⚠️ Henüz training yapılmamış!</div>', unsafe_allow_html=True)
        st.markdown("""
        **Adımlar:**
        1. Sol menüden **📚 Training** sekmesine gidin
        2. PDF manuellerinizi yükleyin
        3. Training'i başlatın
        """)
    else:
        st.markdown('<div class="success-box">✅ Sistem kullanıma hazır!</div>', unsafe_allow_html=True)
        st.markdown("""
        **Yapabilecekleriniz:**
        - 💬 **Sorgulama**: Manuellerden bilgi çekin
        - 🔍 **Arıza Kodları**: Hata kodlarını analiz edin
        """)
        
        if st.button("🚀 Sorgulama Sayfasına Git", type="primary"):
            st.rerun()


# 📚 TRAINING SAYFASI
elif page == "📚 Training":
    st.title("📚 Sistem Eğitimi (Training)")
    
    st.markdown("""
    Bu sayfada PDF manuellerinizi yükleyip sistemi eğitebilirsiniz.
    Training sonrası AI asistan, dokümanlardan bilgi çekerek sorularınıza cevap verebilecek.
    """)
    
    st.markdown("---")
    
    # PDF yükleme
    st.markdown("### 1️⃣ PDF Manuel Yükleme")
    
    uploaded_files = st.file_uploader(
        "PDF dosyalarınızı seçin (birden fazla yüklenebilir)",
        type=['pdf'],
        accept_multiple_files=True,
        help="Jeneratör kullanım kılavuzları, bakım manuelleri vb."
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} PDF seçildi")
        
        # Klasörü oluştur
        pdf_folder = "dokumanlar/manueller"
        os.makedirs(pdf_folder, exist_ok=True)
        
        if st.button("💾 PDF'leri Kaydet", type="primary"):
            with st.spinner("PDF'ler kaydediliyor..."):
                saved_count = 0
                for uploaded_file in uploaded_files:
                    # Dosya adını güvenli hale getir
                    filename = uploaded_file.name
                    filepath = os.path.join(pdf_folder, filename)
                    
                    # Kaydet
                    with open(filepath, 'wb') as f:
                        f.write(uploaded_file.getbuffer())
                    saved_count += 1
                
                st.success(f"✅ {saved_count} PDF başarıyla kaydedildi!")
                st.rerun()
    
    # Mevcut PDF'ler
    st.markdown("### 📄 Yüklü PDF'ler")
    
    pdf_folder = "dokumanlar/manueller"
    if os.path.exists(pdf_folder):
        pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
        
        if pdf_files:
            for pdf in pdf_files:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"📄 {pdf}")
                with col2:
                    if st.button("🗑️", key=f"del_{pdf}"):
                        os.remove(os.path.join(pdf_folder, pdf))
                        st.rerun()
        else:
            st.info("Henüz PDF yüklenmemiş")
    
    st.markdown("---")
    
    # Training başlat
    st.markdown("### 2️⃣ Training Başlat")
    
    st.markdown("""
    **Not:** Training işlemi PDF sayısına göre 2-10 dakika sürebilir.
    Bu süre zarfında sayfayı kapatmayın.
    """)
    
    if st.button("🚀 Training'i Başlat", type="primary", disabled=not pdf_files if 'pdf_files' in locals() else True):
        try:
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # 1. PDF'leri işle
            status_text.text("📄 PDF'ler işleniyor...")
            progress_bar.progress(20)
            
            processor = DocumentProcessor(chunk_size=800, overlap=200)
            chunks = processor.process_all_pdfs(pdf_folder)
            
            if not chunks:
                st.error("❌ Hiç chunk oluşturulamadı!")
                st.stop()
            
            # 2. RAG engine
            status_text.text("🧠 RAG Engine başlatılıyor...")
            progress_bar.progress(40)
            
            rag = RAGEngine(embedding_model="all-MiniLM-L6-v2", llm_model="mistral")
            
            # 3. Embedding oluştur
            status_text.text("🔄 Embedding'ler oluşturuluyor...")
            progress_bar.progress(60)
            
            rag.add_documents(chunks)
            
            # 4. Kaydet
            status_text.text("💾 Vektör veritabanı kaydediliyor...")
            progress_bar.progress(80)
            
            vector_db_path = './data/vector_store/vectordb.pkl'
            rag.save_vector_db(vector_db_path)
            
            # Tamamlandı
            progress_bar.progress(100)
            status_text.text("✅ Training tamamlandı!")
            
            st.success(f"""
            🎉 **Training Başarılı!**
            
            - {len(pdf_files)} PDF işlendi
            - {len(chunks)} chunk oluşturuldu
            - Vektör DB kaydedildi
            
            Artık sorgulama yapabilirsiniz!
            """)
            
            st.session_state.training_done = True
            
        except Exception as e:
            st.error(f"❌ Training hatası: {str(e)}")
            import traceback
            st.code(traceback.format_exc())


# 💬 SORGULAMA SAYFASI
elif page == "💬 Sorgulama":
    st.title("💬 AI Asistan Sorgulama")
    
    if not st.session_state.training_done:
        st.warning("⚠️ Önce training yapmanız gerekiyor! **📚 Training** sekmesine gidin.")
        st.stop()
    
    # Asistanı yükle
    if not load_assistant():
        st.stop()
    
    st.markdown("Jeneratör hakkında sorularınızı sorun. AI asistan, yüklediğiniz manuellerden bilgi çekerek cevap verecek.")
    
    # Chat geçmişi
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Kullanıcı input
    if prompt := st.chat_input("Sorunuzu yazın... (örn: 500 saatlik bakımda neler yapılır?)"):
        # Kullanıcı mesajını göster
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Asistan cevabı
        with st.chat_message("assistant"):
            with st.spinner("Düşünüyor..."):
                try:
                    answer = st.session_state.assistant.query(prompt, top_k=3)
                    st.markdown(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                except Exception as e:
                    error_msg = f"❌ Hata: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
    
    # Chat temizleme
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.chat_history = []
        st.rerun()


# 🔍 ARIZA KODLARI SAYFASI
elif page == "🔍 Arıza Kodları":
    st.title("🔍 Arıza Kodu Analizi")
    
    fault_manager = FaultCodeManager()
    
    tab1, tab2, tab3 = st.tabs(["Kod Ara", "Belirti Ara", "Tüm Kodlar"])
    
    # TAB 1: Kod Ara
    with tab1:
        st.markdown("### Arıza Koduna Göre Arama")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            code_input = st.text_input("Arıza kodu girin (örn: E101)", key="code_search")
        with col2:
            search_btn = st.button("🔍 Ara", type="primary", key="code_btn")
        
        if search_btn and code_input:
            fault = fault_manager.search_by_code(code_input.upper())
            
            if fault:
                st.markdown(f"## {fault['code']}: {fault['name']}")
                
                # Önem seviyesi
                severity_color = {
                    'CRITICAL': '🔴',
                    'HIGH': '🟠',
                    'MEDIUM': '🟡'
                }
                st.markdown(f"**Önem:** {severity_color.get(fault['severity'], '⚪')} {fault['severity']}")
                st.markdown(f"**Kategori:** {fault['category']}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 🔍 Belirtiler")
                    for symptom in fault['symptoms']:
                        st.write(f"• {symptom}")
                    
                    st.markdown("#### 🔎 Olası Nedenler")
                    for cause in fault['causes']:
                        st.write(f"• {cause}")
                
                with col2:
                    st.markdown("#### ✅ Çözüm Adımları")
                    for solution in fault['solutions']:
                        st.write(solution)
                    
                    if fault.get('maintenance_interval_hours'):
                        st.info(f"🕐 Bakım Periyodu: {fault['maintenance_interval_hours']} saat")
            else:
                st.error(f"❌ '{code_input}' kodu bulunamadı")
    
    # TAB 2: Belirti Ara
    with tab2:
        st.markdown("### Belirtiye Göre Arama")
        
        symptom_input = st.text_input("Belirti girin (örn: titreşim, duman, yağ)", key="symptom_search")
        
        if st.button("🔍 Ara", type="primary", key="symptom_btn") and symptom_input:
            results = fault_manager.search_by_symptom(symptom_input)
            
            if results:
                st.success(f"✅ '{symptom_input}' için {len(results)} sonuç bulundu")
                
                for fault in results:
                    with st.expander(f"{fault['code']}: {fault['name']} ({fault['severity']})"):
                        st.markdown(f"**Kategori:** {fault['category']}")
                        st.markdown("**İlk 3 Çözüm:**")
                        for i, sol in enumerate(fault['solutions'][:3], 1):
                            st.write(f"{i}. {sol}")
            else:
                st.warning(f"⚠️ '{symptom_input}' için sonuç bulunamadı")
    
    # TAB 3: Tüm Kodlar
    with tab3:
        st.markdown("### Tüm Arıza Kodları")
        
        # Kategoriye göre filtrele
        categories = list(set([f['category'] for f in fault_manager.fault_codes]))
        selected_category = st.selectbox("Kategori Filtrele", ["Tümü"] + categories)
        
        # Filtrelenmiş kodlar
        if selected_category == "Tümü":
            filtered_faults = fault_manager.fault_codes
        else:
            filtered_faults = [f for f in fault_manager.fault_codes if f['category'] == selected_category]
        
        # Tablo olarak göster
        for fault in filtered_faults:
            severity_emoji = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡'}
            
            with st.expander(f"{severity_emoji.get(fault['severity'], '⚪')} {fault['code']}: {fault['name']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Kategori:** {fault['category']}")
                    st.markdown(f"**Önem:** {fault['severity']}")
                
                with col2:
                    if fault.get('maintenance_interval_hours'):
                        st.markdown(f"**Bakım:** {fault['maintenance_interval_hours']} saat")
                
                st.markdown("**Belirtiler:**")
                st.write(", ".join(fault['symptoms'][:3]))


# ⚙️ AYARLAR SAYFASI
elif page == "⚙️ Ayarlar":
    st.title("⚙️ Sistem Ayarları")
    
    st.markdown("### 🗄️ Veri Yönetimi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Vektör DB'yi Temizle", help="Training'i sıfırlar"):
            vector_db_path = './data/vector_store/vectordb.pkl'
            if os.path.exists(vector_db_path):
                os.remove(vector_db_path)
                st.success("✅ Vektör DB temizlendi")
                st.session_state.training_done = False
                st.rerun()
            else:
                st.info("ℹ️ Vektör DB zaten yok")
    
    with col2:
        if st.button("🗑️ Tüm PDF'leri Sil", help="Yüklü PDF'leri siler"):
            pdf_folder = "dokumanlar/manueller"
            if os.path.exists(pdf_folder):
                for f in os.listdir(pdf_folder):
                    if f.endswith('.pdf'):
                        os.remove(os.path.join(pdf_folder, f))
                st.success("✅ PDF'ler silindi")
                st.rerun()
    
    st.markdown("---")
    
    st.markdown("### ℹ️ Sistem Bilgisi")
    
    # Python version
    st.write(f"🐍 Python: {sys.version.split()[0]}")
    
    # Ollama
    ollama_ok, models = check_ollama()
    if ollama_ok and models:
        st.write(f"🤖 Ollama Model: {models[0].get('name', 'N/A')}")
    
    # Training durumu
    st.write(f"📊 Training: {'✅ Tamamlandı' if st.session_state.training_done else '❌ Yapılmadı'}")
    
    # PDF sayısı
    pdf_folder = "dokumanlar/manueller"
    if os.path.exists(pdf_folder):
        pdf_count = len([f for f in os.listdir(pdf_folder) if f.endswith('.pdf')])
        st.write(f"📄 Yüklü PDF: {pdf_count}")


# Session state başlat
init_session_state()
