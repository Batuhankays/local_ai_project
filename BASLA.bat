@echo off
REM Muhendislik Asistani - Kolay Baslama Scripti
chcp 65001 >nul

echo ========================================
echo    Muhendislik Asistani Baslatiliyor
echo ========================================
echo.

REM ---- 1. PYTHON KONTROLU ----
python --version >nul
if errorlevel 1 (
    echo [HATA] Python yuklu degil!
    echo.
    echo Cozum:
    echo   1. https://www.python.org/downloads/ adresine gidin
    echo   2. Download Python butonuna tiklayin
    echo   3. Kurulum sirasinda "Add Python to PATH" kutusunu isaretleyin
    echo   4. Kurulum bittikten sonra bu dosyayi tekrar calistirin
    echo.
    pause
    exit /b 1
)
echo [OK] Python bulundu
echo.

REM ---- 2. SANAL ORTAM KONTROLU ----
if exist "venv\Scripts\activate.bat" (
    echo [OK] Sanal ortam mevcut
    echo.
) else (
    if exist "venv\" (
        echo [BILGI] Sanal ortam bozuk, yeniden olusturuluyor...
        rmdir /s /q venv
    ) else (
        echo [BILGI] Ilk kurulum yapiliyor...
    )
    echo Bu islem 1-2 dakika surebilir, lutfen bekleyin...
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo [HATA] Sanal ortam olusturulamadi!
        echo.
        pause
        exit /b 1
    )
    echo [OK] Sanal ortam olusturuldu
    echo.
)

REM ---- 3. SANAL ORTAMI AKTIFLE ----
echo [BILGI] Sanal ortam aktive ediliyor...
call venv\Scripts\activate.bat
echo [OK] Sanal ortam aktif
echo.

REM ---- 4. PAKET KURULUMU ----
echo [BILGI] Paketler kontrol ediliyor...
pip show streamlit >nul
if errorlevel 1 (
    echo [BILGI] Gerekli paketler yukleniyor...
    echo Bu islem 2-5 dakika surebilir, lutfen bekleyin...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [HATA] Paket yukleme basarisiz!
        echo.
        echo Olasilik 1: Internet baglantiniz yok
        echo Olasilik 2: requirements.txt dosyasi bulunamadi
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [OK] Paketler yuklendi
    echo.
) else (
    echo [OK] Paketler zaten yuklu
    echo.
)

REM ---- 5. OLLAMA KONTROLU ----
echo [BILGI] Ollama kontrol ediliyor...
ollama list >nul
if errorlevel 1 (
    echo.
    echo [UYARI] Ollama bulunamadi!
    echo.
    echo Ollama, yapay zeka motorudur ve zorunludur.
    echo.
    echo Kurulum adimlari:
    echo   1. https://ollama.ai/download adresine gidin
    echo   2. Download for Windows butonuna tiklayin
    echo   3. Indirilen dosyayi calistirin ve kurun
    echo   4. Kurulum bittikten sonra bu dosyayi tekrar calistirin
    echo.
    pause
    exit /b 1
)
echo [OK] Ollama calisiyor
echo.

REM ---- 6. MISTRAL MODEL KONTROLU ----
echo [BILGI] Mistral modeli kontrol ediliyor...
ollama list | findstr "mistral" >nul
if errorlevel 1 (
    echo [UYARI] Mistral modeli yuklu degil! (yaklasik 4GB)
    echo.
    choice /C EN /M "Simdi indirilsin mi? (E=Evet, N=Hayir)"
    if errorlevel 2 (
        echo.
        echo [BILGI] Mistral atlandi.
        echo.
        goto :check_llama
    )
    echo.
    echo [BILGI] Mistral indiriliyor, lutfen bekleyin...
    ollama pull mistral
    echo [OK] Mistral islemi tamamlandi
    echo.
) else (
    echo [OK] Mistral mevcut
    echo.
)

REM ---- 7. LLAMA3.2 MODEL KONTROLU ----
:check_llama
echo [BILGI] Llama3.2:3b modeli kontrol ediliyor...
ollama list | findstr "llama3.2" >nul
if errorlevel 1 (
    echo [UYARI] Llama3.2:3b modeli yuklu degil! (yaklasik 2GB)
    echo.
    choice /C EN /M "Simdi indirilsin mi? (E=Evet, N=Hayir)"
    if errorlevel 2 (
        echo.
        echo [BILGI] Llama3.2:3b atlandi.
        echo.
        goto :start_app
    )
    echo.
    echo [BILGI] Llama3.2:3b indiriliyor, lutfen bekleyin...
    ollama pull llama3.2:3b
    echo [OK] Llama3.2:3b islemi tamamlandi
    echo.
) else (
    echo [OK] Llama3.2:3b mevcut
    echo.
)

REM ---- 8. WEB ARAYUZU ----
:start_app
echo ========================================
echo   Web Arayuzu Baslatiliyor...
echo ========================================
echo.
echo Tarayicinizda otomatik acilacak.
echo Acilmazsa: http://localhost:8501
echo.
echo Kapatmak icin bu pencereyi kapatin.
echo.

streamlit run app.py

echo.
echo ========================================
echo   Uygulama kapandi.
echo ========================================
pause >nul
