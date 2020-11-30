from random import choice
from sys import argv

dirname = 'input/'

nucleotides = ['A', 'C', 'G', 'T']

# n = int(argv[1])
# k = int(argv[2])
# errorPercentage = int(argv[3])/100

def init():
    for n in range(300, 1001, 100):
        for k in range(8,11):
            for i in range(1, 31):
                start, spectrum, sequence = generate(n,k)
                filename = dirname + 'rand-' + str(n) + '-' + str(k) + '-' + str(i)
                with open(filename, 'w') as file:
                    file.write(start)
                    file.write('\n')
                    file.write(str(n))
                    for i in spectrum:
                        file.write('\n')
                        file.write(i)

                with open(filename + '.seq', 'w') as file:
                    file.write(sequence)
                

def generate(n, k, errorPercentage = 0.05):
    sequence = ''
    spectrum = []

    for i in range(n):
        sequence += choice(nucleotides)
        if i >= k - 1:
            temp = sequence[i - k + 1:i + 1]
            if temp not in spectrum:
                spectrum.append(temp)

    start = spectrum[0]

    perfectLength = n - k + 1
    errorNumber = int(errorPercentage * perfectLength)
    bonus = perfectLength - len(spectrum)

    for i in range(errorNumber):
        if not bonus:
            spectrum.remove(choice(spectrum[1:]))
        else:
            bonus -= 1
        temp = ''
        for i in range(k):
            temp += choice(nucleotides)
        spectrum.append(temp)
    
    spectrum.sort()

    return start, spectrum, sequence

init()