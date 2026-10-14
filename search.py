import math
import random
import time
from data import *

def random_fill():
    current = []

    for i in range(9):
        
      line = initial[i]
      missing = []

      for n in range(1,10):
           if n not in line:
                missing.append(n)

                
      random.shuffle(missing)

      new_line = []
      for value in line:
            if value == 0:
                new_line.append(missing.pop())
            else:
                new_line.append(value)

      current.append(new_line)


    return current


# --------------------------------------------------------------------------
# Hill climbing
# --------------------------------------------------------------------------
# Voisin      : échange de deux cases modifiables dans une même ligne.
# Acceptation : seulement si le nombre d'erreurs ne augmente pas.
# Redémarrage : nouvelle grille aléatoire après 2000 itérations sans amélioration.

def climbing_hill(puzzle, max_iterations=2_000_000, max_stuck=2_000):
    """
    Retourne (solution ou None, temps d'exécution en ns, historique, nombre d'itérations).
    historique[k] = nombre d'erreurs de l'état courant après l'itération k+1.
    """
    global initial
    initial = puzzle

    history = []
    iteration = 0
    solution = None
    start_time = time.time_ns()

    current = random_fill()
    errors = errors_counter(current)
    stuck = 0

    while iteration < max_iterations:
        current, isEnding, new_errors = climb(current, errors)
        iteration += 1
        history.append(new_errors)

        if isEnding:
            solution = current
            break

        if new_errors < errors:
            stuck = 0
        else:
            stuck += 1
        errors = new_errors

        # minimum local : aucune amélioration depuis trop longtemps -> redémarrage
        if stuck >= max_stuck:
            current = random_fill()
            errors = errors_counter(current)
            stuck = 0

    execution_time = time.time_ns() - start_time
    return solution, execution_time, history, iteration


def climb(passedPuzzle, currentErrors):

      randowRow = int(random.random() * 9)
      randomCol1 = int(random.random() * 9)
      randomCol2 = int(random.random() * 9)

      # choisir deux cases modifiables (pas dans le puzzle initial) sur une même ligne
      while(initial[randowRow][randomCol1] != 0 or initial[randowRow][randomCol2] != 0
            or randomCol1 == randomCol2):
            randowRow = int(random.random() * 9)
            randomCol1 = int(random.random() * 9)
            randomCol2 = int(random.random() * 9)

      stepState = [list(row) for row in passedPuzzle]

      #swap
      stepState[randowRow][randomCol1], stepState[randowRow][randomCol2] = stepState[randowRow][randomCol2], stepState[randowRow][randomCol1]

      stepErrors = errors_counter(stepState)

      if stepErrors == 0:
            return stepState, True, stepErrors

      # hill climbing : on accepte seulement si ce n'est pas pire
      elif stepErrors <= currentErrors:
            return stepState, False, stepErrors

      else:
            return passedPuzzle, False, currentErrors



def find_duplicates(section):
    

    return 9 - len(set(section))
      

