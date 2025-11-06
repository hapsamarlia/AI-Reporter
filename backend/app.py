from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from pydub import AudioSegment
import speech_recognition as sr
import subprocess
import ollama  # for llama model response generation

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
    print("🎧 Converting MP3 to WAV using FFmpeg...")
    wav_path = os.path.splitext(audio_path)[0] + ".wav"
    AudioSegment.from_file(audio_path).export(wav_path, format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            print("🗣️ Transcription:", text)
            return text
        except sr.UnknownValueError:
            print("⚠️ Speech not clear.")
            return "Could not understand the audio clearly."
        except sr.RequestError as e:
            print("⚠️ Speech Recognition error:", e)
            return f"Speech Recognition error: {e}"


# 🧠 Function: Generate AI Report using LLaMA (Ollama)
def generate_report(transcription):
    print("🧠 Generating business report with LLaMA...")
    try:
        response = ollama.chat(model="llama3.2:1b", messages=[
            {"role": "user", "content": f"Create a short business analysis report for: {transcription}"}
        ])
        result = response["message"]["content"]
        print("📊 Report:", result)
        return result
    except Exception as e:
        print("⚠️ LLaMA error:", e)
        return f"Error generating report: {e}"


# 🌍 Function: Translate report to French (Offline fallback)
def translate_text(text, lang="fr"):
    print("🌍 Translating report to French...")
    try:
        # simple offline translation fallback using ollama
        response = ollama.chat(model="llama3.2:1b", messages=[
            {"role": "user", "content": f"Translate this text to French:\n{text}"}
        ])
        result = response["message"]["content"]
        print("✅ Translated Report:", result)
        return result
    except Exception as e:
        print("⚠️ Translation error:", e)
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
    # Step 2: Report Generation
    report = generate_report(transcription)
    # Step 3: Translation
    translated = translate_text(report, "fr")

    print("------------------------------------------")
    print("✅ Process completed.\n")

    return jsonify({
        "transcription": transcription,
        "report": report,
        "translated_report": translated
    })


if __name__ == "__main__":
    app.run(debug=True)
