# https://www.codewars.com/kata/551dc350bf4e526099000ae5/python

import re

def song_decoder(song):
    return re.sub('(WUB)+', ' ', song).strip()