def errors_counter(sudoku):
      errorsNumber = 0
      sectionRow = [[],[],[],[],[],[],[],[],[]]
      sectionCol = sudoku
      section3x3 = [[],[],[],[],[],[],[],[],[]]

      for i in range(9):
                for j in range(9):
                        if (sudoku[i][j] == 0):
                              print("zero")
                        if (sudoku[i][j] != initial[i][j] and initial[i][j] != 0):
                              errorsNumber +=1

                        sectionRow[j].append(sudoku[i][j])

                        section3x3[(i // 3) * 3 + j // 3].append(sudoku[i][j])

      for i in range(9):
            errorsNumber += find_duplicates(sectionRow[i])
            errorsNumber += find_duplicates(sectionCol[i])
            errorsNumber += find_duplicates(section3x3[i])

      return errorsNumber




def verify(sudoku):
    total = 0
    for i in range(9):
          for j in range(9):
                total += sudoku[i][j]

    if(total != 243):
          return False

    else:
          pass
                
    return True


# --------------------------------------------------------------------------
# Algorithme génétique
# --------------------------------------------------------------------------
# Individu    : une grille 9x9 où chaque ligne contient les chiffres 1 à 9
#               (cases données fixes, cases vides remplies avec les chiffres manquants).
# Fitness     : errors_counter -> nombre de conflits (à minimiser, 0 = solution).
# Sélection   : tournoi de taille 3.
# Croisement  : uniforme par ligne (chaque ligne vient du parent 1 ou du parent 2).
# Mutation    : échange de deux cases modifiables dans une même ligne.
# Élitisme    : les 2 meilleurs individus passent à la génération suivante.
# Redémarrage : si aucune amélioration pendant 60 générations, nouvelle population.

def ga_individual(puzzle):
    individual = []
    for line in puzzle:
        missing = [n for n in range(1, 10) if n not in line]
        random.shuffle(missing)
        individual.append([missing.pop() if v == 0 else v for v in line])
    return individual


def ga_tournament(population, fitnesses, size=3):
    best = None
    for _ in range(size):
        k = random.randrange(len(population))
        if best is None or fitnesses[k] < fitnesses[best]:
            best = k
    return population[best]


def ga_crossover(parent1, parent2):
    return [list(parent1[i]) if random.random() < 0.5 else list(parent2[i]) for i in range(9)]


def ga_mutate(individual, free, rate):
    for r in range(9):
        if len(free[r]) >= 2 and random.random() < rate:
            c1, c2 = random.sample(free[r], 2)
            individual[r][c1], individual[r][c2] = individual[r][c2], individual[r][c1]

def fill_singles(puzzle):
    """Remplit les cases qui n'ont qu'une seule valeur possible, jusqu'à ce qu'il n'y en ait plus."""
    grid = [list(row) for row in puzzle]
    changed = True
    while changed:
        changed = False
        for i in range(9):
            for j in range(9):
                if grid[i][j] != 0:
                    continue
                used = set(grid[i]) | {grid[k][j] for k in range(9)}
                bi, bj = (i // 3) * 3, (j // 3) * 3
                used |= {grid[bi + a][bj + b] for a in range(3) for b in range(3)}
                candidates = [v for v in range(1, 10) if v not in used]
                if len(candidates) == 1:
                    grid[i][j] = candidates[0]
                    changed = True
    return grid

def genetic(puzzle, population_size=150, max_generations=5_000, elite_size=2,
            tournament_size=3, crossover_rate=0.9, mutation_rate=0.15, stagnation_limit=60):
    """
    Retourne (solution ou None, temps d'exécution en ns, historique, nombre de générations).
    historique[k] = meilleure fitness (nombre de conflits) à la génération k+1.
    """
    global initial
    initial = puzzle                      # utilisé par errors_counter

    free = [[j for j in range(9) if puzzle[i][j] == 0] for i in range(9)]

    history = []
    generation = 0
    solution = None
    best_ever = None
    stagnation = 0

    start_time = time.time_ns()
    population = [ga_individual(puzzle) for _ in range(population_size)]

    while generation < max_generations:
        fitnesses = [errors_counter(ind) for ind in population]
        order = sorted(range(population_size), key=lambda k: fitnesses[k])
        best_fitness = fitnesses[order[0]]

        generation += 1
        history.append(best_fitness)

        if best_fitness == 0:
            solution = population[order[0]]
            break

        if best_ever is None or best_fitness < best_ever:
            best_ever, stagnation = best_fitness, 0
        else:
            stagnation += 1

        if stagnation >= stagnation_limit:
            # population bloquée dans un minimum local : on repart de zéro
            population = [ga_individual(puzzle) for _ in range(population_size)]
            best_ever, stagnation = None, 0
            continue

        new_population = [[list(row) for row in population[k]] for k in order[:elite_size]]
        while len(new_population) < population_size:
            parent1 = ga_tournament(population, fitnesses, tournament_size)
            parent2 = ga_tournament(population, fitnesses, tournament_size)
            if random.random() < crossover_rate:
                child = ga_crossover(parent1, parent2)
            else:
                child = [list(row) for row in parent1]
            ga_mutate(child, free, mutation_rate)
            new_population.append(child)

        population = new_population

    execution_time = time.time_ns() - start_time
    return solution, execution_time, history, generation

if __name__ == "__main__":
      df = extract_csv()
      pp = extract_puzzle(df)

      solution, temps, historique, generations = genetic(pp)
      print("Génétique :", "trouvé" if solution else "NON trouvé", generations, "générations", temps / 1e9, "s")
      print(solution)

      solution, temps, historique, iterations = climbing_hill(pp)
      print("Hill climbing :", "trouvé" if solution else "NON trouvé", iterations, "itérations", temps / 1e9, "s")
      print(solution)