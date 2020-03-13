# https://www.codewars.com/kata/521c2db8ddc89b9b7a0000c1/python

def snail(snail_map):
    snailed = []
    
    while len(snail_map) > 0:
    
        # top
        snailed = snailed + snail_map.pop(0)
        
        if len(snail_map) == 0:
            return snailed

        # right
        for arr in snail_map:
            snailed.append(arr.pop())
            
        # bottom
        snailed = snailed + snail_map.pop()[::-1]
        
        if len(snail_map) == 0:
            return snailed
        
        # left
        for i in range(len(snail_map) - 1, -1, -1):
            snailed.append(snail_map[i].pop(0))
