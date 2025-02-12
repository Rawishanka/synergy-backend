virtual env -- Synergy-Backend
pip install -r requirements.txt
Synergy-Backend\Scripts\activate.bat
uvicorn main:app --reload
python 
fastapi dev main.py
pip install "passlib[bcrypt]"
pip install pyjwt
