@echo off
REM Mühendislik Asistanı - Kolay Başlatma Scripti
REM Bu dosyayı çift tıklayarak web arayüzünü başlatın

echo ========================================
echo    Muhendislik Asistani Baslatiliyor
echo ========================================
echo.

REM Python kontrolü
python --version >nul 2>&1
if errorlevel 1 (
    echo [HATA] Python yuklu degil!
    echo.
    echo Lutfen Python yukleyin: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python bulundu
echo.

REM Sanal ortam kontrolü
if not exist "venv\" (
    echo [BILGI] Sanal ortam bulunamadi, olusturuluyor...
    python -m venv venv
    echo [OK] Sanal ortam olusturuldu
    echo.
)

REM Sanal ortamı aktifleştir
echo [BILGI] Sanal ortam aktive ediliyor...
call venv\Scripts\activate.bat

REM Bağımlılıkları kontrol et
echo [BILGI] Gerekli paketler kontrol ediliyor...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo [BILGI] Paketler yukleniyor (ilk seferde 2-5 dakika surebilir)...
    pip install -r requirements.txt
    echo [OK] Paketler yuklendi
    echo.
)

REM Ollama kontrolü
echo [BILGI] Ollama kontrol ediliyor...
ollama list >nul 2>&1
if errorlevel 1 (
    echo.
    echo [UYARI] Ollama bulunamadi veya calismiyor!
    echo.
    echo Cozum:
    echo   1. Ollama yukleyin: https://ollama.ai/download
    echo   2. Kurulum sonrasi terminal apin:
    echo      ollama pull mistral
    echo.
    echo Devam etmek icin bir tusa basin...
    pause
)

REM Web arayüzünü başlat
echo.
echo ========================================
echo   Web Arayuzu Baslatiliyor...
echo ========================================
echo.
echo Tarayicinizda acilacak.
echo Otomatik acilmazsa: http://localhost:8501
echo.
echo Kapatmak icin bu pencereyi kapatabilirsiniz.
echo.

streamlit run app.py

REM Hata durumunda bekle
if errorlevel 1 (
    echo.
    echo [HATA] Bir sorun olustu!
    echo.
    pause
)
