@echo off
REM ============================================================
REM  Finca Vistabonita - Revenue Dashboard (puerto 8501)
REM  1) Procesa el buzon (Excel-Lunes\BUZON)
REM  2) Abre el dashboard en el navegador
REM ============================================================
cd /d "%~dp0"
call .venv\Scripts\activate.bat
set PYTHONIOENCODING=utf-8

echo.
echo === Procesando buzon Finca Vistabonita ===
python scripts\procesar_buzon.py
echo.
echo === Abriendo dashboard Finca Vistabonita ===
start "" "http://localhost:8501"
streamlit run app.py
