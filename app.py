import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import speech_recognition as sr
from deep_translator import GoogleTranslator
from monsterapi import client

# Load API key
load_dotenv()
MONSTER_API_KEY = os.getenv("MONSTER_API_KEY")

# Flask app
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

# Initialize tools
recognizer = sr.Recognizer()
monster_client = client(MONSTER_API_KEY)


@app.route("/", methods=["GET", "POST"])
def index():
    generated_image = None
    recognized_text = ""
    translated_text = ""

    if request.method == "POST":
        audio_file = request.files.get("audio")

        if audio_file:
            # Save uploaded audio file
            audio_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
            audio_file.save(audio_path)

            try:
                # Convert speech to text
                with sr.AudioFile(audio_path) as source:
                    audio = recognizer.record(source)

                # Hindi speech recognition
                recognized_text = recognizer.recognize_google(
                    audio,
                    language="hi-IN"
                )

                print("Recognized Text:", recognized_text)

                # Translate Hindi text to English
                translated_text = GoogleTranslator(
                    source="auto",
                    target="en"
                ).translate(recognized_text)

                print("Translated Text:", translated_text)

                # Generate image using MonsterAPI
                response = monster_client.generate(
                    model="txt2img",
                    data={
                        "prompt": translated_text,
                        "negprompt": "blurry, low quality",
                        "samples": 1,
                        "steps": 30
                    }
                )

                generated_image = response["output"][0]

            except Exception as e:
                print("Error:", e)

    return render_template(
        "index.html",
        generated_image=generated_image,
        recognized_text=recognized_text,
        translated_text=translated_text
    )


if __name__ == "__main__":
    app.run(debug=True)