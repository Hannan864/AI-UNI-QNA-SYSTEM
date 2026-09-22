from gtts import gTTS
import os
import tempfile

class TextToSpeech:
    def __init__(self):
        self.language = 'en'
        self.slow = False
    
    def text_to_speech(self, text, output_file=None):
        """Convert text to speech and save to file"""
        try:
            tts = gTTS(text=text, lang=self.language, slow=self.slow)
            
            if output_file is None:
                # Create temporary file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                output_file = temp_file.name
                temp_file.close()
            
            tts.save(output_file)
            return output_file
        
        except Exception as e:
            print(f"Error in text-to-speech: {str(e)}")
            return None
    
    def speak_text(self, text):
        """Convert text to speech and return file path"""
        return self.text_to_speech(text)