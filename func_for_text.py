from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def read_text(file):
    with open(file, 'r', encoding='utf-8') as f:
        our_str = f.read().replace('\n', ' ')
    return our_str


def write_text(value):
    with open('transcribed_text/transcribed_text.txt', 'w', encoding='utf-8') as f:
        f.write(value)
