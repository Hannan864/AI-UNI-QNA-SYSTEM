try:
    import sounddevice as sd
except ImportError:
    sd = None
try:
    import numpy as np
except ImportError:
    np = None
try:
    import wave
except ImportError:
    wave = None
import tempfile
import os
try:
    import speech_recognition as sr
except ImportError:
    sr = None

class SpeechToText:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
        self.recognizer = sr.Recognizer()

    def record_audio(self, duration=5):
        """Record audio from microphone for a specific duration"""
        print(f"🎤 Listening... Speak now ({duration} seconds)")
        try:
            # Record audio data
            audio_data = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=1, dtype='int16')
            sd.wait() # Wait until recording is finished
            return audio_data
        except Exception as e:
            print(f"Error recording audio: {e}")
            return None

    def save_audio_to_wav(self, audio_data, filename):
        """Save numpy audio data to a WAV file"""
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_data.tobytes())

    def listen_and_transcribe(self, duration=5):
        """Main function to record and transcribe"""
        audio_data = self.record_audio(duration)
        
        if audio_data is None:
            return "Error: Could not access microphone."

        # Create a temporary WAV file
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            self.save_audio_to_wav(audio_data, temp_path)
            
            # Transcribe using Google Speech Recognition
            with sr.AudioFile(temp_path) as source:
                audio = self.recognizer.record(source)
            
            text = self.recognizer.recognize_google(audio, language='en-US')
            return text
        
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            return f"Could not request results; {e}"
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def transcribe_audio_file(self, file_path):
        """Transcribe an audio file to text"""
        try:
            with sr.AudioFile(file_path) as source:
                audio = self.recognizer.record(source)
            text = self.recognizer.recognize_google(audio, language='en-US')
            return text
        except sr.UnknownValueError:
            return "Sorry, I could not understand the audio."
        except sr.RequestError as e:
            return f"Could not request results; {e}"
        except Exception as e:
            return f"Error transcribing audio: {e}"