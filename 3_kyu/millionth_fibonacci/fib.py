# https://www.codewars.com/kata/53d40c1e2f13e331fc000c26

def fib(n):
    def m_mul(m1, m2):
        if len(m2[0]) == 1:
            return [
                [m1[0][0] * m2[0][0] + m1[0][1] * m2[1][0]],
                [m1[1][0] * m2[0][0] + m1[1][1] * m2[1][0]],
            ]

        return [
            [m1[0][0] * m2[0][0] + m1[0][1] * m2[1][0], m1[0][0] * m2[0][1] + m1[0][1] * m2[1][1]],
            [m1[1][0] * m2[0][0] + m1[1][1] * m2[1][0], m1[1][0] * m2[0][1] + m1[1][1] * m2[1][1]]
        ]

    def m_pow(m1, p):
        if p == 0:
            return [[0, 0], [0, 0]]

        if p == 1:
            return m1

        if p % 2 == 0:
            half = m_pow(m1, p / 2)
            return m_mul(half, half)

        return m_mul(m1, m_pow(m1, p - 1))

    m1 = [[0, 1], [1, 1]]
    f0 = [[0], [1]]

    if n == 0: return f0[0][0]
    if abs(n) == 1: return f0[1][0]

    fn = m_mul(m_pow(m1, abs(n) - 1), f0)[1][0]
    return fn if n > 0 or n % 2 != 0 else -fn