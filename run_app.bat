@echo off
echo ===================================================
echo Starting PolyBot Streamlit Web Application...
echo ===================================================
call venv\Scripts\activate.bat
streamlit run app.py
pause
