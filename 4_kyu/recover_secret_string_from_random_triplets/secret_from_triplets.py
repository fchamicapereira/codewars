# https://www.codewars.com/kata/53f40dff5f9d31b813000774

import string

def recoverSecret(triplets):
    letters = dict()

    class Letter:
        def __init__(self, l):
            self.l = l
            self.next_letters = {}

        def has(self, l):
            return l in self.next_letters

        def has_next(self, l):
            if l in self.next_letters:
                return True

            for nl in self.next_letters.values():
                if nl.has_next(l):
                    return True
            return False

        def next(self, l):
            if not self.has_next(l):
                self.next_letters[l] = letters[l]

        def unroll(self):
            base = self.l
            possibilities = []
            stored = []
            m = -1

            for nlk, nlv in self.next_letters.items():
                for p in nlv.unroll():
                    s = "{}{}".format(base, p)
                    possibilities.append(s)

                    if len(s) > m:
                        m = len(s)

            if len(possibilities) == 0:
                return [base]

            return [p for p in possibilities if len(p) == m]

    for t in triplets:
        for tt in t:
            if tt not in letters:
                letters[tt] = Letter(tt)

        letters[t[0]].next(t[1])
        letters[t[0]].next(t[2])
        letters[t[1]].next(t[2])

    has = False
    for lk, lv in letters.items():
        for llk, llv in letters.items():
            if llv.has(lk):
                has = True
                break

        if has:
            has = False
            continue
        
        return lv.unroll()[0]
