# 🎧 Audio Creator App

Web application built with Flask that allows you to convert text to audio (using gTTS) and voice to text (using AssemblyAI). Includes user authentication and categorized content.

---

## ✨ Features

- 🔐 User registration, login and logout  
- 📄 Upload `.txt` files or paste your own text  
- 🎧 Convert any text to audio using gTTS  
- 🎙️ Record 10 seconds of voice and transcribe it to text using AssemblyAI  
- 🗂️ Category sections: Science, Recipes, Beauty, News, Entertainment, Children  
- 👤 Private dashboard for logged-in users  

---

## 🧠 Tech Stack

- Python 3.12  
- Flask (web framework)  
- gTTS (Google Text-to-Speech)  
- AssemblyAI (Speech-to-Text API)  
- Flask-Login (authentication)  
- SQLite (local DB)  
- SoundDevice + Scipy (for recording WAV)  
- HTML + CSS (custom layout)  
- dotenv (for secure API keys)  

---

## 🗂️ Project Structure

```
audiobook-flask-app/
├── app.py
├── .env
├── .gitignore
├── requirements.txt
├── static/
│   └── styles.css
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── transcription_result.html
│   └── [category].html
├── uploads/
├── audio/
└── venv/
```

---

## ⚙️ Setup Instructions

**1. Clone the repository**

```
git clone https://github.com/adrianalola/audiobook-flask-app.git
cd audiobook-flask-app
```

**2. Create and activate a virtual environment**

```
python -m venv venv
source venv/bin/activate      # For Mac/Linux
venv\Scripts\activate         # For Windows
```

**3. Install the dependencies**

```
pip install -r requirements.txt
```

**4. Create your `.env` file**

```
SECRET_KEY=your_flask_secret_key
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
```

**5. Run the app**

```
python app.py
```

Visit `http://127.0.0.1:5000` in your browser to use the application.

---

## 🚫 .gitignore (recommended)

```
# virtual environments
venv/
.env

# cache and compiled files
__pycache__/
*.pyc

# media
uploads/
audio/

# system
.DS_Store
```

---

## 👩‍💻 Author

**Adriana Martinez**  
Junior Software Engineer | Cloud & AI Enthusiast
