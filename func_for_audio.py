from pydub import silence

import numpy as np

import os

from pathlib import Path

import wave

import json

from noisereduce import reduce_noise

from vosk import Model, KaldiRecognizer

from pydub import AudioSegment


def find_long_silences(file, silence_threshold=-40, min_silence_duration=2000):
    all_pauses = []
    audio = AudioSegment.from_wav(file)
    silences = silence.detect_silence(audio, min_silence_len=min_silence_duration, silence_thresh=silence_threshold)
    detected_silences = [(start / 1000.0, end / 1000.0) for start, end in silences]
    for start, end in detected_silences:
        all_pauses.append(f"Длинная пауза с {start:.2f} до {end:.2f} секунд")
    return all_pauses


def m4a_to_wav(file, upload_to='wav_audio/wav_audio.wav'):
    audio = AudioSegment.from_file(file, format="m4a")
    audio.export(upload_to, format="wav")


def delete_noise(first_wav_file_path):
    # Преобразование в numpy массив для последующей обработки шумов
    new_audio = AudioSegment.from_file(first_wav_file_path)
    samples = np.array(new_audio.get_array_of_samples())

    # Пример шума для удаления
    sample_rate = new_audio.frame_rate
    noise_sample = samples[:sample_rate]

    # Подавление шума
    reduced_noise_samples = reduce_noise(y=samples, sr=sample_rate, y_noise=noise_sample, stationary=True)

    # Обратное преобразование и сохранение файла wav
    reduced_noise_audio = AudioSegment(
        reduced_noise_samples.tobytes(),
        frame_rate=sample_rate,
        sample_width=new_audio.sample_width,
        channels=new_audio.channels
    )

    reduced_noise_audio.export("wav_audio/wav_without_noise_audio.wav", format="wav")

    second_wav_file_path = "wav_audio/wav_without_noise_audio.wav"
    return second_wav_file_path


def audio_to_text_with_vosk(file):
    model_path = "model/vosk-model-ru-0.42"
    model = Model(model_path)
    wf = wave.open(file, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())

    transcript = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            transcript += result.get("text", "") + " "

    result = json.loads(rec.FinalResult())
    transcript += result.get("text", "")
    return transcript


def get_file():
    try:
        if len(os.listdir('audio')) == 0:
            print(len(os.listdir('audio')))
            raise FileNotFoundError
        elif Path(os.listdir('audio')[0]).suffix != '.m4a':

            raise TypeError
        elif len(os.listdir('audio')) > 1:
            raise Exception
        else:
            file_path = f"audio/{os.listdir('audio')[0]}"
            return file_path

    except TypeError as e:
        print(e)
        print("Файл должен быть в формате m4a")
        print(Path(os.listdir('audio')[0]).suffix)
    except FileNotFoundError as e:
        print(e)
        print('Нет файлов для обработки')
    except Exception as e:
        print(e)
        print("За раз можно обработать только 1 файл")
