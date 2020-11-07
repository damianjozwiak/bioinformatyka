import sys
import Levenshtein

DEBUG = False

fullSequence = ''
tabu = []
# start = ''
# n = 0
# spectrum = []


def init(argv):
    global fullSequence  # , start, n, spectrum

    if len(argv) != 2:
        sys.exit("Usage: python3 " + argv[0] + " FILENAME")
    filename = argv[1]

    # print(filename)

    with open(filename, "r") as file:
        start = file.readline().rstrip()
        n = int(file.readline().rstrip())
        spectrum = [line.rstrip() for line in file]

    with open(filename + ".seq", "r") as seqFile:
        fullSequence = str(seqFile.read()).strip()
        # print(fullSequence)

    return n, start, spectrum


def calcDifference(stringA, stringB, difference):
    if stringA[difference:] == stringB[:len(stringB) - difference]:
        return difference
    return calcDifference(stringA, stringB, difference + 1)


def generateMatrix(spectrum):
    return [[calcDifference(i, j, 0) for j in spectrum] for i in spectrum]


def findMin(array):
    minval = len(fullSequence)

    for element in array:
        if element < minval and element > 0:
            minval = element

    return minval


def findMax(array):
    maxval = 0

    for element in array:
        if element > maxval:
            maxval = element

    return maxval


def getSequence(solution):

    sequence = ''

    for i in range(len(solution)):
        if not sequence:
            sequence += solution[i]
        else:
            addition = calcDifference(solution[i - 1], solution[i], 0)
            sequence += solution[i][-1*addition:]

    return sequence


def getLength(solution):

    length = 0
    for i in range(len(solution)):
        if not length:
            length += len(solution[i])
        else:
            length += calcDifference(solution[i-1], solution[i], 0)

    return length


def greedy(n, start, spectrum):

    last = start
    length = len(last)
    trashSet = spectrum[:]
    solution = [last]

    if DEBUG:
        print("Generating matrix...")

    m = generateMatrix(spectrum)

    if DEBUG:
        print("Generated.")
        print("Start: ", last)

    while True:
        indexLast = spectrum.index(last)
        ar = [m[indexLast][spectrum.index(o)] for o in trashSet]

        for i in range(len(ar)):
            x = trashSet[i]
            if x != spectrum[indexLast]:
                ar[i] += findMin(m[spectrum.index(x)])

        temp = ar.index(findMin(ar))
        index = spectrum.index(trashSet[temp])
        addition = m[indexLast][index]

        if length + addition > n:
            break

        last = spectrum[index]
        
        solution.append(last)
        length += addition

        trashSet.remove(last)

        if DEBUG:
            print("Added", last)
        # ans += last[:-1*addition]

    if DEBUG:
        for el in solution:
            temp = solution.count(el)
            if temp > 1:
                print("Warning:", el,
                      "is in solution more than once ({})".format(temp))
        print(len(solution), "oligonucleotides in the solution")

    return solution


def getGlobalCriterionValue(solution):
    return len(solution)


def getCondensationValue(solution):
    return len(solution)/getLength(solution)

# def condensationStep(solution, condensation):
def condensationStep(solution):

    condensation = getCondensationValue(solution)
    condensationValues = []

    for oligonucleotide in solution:
        newSolution = solution[:]
        newSolution.remove(oligonucleotide)
        condensationValues.append(getCondensationValue(newSolution))

    maxval = findMax(condensationValues)
    # if DEBUG:
    print("Condensation:", condensation, "\nMaxVal:", maxval)
    if maxval >= condensation:
        tabu.append(solution.pop(condensationValues.index(maxval)))
    else:
        return ''

    return solution


def extensionStep(solution):
    pass


def tabuSearch(solution):

    newSol = solution
    # condensation = getCondensationValue(solution)

    while True:
        # testSol = condensationStep(newSol, condensation)
        testSol = condensationStep(newSol)
        if not testSol:
            break
        newSol = testSol

    if DEBUG and tabu:
        print("TABU LIST:", tabu)

    solution = newSol
    # globalCrit = getGlobalCriterionValue(solution)

    return solution

if __name__ == "__main__":

    n, start, spectrum = init(sys.argv)
    solution = greedy(n, start, spectrum)
    # tabuSearch(solution)

    print(Levenshtein.ratio(getSequence(solution), fullSequence))