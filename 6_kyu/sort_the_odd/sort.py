# https://www.codewars.com/kata/578aa45ee9fd15ff4600090d/python

def sort_array(source_array):
    odd = sorted([n for n in source_array if n % 2 != 0])

    odd_i = 0
    for source_i in range(len(source_array)):
        if source_array[source_i] % 2 != 0:
            source_array[source_i] = odd[odd_i]
            odd_i += 1

    return source_array
