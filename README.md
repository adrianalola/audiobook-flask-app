# 🎧 Audio Creator App

Flask-based web application that lets users convert text to audio using gTTS, and voice to text using AssemblyAI.

---

## 🚀 Features

- 🔐 User authentication (register, login, logout)
- 📄 Upload `.txt` files or paste custom text
- 🎙️ Record your voice (10 seconds) and get real-time transcription
- 🎧 Convert text into audio using gTTS
- 🧠 Thematic sections: Science, Recipes, Beauty, News, Entertainment, Children
- 🔒 Private dashboard for logged-in users

---

## 🛠 Tech Stack

- **Backend**: Python, Flask, SQLite
- **Audio**: gTTS, sounddevice, scipy
- **Transcription**: AssemblyAI API
- **Frontend**: HTML, CSS (custom)
- **Authentication**: Flask-Login
- **Environment Management**: `python-dotenv`, `.env`

---

## 📁 Project Structure


📦 audio-creator-app/
├── app.py
├── .env
├── .gitignore
├── requirements.txt
├── static/
│ └── styles.css
├── templates/
│ ├── index.html
│ ├── login.html
│ ├── register.html
│ ├── dashboard.html
│ ├── transcription_result.html
│ └── [category pages].html
├── uploads/
├── audio/
└── venv/


---

## ⚙️ Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/adrianalola/audio-creator-app.git
cd audio-creator-app

Create and activate a virtual environment

```bash

python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\\Scripts\\activate        # Windows
Install dependencies

```bash

pip install -r requirements.txt
Create your .env file

env

SECRET_KEY=your_flask_secret_key
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
Run the app

```bash

python app.py
Go to http://127.0.0.1:5000 in your browser

🧼 .gitignore (important)
gitignore

# virtual environment
venv/
.env

# Flask artifacts
__pycache__/
*.pyc
*.db

# media
uploads/
audio/

# system
.DS_Store
👩‍💻 Author
Adriana Martinez
Cloud & Python Developer
🛰️ Passionate about building powerful tools with clean architecture