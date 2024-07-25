import os

from func_for_text import read_text, similar


if len(os.listdir('text')) != 0 and len(os.listdir('transcribed_text')) != 0:
    path_file = f"text/{os.listdir('text')[0]}"
    check_text = read_text("text/axolotls.txt")
    print(check_text)
    new_text = read_text("transcribed_text/transcribed_text.txt")
    print(new_text)
    similarity = similar(check_text, new_text)
    print(str(round((similarity * 100), 2)) + "%")
