# https://www.codewars.com/kata/54b724efac3d5402db00065e/python

def decodeMorse(morse_code):
    # ToDo: Accept dots, dashes and spaces, return human-readable message
    decoded_words = []
    word = ''
    for w in morse_code.split(' '):
        if w == '':
            if len(word) > 0:
                decoded_words.append(word)
                word = ''
            continue
        word += MORSE_CODE[w]
    if len(word) > 0:
        decoded_words.append(word)
    return ' '.join(decoded_words)
