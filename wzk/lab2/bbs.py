from random import getrandbits, randrange
from sys import argv
from sympy import nextprime


def isPrime(n):
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    if n < 9:
        return True
    if n % 3 == 0:
        return False
    r = int(n**0.5)
    f = 5
    while f <= r:
        if n % f == 0:
            return False
        if n % (f+2) == 0:
            return False
        f += 6
    return True


def isGoodPrime(p):
    return p % 4 == 3


def findGoodPrime(bits=512):
    candidate = 1
    while not isGoodPrime(candidate):
        candidate = nextprime(getrandbits(bits))
    print("p =", candidate)
    return candidate


def getBlumNumber():
    return findGoodPrime() * findGoodPrime()


def gcd(p, q):
    while q != 0:
        p, q = q, p % q
    return p


def isCoprime(x, y):
    return gcd(x, y) == 1


def getInitialX(N):
    x = randrange(2, N)
    while not isCoprime(x, N):
        x = randrange(2, N)
    return x


def getNewX(x, n):
    return x**2 % n


def generate(length):
    n = getBlumNumber()
    x = getInitialX(n)
    print('N =', n)
    print('x =', x)
    result = ''
    for _ in range(length):
        x = getNewX(x, n)
        result += bin(x)[-1]

    return result


def monoBitTest(sequence):
    return True if 9725 < sum(int(x) for x in sequence) < 10275 else False


def intervalCheck(runs):
    if not (2315 <= runs[0] <= 2685):
        return False
    if not (1114 <= runs[1] <= 1386):
        return False
    if not (527 <= runs[2] <= 723):
        return False
    if not (240 <= runs[3] <= 384):
        return False
    if not (103 <= runs[4] <= 209):
        return False
    if not (103 <= runs[5] <= 209):
        return False
    return True


def runsTest(sequence):
    ref = sequence[0]
    length = 0
    zeroRuns = [0, 0, 0, 0, 0, 0]
    oneRuns = [0, 0, 0, 0, 0, 0]
    seq = ''
    for x in sequence:
        if x == ref:
            length += 1
            seq += x
        else:
            if length < 6:
                if ref == '1':
                    oneRuns[length - 1] += 1
                elif ref == '0':
                    zeroRuns[length - 1] += 1
            else:
                if ref == '1':
                    oneRuns[5] += 1
                elif ref == '0':
                    zeroRuns[5] += 1
            ref = x
            length = 1

    return intervalCheck(oneRuns) and intervalCheck(zeroRuns)


def longRunsTest(sequence):
    ref = sequence[0]
    length = 0
    maxLength = 0
    for x in sequence:
        if x == ref:
            length += 1
        else:
            if length > maxLength:
                maxLength = length
                if maxLength >= 26:
                    return False
            ref = x
            length = 1

    return True


def pokerTest(sequence):
    count = ['{0:04b}'.format(i) for i in range(16)]
    values = [sequence[i:i+4] for i in range(5000)]
    for i in range(len(count)):
        count[i] = values.count(count[i])

    sum = 0
    for i in range(len(count)):
        sum += count[i]**2
    sum *= (16/5000)
    sum -= 5000
    return True if 2.16 < sum < 46.17 else False


def testResult(val):
    return 'PASSED' if val else 'NOT PASSED'


if __name__ == "__main__":
    length = int(argv[1])
    sequence = generate(length)
    if sequence:
        print("Sequence of length {} generated.".format(length))
    print('Monobit test:\t', testResult(monoBitTest(sequence)))
    print('Runs test:\t', testResult(runsTest(sequence)))
    print('Long runs test:\t', testResult(longRunsTest(sequence)))
    print('Poker test:\t', testResult(pokerTest(sequence)))
