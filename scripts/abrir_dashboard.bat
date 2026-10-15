@echo off
REM Lanzador del dashboard Streamlit del Hotel Neptuno.
cd /d "%~dp0.."
call .venv\Scripts\activate.bat
streamlit run app.py
