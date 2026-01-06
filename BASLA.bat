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
    if errorlevel 1 (
        echo [HATA] Sanal ortam olusturulamadi!
        pause
        exit /b 1
    )
    echo [OK] Sanal ortam olusturuldu
    echo.
)

REM Sanal ortamı aktifleştir
echo [BILGI] Sanal ortam aktive ediliyor...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo [OK] Sanal ortam aktif
    echo.
) else (
    echo [HATA] activate.bat bulunamadi!
    echo Aranan konum: %CD%\venv\Scripts\activate.bat
    pause
    exit /b 1
)

REM Pip kontrolü
echo [BILGI] Pip version kontrol ediliyor...
pip --version
if errorlevel 1 (
    echo [HATA] Pip bulunamadi! Sanal ortam dogru aktive edilmemis olabilir.
    pause
    exit /b 1
)
echo [OK] Pip bulundu
echo.

REM Bağımlılıkları kontrol et
echo [BILGI] Gerekli paketler kontrol ediliyor...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo [BILGI] Streamlit bulunamadi, TUM paketler yukleniyor...
    echo Bu islem 2-5 dakika surebilir, lutfen bekleyin...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [HATA] Paket yukleme basarisiz!
        echo.
        echo Olasilik 1: Internet baglantiniz yok
        echo Olasilik 2: requirements.txt dosyasi bulunamadi
        echo Olasilik 3: Pip guncel degil (pip install --upgrade pip)
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [OK] Paketler yuklendi
    echo.
) else (
    echo [OK] Streamlit zaten yuklu
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
    echo   2. Kurulum sonrasi:
    echo      ollama pull llama3.2:3b
    echo.
    pause
    goto :skip_model_check
)

echo [OK] Ollama calisiy or
echo.
echo [BILGI] llama3.2:3b modeli kullanilacak
echo   Yoksa indirmek icin: ollama pull llama3.2:3b
echo.

:skip_model_check

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

REM Her durumda pencereyi açık tut
echo.
echo ========================================
echo Kapatmak icin bu pencereyi kapatabilirsiniz.
echo ========================================
pause >nul
