import os
import speech_recognition as sr
from pydub import AudioSegment

# ✅ Force pydub to use the correct ffmpeg.exe path
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffmpeg = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"

def transcribe_audio(audio_path):
    # Convert MP3 → WAV if needed
    if audio_path.endswith(".mp3"):
        print("🎧 Converting MP3 to WAV using FFmpeg...")
        sound = AudioSegment.from_mp3(audio_path)
        wav_path = audio_path.replace(".mp3", ".wav")
        sound.export(wav_path, format="wav")
        audio_path = wav_path

    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data)
            print("🗣️ Transcription:", text)
            return text
        except sr.UnknownValueError:
            return "Could not understand the audio clearly."
        except sr.RequestError as e:
            return f"Speech Recognition error: {e}"
