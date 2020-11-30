import sys
import Levenshtein
import time

DEBUG = False

fullSequence = ''
tabu = []
# trashSet = []
# start = ''
# n = 0
# spectrum = []


def init(argv):
    global fullSequence  # , start, n, spectrum

    if len(argv) != 2:
        sys.exit('Usage: python3 ' + argv[0] + ' FILENAME')
    filename = argv[1]

    # print(filename)

    with open(filename, 'r') as file:
        start = file.readline().rstrip()
        n = int(file.readline().rstrip())
        spectrum = [line.rstrip() for line in file]

    # trashSet = spectrum[:]

    with open(filename + '.seq', 'r') as seqFile:
        fullSequence = str(seqFile.read()).strip()
        # print(fullSequence)

    return n, start, spectrum


def calcDifference(stringA, stringB, difference=0):
    if stringA[difference:] == stringB[:len(stringB) - difference]:
        return difference
    return calcDifference(stringA, stringB, difference + 1)


def generateMatrix(spectrum):
    return [[calcDifference(i, j) for j in spectrum] for i in spectrum]


def findMin(array):
    minval = array[0]

    for element in array:
        if element < minval and element > 0:
            minval = element

    return minval


def findMax(array):
    maxval = array[0]

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
            addition = calcDifference(solution[i - 1], solution[i])
            sequence += solution[i][-1*addition:]

    return sequence


def getLength(solution):

    length = 0
    for i in range(len(solution)):
        if not length:
            length += len(solution[i])
        else:
            length += calcDifference(solution[i-1], solution[i])

    return length


def greedy(n, start, spectrum):
    
    if DEBUG:
        print('Starting greedy...')

    last = start
    length = len(last)
    solution = [last]
    trashSet = spectrum[:]
    trashSet.remove(last)

    if DEBUG:
        print('Generating matrix...')

    m = generateMatrix(spectrum)

    if DEBUG:
        print('Start: ', last)

    while True:
        indexLast = spectrum.index(last)
        ar = [m[indexLast][spectrum.index(o)] for o in trashSet if o not in tabu]

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

        # if DEBUG:
        # print('Added', last)
        # ans += last[:-1*addition]

    if DEBUG:
        for el in solution:
            temp = solution.count(el)
            if temp > 1:
                print('Warning:', el,
                      'is in solution more than once ({})'.format(temp))
        print('There are', len(solution),
              'oligonucleotides in the initial solution')

    return solution


def getGlobalCriterionValue(solution):
    return len(solution)


def getCondensationValue(solution):
    return len(solution)/getLength(solution)


def makeClusters(solution):
    clusters = []
    start = 0

    for i in range(len(solution) - 1):
        if calcDifference(solution[i], solution[i + 1]) == 1:
            continue
        clusters.append((start, i))
        start = i + 1

    clusters.append((start, len(solution) - 1))

    return clusters


def condensationStep(solution, clusters):

    sol = solution[:]
    condensation = getCondensationValue(sol)
    condensationValues = []

    for cluster in clusters:
        tempSol = [
            ont for ont in sol if ont not in sol[cluster[0]:cluster[1] + 1]]
        condensationValues.append(getCondensationValue(tempSol))

    maxval = findMax(condensationValues)

    if maxval >= condensation:
        cluster = clusters[condensationValues.index(maxval)]
        for _ in range(cluster[0], cluster[1] + 1):
            x = sol.pop(cluster[0])
            tabu.append(x)
    else:
        return ''

    return sol


def tabuSearch(solution, n, spectrum):

    globalCrit = getGlobalCriterionValue(solution)

    newSol = solution[:]
    while True:
        clusters = makeClusters(newSol)
        testSol = condensationStep(newSol, clusters)
        if not testSol:
            break
        newSol = testSol

    if not tabu:
        return solution

    feasible = [o for o in spectrum if o not in newSol]
    feasible.append(newSol[-1])

    newSol.extend(greedy(n - getLength(newSol), newSol[-1], feasible))
    # print(len(solution), '\t\t\t', len(newSol))
        
    return solution if globalCrit > getGlobalCriterionValue(newSol) else newSol


if __name__ == '__main__':

    n, first, spectrum = init(sys.argv)
    start = time.time()
    initialSolution = greedy(n, first, spectrum)
    result = Levenshtein.ratio(getSequence(initialSolution), fullSequence)
    stop = time.time()
    # solution = tabuSearch(initialSolution, n, spectrum)
    print('{};{};{}'.format(sys.argv[1], result, stop - start))