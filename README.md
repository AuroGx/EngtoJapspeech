## Speech to Japanese Audio Converter
This Python code is used to convert speech in English to Japanese audio. The program uses PyAudio to record audio from the microphone and saves it to a WAV file. It then uses Whisper AI to transcribe the audio into text. The text is then translated to Japanese using the Google Translate API. Finally, the program uses the Voicevox API to generate a Japanese audio file and play it back using PyDub.

# Requirements
* Python 3.x
* PyAudio
* Whisper
* requests
* PyDub
* googletrans

# Usage
To use this program, simply run the main() function. The program will record 5 seconds of audio from your microphone and save it to a file called output_audio.wav. The audio will then be transcribed to text using Whisper AI and translated to Japanese using the Google Translate API. The Japanese audio will be saved to a file called voice_output.wav and played back using PyDub.
