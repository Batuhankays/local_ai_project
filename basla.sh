#!/bin/bash
# Muhendislik Asistani - macOS/Linux Baslama Scripti
# Kullanim: bash basla.sh

set -e  # Hata olursa dur

# Renk kodlari
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # Renk sifirla

ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
info() { echo -e "${YELLOW}[BILGI]${NC} $1"; }
err()  { echo -e "${RED}[HATA]${NC} $1"; }

echo "========================================"
echo "   Muhendislik Asistani Baslatiliyor"
echo "========================================"
echo ""

# Script'in bulundugu dizine git
cd "$(dirname "$0")"

# ---- 1. PYTHON KONTROLU ----
if command -v python3 &>/dev/null; then
    ok "Python3 bulundu: $(python3 --version)"
elif command -v python &>/dev/null; then
    ok "Python bulundu: $(python --version)"
else
    err "Python yuklu degil!"
    echo ""
    echo "Cozum (macOS):"
    echo "  1. https://www.python.org/downloads/ adresine gidin"
    echo "  2. macOS icin Python indirin ve kurun"
    echo "  VEYA Homebrew ile: brew install python3"
    echo ""
    read -p "Devam etmek icin Enter'a basin..."
    exit 1
fi

# Python komutunu belirle
PYTHON_CMD="python3"
command -v python3 &>/dev/null || PYTHON_CMD="python"

# ---- 2. SANAL ORTAM KONTROLU ----
if [ -f "venv/bin/activate" ]; then
    ok "Sanal ortam mevcut"
else
    if [ -d "venv" ]; then
        info "Sanal ortam bozuk, yeniden olusturuluyor..."
        rm -rf venv
    else
        info "Ilk kurulum yapiliyor..."
    fi
    echo "Bu islem 1-2 dakika surebilir, lutfen bekleyin..."
    $PYTHON_CMD -m venv venv
    if [ $? -ne 0 ]; then
        err "Sanal ortam olusturulamadi!"
        read -p "Devam etmek icin Enter'a basin..."
        exit 1
    fi
    ok "Sanal ortam olusturuldu"
fi
echo ""

# ---- 3. SANAL ORTAMI AKTIFLE ----
info "Sanal ortam aktive ediliyor..."
source venv/bin/activate
ok "Sanal ortam aktif"
echo ""

# ---- 4. PAKET KURULUMU ----
info "Paketler kontrol ediliyor..."
if pip show streamlit &>/dev/null; then
    ok "Paketler zaten yuklu"
else
    info "Gerekli paketler yukleniyor (ilk kurumda 2-5 dakika surebilir)..."
    echo ""
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo ""
        err "Paket yukleme basarisiz!"
        echo ""
        echo "Olasilik 1: Internet baglantiniz yok"
        echo "Olasilik 2: requirements.txt dosyasi bulunamadi"
        echo ""
        read -p "Devam etmek icin Enter'a basin..."
        exit 1
    fi
    echo ""
    ok "Paketler yuklendi"
fi
echo ""

# ---- 5. OLLAMA KONTROLU ----
info "Ollama kontrol ediliyor..."
if ! command -v ollama &>/dev/null; then
    echo ""
    err "Ollama bulunamadi!"
    echo ""
    echo "Ollama, yapay zeka motorudur ve zorunludur."
    echo ""
    echo "Kurulum adimlari (macOS):"
    echo "  1. https://ollama.ai/download adresine gidin"
    echo "  2. macOS icin indirin ve kurun"
    echo "  VEYA Homebrew ile: brew install ollama"
    echo "  3. Kurulum bittikten sonra bu scripti tekrar calistirin"
    echo ""
    read -p "Devam etmek icin Enter'a basin..."
    exit 1
fi

if ! ollama list &>/dev/null; then
    echo ""
    err "Ollama yuklu ama calismiyor!"
    echo ""
    echo "Cozum: Yeni bir terminal acin ve su komutu calistirin:"
    echo "  ollama serve"
    echo ""
    echo "Sonra bu scripti tekrar calistirin."
    echo ""
    read -p "Devam etmek icin Enter'a basin..."
    exit 1
fi
ok "Ollama calisiyor"
echo ""

# ---- 6. MISTRAL MODEL KONTROLU ----
info "Mistral modeli kontrol ediliyor..."
if ! ollama list | grep -q "mistral"; then
    echo ""
    echo "[UYARI] Mistral modeli yuklu degil! (yaklasik 4GB)"
    echo ""
    read -p "Simdi indirilsin mi? (e=Evet, h=Hayir): " choice
    case "$choice" in
        e|E|evet|Evet)
            echo ""
            info "Mistral indiriliyor, lutfen bekleyin..."
            ollama pull mistral
            ok "Mistral islemi tamamlandi"
            ;;
        *)
            info "Mistral atlandi. Daha sonra indirmek icin: ollama pull mistral"
            ;;
    esac
    echo ""
else
    ok "Mistral mevcut"
    echo ""
fi

# ---- 7. LLAMA3.2 MODEL KONTROLU ----
info "Llama3.2:3b modeli kontrol ediliyor..."
if ! ollama list | grep -q "llama3.2"; then
    echo ""
    echo "[UYARI] Llama3.2:3b modeli yuklu degil! (yaklasik 2GB)"
    echo ""
    read -p "Simdi indirilsin mi? (e=Evet, h=Hayir): " choice
    case "$choice" in
        e|E|evet|Evet)
            echo ""
            info "Llama3.2:3b indiriliyor, lutfen bekleyin..."
            ollama pull llama3.2:3b
            ok "Llama3.2:3b islemi tamamlandi"
            ;;
        *)
            info "Llama3.2:3b atlandi. Daha sonra indirmek icin: ollama pull llama3.2:3b"
            ;;
    esac
    echo ""
else
    ok "Llama3.2:3b mevcut"
    echo ""
fi

# ---- 8. WEB ARAYUZU ----
echo "========================================"
echo "  Web Arayuzu Baslatiliyor..."
echo "========================================"
echo ""
echo "Tarayicinizda otomatik acilacak."
echo "Acilmazsa: http://localhost:8501"
echo ""
echo "Durdurmak icin: Ctrl+C"
echo ""

# macOS'ta tarayiciyi otomatik ac
sleep 2
open "http://localhost:8501" 2>/dev/null || true

streamlit run app.py

echo ""
echo "========================================"
echo "  Uygulama kapandi."
echo "========================================"
