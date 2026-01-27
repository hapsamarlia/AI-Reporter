from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from pydub import AudioSegment
import speech_recognition as sr
import ollama

app = Flask(__name__)
CORS(app)

# ✅ Set up FFmpeg path manually
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffmpeg = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"

# Folder to save uploaded files
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# 🎙️ Function: Convert + Transcribe Audio
def transcribe_audio(audio_path):
    print("🎧 Converting audio to WAV using FFmpeg...")
    wav_path = os.path.splitext(audio_path)[0] + ".wav"
    AudioSegment.from_file(audio_path).export(wav_path, format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
            clean_text = text.strip()
            print("🗣️ Transcription:", clean_text)
            return clean_text

        except sr.UnknownValueError:
            return "Could not understand the audio clearly."

        except sr.RequestError as e:
            return f"Speech Recognition error: {e}"


# 🧠 Function: Generate AI Report (MAX 5 LINES)
def generate_report(transcription):
    print("🧠 Generating business report with LLaMA...")

    prompt = f"""
Summarize the following transcript into a maximum of 5 short lines.
Only include key business insights.
Do NOT exceed 5 lines.
Keep it clear, professional, and concise.

Transcript:
{transcription}
"""

    try:
        response = ollama.chat(
            model="llama3.2:1b",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response["message"]["content"].strip()

        # HARD LIMIT: Max 5 lines
        lines = result.split("\n")[:5]
        final_result = "\n".join(lines)

        print("📊 Report:", final_result)
        return final_result

    except Exception as e:
        return f"Error generating report: {e}"


# 🌍 Function: Translate report to French (MAX 5 LINES)
def translate_text(text, lang="fr"):
    print("🌍 Translating report to French...")

    prompt = f"""
Translate the following text into French.
Limit output to a maximum of 5 short lines.
Keep it clear and concise.

Text:
{text}
"""

    try:
        response = ollama.chat(
            model="llama3.2:1b",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response["message"]["content"].strip()

        # HARD LIMIT: Max 5 lines
        lines = result.split("\n")[:5]
        final_result = "\n".join(lines)

        print("✅ Translated Report:", final_result)
        return final_result

    except Exception as e:
        return f"Error translating text: {e}"


# 🚀 Route: Handle audio upload + full processing
@app.route("/analyze_audio", methods=["POST"])
def analyze_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    print(f"\n📁 Received file: {file.filename}")
    print("------------------------------------------")

    # Step 1: Transcription
    transcription = transcribe_audio(file_path)

    # Step 2: AI Business Report (5 lines max)
    report = generate_report(transcription)

    # Step 3: Translation (5 lines max)
    translated = translate_text(report, "fr")

    print("------------------------------------------")
    print("✅ Process completed.\n")

    return jsonify({
        "transcription": transcription,
        "report": report,
        "translated_report": translated
    })


@app.route("/")
def home():
    return "🚀 AI Reporter Backend Running Successfully!"


if __name__ == "__main__":
    app.run(debug=True)
