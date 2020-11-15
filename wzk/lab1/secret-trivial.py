from sys import argv, exit
from random import randrange

def split(k, secret, n):
    shares = [randrange(0, k) for _ in range(n - 1)]
    x = secret
    for j in shares:
        x -= j

    shares.append(x % k)

    return shares

def combine(shares, k):
    temp = 0
    for i in shares:
        temp += i
    
    return temp % k

if __name__ == "__main__":
    
    if len(argv) < 4:
        msg = "Usage: python3 " + argv[0] + " <range> <secret> <number of shares>"
        exit(msg)
    
    k = int(argv[1])
    secret = int(argv[2])
    n = int(argv[3])

    if secret >= k:
        exit("Error: secret out of range")
    print("Secret:\t", secret)
    
    shares = split(k, secret, n)
    print("Shares:\t", shares)

    print("Answer:\t", combine(shares, k))