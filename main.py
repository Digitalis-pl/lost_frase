from func_for_text import write_text
from func_for_audio import (find_long_silences, m4a_to_wav,
                            delete_noise, audio_to_text_with_vosk,
                            get_file)


'''Обработка файла приведение к wav и очистка от шумов'''
m4a_to_wav(get_file())
path_wav_audio = "wav_audio/wav_audio.wav"
clean_audio = delete_noise(path_wav_audio)
'''Ищем чрезмерно длинные паузы во время речи'''
pauses = find_long_silences(clean_audio)
'''Переводим аудио в текст и запись в отдельный файл'''
transcribed_text = audio_to_text_with_vosk(clean_audio)
write_text(transcribed_text)

print(pauses)
print(transcribed_text)
