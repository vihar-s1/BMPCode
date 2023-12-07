def inv_mod(a, b):
    pass

def add(P, Q, A, B, p):
    if P == 0: return Q
    if Q == 0: return P
    if P[0] == Q[0] and P[1] != Q[1]: return 0
    
    if P[0] != Q[0]:
        rise = (P[1] - Q[1]) % p
        run = (P[0] - Q[0]) % p
    else:
        if P[1] == 0: return 0  # added this line
        rise = (3 * P[0] * P[0] + A) % p
        run = (2 * P[1]) % p
    slope = (rise * inv_mod(run, p)) % p
    y_int = (P[1] - P[0] * slope) % p
    x = (slope * slope - P[0] - Q[0]) % p
    y = (-(slope * x + y_int)) % p
    return (x, y)
