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

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# 🎙️ Convert + Transcribe Audio
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


# 🧠 Generate AI Report
def generate_report(transcription):
    print("🧠 Generating business report with LLaMA...")

    prompt = f"""
Summarize the following transcript into a maximum of 5 short lines.
Only include key business insights.
Do NOT exceed 5 lines.

Transcript:
{transcription}
"""

    try:
        response = ollama.chat(
            model="llama3.2:1b",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response["message"]["content"].strip()
        lines = result.split("\n")[:5]
        final_result = "\n".join(lines)

        print("📊 Report:", final_result)
        return final_result

    except Exception as e:
        return f"Error generating report: {e}"


# 🌍 Translate Report (Dynamic Language)
def translate_text(text, lang="French"):
    print(f"🌍 Translating report to {lang}...")

    prompt = f"""
Translate the following text into {lang}.
Return ONLY the translated text.
Maximum 5 short lines.

Text:
{text}
"""

    try:
        response = ollama.chat(
            model="llama3.2:1b",
            messages=[{"role": "user", "content": prompt}]
        )

        result = response["message"]["content"].strip()

        lines = result.split("\n")[:5]
        final_result = "\n".join(lines)

        print("✅ Translated Report:", final_result)
        return final_result

    except Exception as e:
        return f"Error translating text: {e}"


# 🚀 Main API
@app.route("/analyze_audio", methods=["POST"])
def analyze_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # ✅ Get language selected by user
    language = request.form.get("language", "French")

    print(f"\n📁 Received file: {file.filename}")
    print(f"🌍 Selected Language: {language}")
    print("------------------------------------------")

    # Step 1: Transcription
    transcription = transcribe_audio(file_path)

    # Step 2: Generate Report
    report = generate_report(transcription)

    # Step 3: Translate Report
    translated = translate_text(report, language)

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