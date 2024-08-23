import speech_recognition as sr
from transformers import pipeline
from pydub import AudioSegment
import os

def audio_to_text(audio_file_path):
    recognizer = sr.Recognizer()
    converted_audio_path = "converted.wav"

    try:
        # Convert the audio file to a format compatible with the recognizer
        print(f"Converting {audio_file_path} to WAV format...")
        audio = AudioSegment.from_file(audio_file_path)
        audio.export(converted_audio_path, format="wav")
        print(f"Conversion to WAV successful: {converted_audio_path}")

        with sr.AudioFile(converted_audio_path) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                print("Audio to text conversion successful.")
                return text
            except sr.UnknownValueError:
                print("Audio is not clear enough to transcribe.")
                return "Audio is not clear enough to transcribe."
            except sr.RequestError:
                print("Speech recognition service is not available.")
                return "Speech recognition service is not available."
    except Exception as e:
        print(f"Error during conversion or transcription: {e}")
        return "Error during conversion or transcription."
    finally:
        # Clean up the converted file if it exists
        if os.path.exists(converted_audio_path):
            os.remove(converted_audio_path)
            print(f"Temporary file {converted_audio_path} deleted.")
        else:
            print(f"Temporary file {converted_audio_path} not found.")

def summarize_text(text):
    summarizer = pipeline("summarization")
    # Adjust max_length based on input length
    max_length = min(150, len(text) // 2)
    summary = summarizer(text, max_length=max_length, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def summarize_audio_file(audio_file_path):
    text = audio_to_text(audio_file_path)
    if text.startswith("Audio is not clear") or text.startswith("Speech recognition service") or text.startswith("Error during conversion"):
        return text
    summary = summarize_text(text)
    return summary
