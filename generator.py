from random import choice
from sys import argv

filename = 'input/random'

nucleotides = ['A', 'C', 'G', 'T']

n = int(argv[1])
k = int(argv[2])
errorPercentage = int(argv[3])/100

sequence = ''
spectrum = []

for i in range(n):
    sequence += choice(nucleotides)
    if i >= k - 1:
        temp = sequence[i - k + 1:i + 1]
        if temp not in spectrum:
            spectrum.append(temp)

start = spectrum[0]
spectrum.sort()

perfectLength = n - k + 1
errorNumber = int(errorPercentage * perfectLength)
bonus = perfectLength - len(spectrum)

for i in range(errorNumber):
    if not bonus:
        spectrum.remove(choice(spectrum))
    else:
        bonus -= 1
    temp = ''
    for i in range(k):
        temp += choice(nucleotides)
    spectrum.append(temp)

with open(filename, 'w') as file:
    file.write(start)
    file.write('\n')
    file.write(str(n))
    for i in spectrum:
        file.write('\n')
        file.write(i)

with open(filename + '.seq', 'w') as file:
    file.write(sequence)