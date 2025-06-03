from flask import Flask, request, send_file, render_template, redirect, url_for, flash
from gtts import gTTS  #generar audio a partir de texto google 
import os
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import sounddevice as sd
from scipy.io.wavfile import write
import assemblyai as aai

#cargar variables de entorno
load_dotenv()
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

app = Flask(__name__)

#crear carpetas si no existen
os.makedirs("uploads", exist_ok=True)
os.makedirs("audio", exist_ok=True)

#configuración de la base de datos y login
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "mysecretkey")
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#modelo de usuario
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

#loader usuario
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#lar uta principal
@app.route('/')
def home():
    return render_template("index.html")

#generar audio desde archivo
@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    if 'textFile' in request.files:
        text_file = request.files['textFile']
        if text_file and text_file.filename.endswith('.txt'):
            text = text_file.read().decode('utf-8')
        else:
            return "Error: Archivo no válido", 400
    else:
        return "Error: No se subió un archivo", 400

    language = request.form.get('language', 'en')
    tts = gTTS(text=text, lang=language)

    #guardar el audio
    audio_path = os.path.join("audio", "audio.mp3")
    tts.save(audio_path)

    return send_file(audio_path, mimetype='audio/mpeg', as_attachment=True, download_name="audio.mp3")

#generar audio desde texto
@app.route('/generate-audio-text', methods=['POST'])
def generate_audio_text():
    text = request.form.get('text')
    language = request.form.get('language', 'en')
    supported_languages = ['en', 'es', 'fr', 'de', 'it']
    if language not in supported_languages:
        return f"Error: Language '{language}' not supported. Supported languages are: {', '.join(supported_languages)}", 400

    if not text:
        return "Error: No se proporcionó texto", 400

    tts = gTTS(text=text, lang=language)
    audio = BytesIO()
    tts.write_to_fp(audio)
    audio.seek(0)

    return send_file(audio, mimetype='audio/mpeg', as_attachment=True, download_name="audio.mp3")

#rutas de categorías de artículos
@app.route('/science')
def science():
    return render_template("science.html")

@app.route('/recipes')
def recipes():
    return render_template("recipes.html")

@app.route('/beauty')
def beauty():
    return render_template("beauty.html")

@app.route('/news')
def news():
    return render_template("news.html")

@app.route('/entertainment')
def entertainment():
    return render_template("entertainment.html")

@app.route('/children')
def children():
    return render_template("children.html")

@app.route('/library')
def library():
    return redirect("https://www.sciencedirect.com/")

#register de user
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        #verificamos si el usuario ya existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("User already exist try again.")
            return redirect(url_for('register'))

        #create new user con passsword
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Register is succesfull! now you can login.")
        return redirect(url_for('login'))

    return render_template("register.html")

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Inicio de sesión exitoso.")
            return redirect(url_for('dashboard'))
        else:
            flash("Error, please try again.")

    return render_template("login.html")

#privado para usuarios logueados
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.username)

#cerrar session 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sesion close.")
    return redirect(url_for('login'))

#grabar voz, transcribir y mostrar texto
@app.route('/transcribe', methods=['GET'])
@login_required
def transcribe():
    try:
        record()  #grabar 10 segundos
        transcript = speech_to_text()
        return render_template("transcription_result.html", transcript=transcript)
    except Exception as e:
        return f"<h2>Error:</h2><p>{str(e)}</p>", 500

#grabar voz
def record(duration=60, filename="output.wav"):
    fs = 44100  # Sample rate
    print("Recording...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, audio)
    print(f"Audio saved as {filename}")

#convertir voz a texto con AssemblyAI
def speech_to_text(audio_file="output.wav"):
    config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)
    transcript = aai.Transcriber(config=config).transcribe(audio_file)

    if transcript.status == "error":
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    return transcript.text.strip()

#crear la database si no existe
with app.app_context():
    db.create_all()

#para ejecutar
if __name__ == '__main__':
    app.run(debug=True)
