from sys import argv, exit
from random import randrange, sample, choice

global fieldSize
fieldSize = 10**5

def isPrime(n):
    if n == 2 or n == 3: return True
    if n < 2 or n%2 == 0: return False
    if n < 9: return True
    if n%3 == 0: return False
    r = int(n**0.5) 
    f = 5
    while f <= r:
        if n % f == 0: return False
        if n % (f+2) == 0: return False
        f += 6
    return True

def polynomial(x, coeffs):
    return sum([coeffs[i] * x**(len(coeffs) - i - 1) for i in range(len(coeffs))])

def init(argv):
    
    msg = "Usage: python3 " + argv[0] + " <secret> <number of shares> <minimum number of shares>"

    if len(argv) < 4:
        exit(msg)
    
    secret = int(argv[1])
    n = int(argv[2])
    t = int(argv[3])

    if t > n:
        print("===> ERROR: minimum number of shares should be lower than the actual number of shares\n")
        exit(msg)

    print("Secret:\t\t\t\t", secret)
    print("Number of shares:\t\t", n)
    print("Minimum number of shares:\t", t)

    return secret, n, t

def split(secret, n, t):
    
    # primes = [k for k in range(max(secret, n), fieldSize) if isPrime(k)]
    # p = choice(primes)
    # p = randrange(max(secret, n), fieldSize)
    p = 11

    a = [randrange(1, fieldSize) for _ in range(t - 1)]
    a.append(secret)

    shares = [(i, polynomial(i, a)) for i in range(1, n+1)]

    print("p:\t\t\t\t", p)
    print("Shares:\t\t\t\t", shares)
    return p, shares

def combine(p, shares):
    print("Shares used:\t\t\t", shares)
    
    secret = 0
    for i in range(len(shares)):
        x, y = shares[i][0], shares[i][1]
        li = 1
        for j in range(len(shares)):
            if j != i:
                xj = shares[j][0]
                li *= -1 * xj / (x - xj)
        secret += li * y % p

    secret = int(round(secret % p, 0))
    return secret

if __name__ == "__main__":
    
    secret, n, t = init(argv)
    p, shares = split(secret, n, t)
    
    print("Combined secret:\t\t", combine(p, sample(shares, t)))