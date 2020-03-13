# https://www.codewars.com/kata/52b7ed099cdc285c300001cd/python

def sum_of_intervals(intervals):
    joined = []
    modified = False
    
    for i in intervals:   
        done = False
        for idx, j in enumerate(joined):
            if j[0] <= i[0] <= i[1] <= j[1]:
                done = True
                break
            
            if i[0] < i[1] < j[0] or j[1] < i[0] < i[1]:
                continue
            
            joined[idx] = (min(i[0], j[0]), max(i[1], j[1]))
            modified = True
            done = True
            break
        
        if done:
            continue
        
        joined.append(i)
    
    if not modified:
        return sum([j[1] - j[0] for j in joined])

    return sum_of_intervals(joined)
