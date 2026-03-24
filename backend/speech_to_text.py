import os
import speech_recognition as sr
from pydub import AudioSegment

# ✅ Set FFmpeg path
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffmpeg = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"

def transcribe_audio(audio_path):
    # Convert MP3 → WAV if neededca
    if audio_path.endswith(".mp3"):
        print("🎧 Converting MP3 to WAV using FFmpeg...")
        sound = AudioSegment.from_mp3(audio_path)
        wav_path = audio_path.replace(".mp3", ".wav")
        sound.export(wav_path, format="wav")
        audio_path = wav_path

    r = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        r.adjust_for_ambient_noise(source)  # Improve accuracy
        audio_data = r.record(source)

        try:
            text = r.recognize_google(audio_data)
            clean_text = text.strip()

            print("🗣️ Transcription:", clean_text)
            return clean_text

        except sr.UnknownValueError:
            return "Audio unclear. Please upload a clearer recording."

        except sr.RequestError as e:
            return f"Speech Recognition API error: {e}"
