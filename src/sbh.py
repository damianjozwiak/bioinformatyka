import sys
import Levenshtein

DEBUG = False

fullSequence = ''
# start = ''
# n = 0
# spectrum = []

def init(argv):
    global fullSequence #, start, n, spectrum

    if len(argv) != 2:
        sys.exit("Usage: python3 " + argv[0] + " [filename]")
    filename = argv[1]

    file = open(filename, "r")

    start = file.readline().rstrip()
    n = int(file.readline().rstrip())
    spectrum = [line.rstrip() for line in file]

    with open(filename + ".seq", "r") as seqFile:
        fullSequence = str(seqFile.read()).rstrip()

    file.close()
    seqFile.close()
    return n, start, spectrum


def calcDistance(a, b, x):
    if a[x:] == b[:len(b)-x]:
        return x
    return calcDistance(a, b, x+1)


def generateMatrix(spectrum):
    return [[calcDistance(i, j, 0) for j in spectrum] for i in spectrum]


def findMin(array):
    minval = len(fullSequence)

    for i in array:
        if i < minval and i != 0:
            minval = i

    return minval


def getAns(sol):

    ans = ''

    for i in range(len(sol)):
        if len(ans) == 0:
            ans += sol[i]
        else:
            addition = calcDistance(sol[i - 1], sol[i], 0)
            ans += sol[i][:-1*addition]

    return ans


def greedy(n, start, spectrum):

    last = start
    length = len(last)
    trashSet = spectrum[:]
    solution = [last]

    m = generateMatrix(spectrum)

    while True:
        iLast = spectrum.index(last)
        ar = [m[iLast][spectrum.index(o)] for o in trashSet]

        for i in range(len(ar)):
            x = trashSet[i]
            if x != spectrum[iLast]:
                ar[i] += findMin(m[spectrum.index(x)])

        temp = ar.index(findMin(ar))
        index = spectrum.index(trashSet[temp])
        addition = m[iLast][index]

        if length + addition > n:
            break
        length += addition

        last = spectrum[index]
        solution.append(last)
        trashSet.remove(last)
        # ans += last[:-1*addition]

    return solution


def globalCrit(sol):
    return len(sol)


def condensation(sol):
    return len(sol)/len(getAns(sol))


def tabuSearch():
    pass

if __name__ == "__main__":
    
    n, start, spectrum = init(sys.argv)
    solution = greedy(n, start, spectrum)

    # print(Levenshtein.ratio(sequence, fullSequence))