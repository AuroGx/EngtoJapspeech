import pyaudio
import wave
import whisper
import requests
from pydub import AudioSegment
from pydub.playback import play
from googletrans import Translator


def record_audio():

    # Set the recording parameters
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    OUTPUT_AUDIO = "output_audio.wav"

    # Create the PyAudio object
    audio = pyaudio.PyAudio()

    # Open the microphone stream
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording... for 5 Sec")

    # Record the audio
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    # Close the stream and PyAudio object
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the audio to a file using wave
    wf = wave.open(OUTPUT_AUDIO, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    #returning "output_audio.wav"
    return OUTPUT_AUDIO


def speech_to_text(audio_name):

    #loads whisper model, there's tiny,base,small,medium,large
    model = whisper.load_model('base')
    print("model loaded, transcribing...")
    result = model.transcribe(audio_name, fp16 = False)
    print(result["text"])
    return result["text"]


def text_to_syn(text):
    speaker_id = 1 # changable to other speaker ID

    # finding the API URL
    apiurl = "https://api.tts.quest/v1/voicevox/"
    vvurl = f"{apiurl}?text={text}&speaker={speaker_id}"

    # sending a post request to the API and returning a json
    print(f"sending post request to: {vvurl}")
    response = requests.request("POST", vvurl)
    print(f"response: {response}")
    response_json = response.json()

    #getting the exact thing you want from response_json
    try:
        wav_url = response_json['wavDownloadUrl']
    except:
        print("failed to get wav download link")
        print(response_json)
        return
    
    print(f"Downloading wav responese from {vvurl}")
    wav_bytes =  requests.get(wav_url).content

    #print(wav_bytes)


    filename = "voice_output.wav"

    # writing the wav bytes into the file
    try:
        with open(filename, "wb") as file:
            file.write(wav_bytes)
    except:
        print("failed to write to wav file")
    
    return filename


def main():
    
    # record speech and getting the file name in a string
    audio_name = record_audio()

    # Convert speech to text (output_audio.wav)
    english_text = speech_to_text('output_audio.wav')
    print("speech to text done")

    # Translate English to Japanese with googletrans
    translator = Translator()
    translated = translator.translate(english_text, dest='ja').text

    # init the voicevox
    filename = text_to_syn(translated)
    
    try:
        # Play the audio
        voiceLine = AudioSegment.from_wav(filename)
        play(voiceLine)
    except:
        print("api probably not working. try again")

if __name__=="__main__":
    main()