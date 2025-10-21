import speech_recognition as sr
import os
from pydub import AudioSegment

def transcribe_call(input_folder, output_folder):
    recognizer = sr.Recognizer()

    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith("mp3"):
            continue

        file_path = os.path.join(input_folder, filename)
        print(f"Processing {filename}")

        if not filename.lower().endswith("wav"):
            sound = AudioSegment.from_file(file_path)
            wav_path = os.path.join(input_folder, 'temp.wav')
            sound.export(wav_path, format="wav")
            file_path = wav_path

        with sr.AudioFile(file_path) as source:
            audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data, language='uk-UA')
            print(f"Transcribed succesfully")

            output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_file, 'w') as f:
                f.write(text)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

if __name__ == "__main__":
    transcribe_call('audio/calls', 'audio/calls_transcribed')
