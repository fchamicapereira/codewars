# https://www.codewars.com/kata/58c5577d61aefcf3ff000081/python

def encode_rail_fence_cipher(m, r):
    def encode_arr(arr, r):
        rails = [[] for i in range(r)]
        rail = 0
        up = True
        for c in arr:
            rails[rail].append(c)
            rail = rail + 1 if up else rail - 1
            if rail == 0 or rail == r - 1:
                up = not up
        
        return [ c for subrail in rails for c in subrail ]
    
    if isinstance(m, list):
        return encode_arr(m, r)

    return "".join(encode_arr([c for c in m], r))

def decode_rail_fence_cipher(c, r):
    m = [""] * len(c)
    map = encode_rail_fence_cipher([ i for i in range(len(c)) ], r)
    for index, letter in zip(map, c):
        m[index] = letter
    return "".join(m)