import math
import random
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


    print(current)
    return current

def climbing_hill(puzzle):
    global initial
    initial = puzzle
    current  = [[0 for _ in range(9)] for _ in range(9)]
    
    isEnding = False
    iteration = 0
    temperature = 0.5
    temperatureZero = 0.2 
    cooling = 0.99999998

    errors = 1_000_000 #close to infinity
    best = errors

    #remplir aleatoirement
    current = random_fill()

    while(not isEnding and temperature > temperatureZero):
          solution, isEnding, errors = climb(current, temperature)
          current = solution

          temperature *= cooling

          if errors < best:
             best = errors
             
      

          iteration += 1
          print(iteration)


    #print(current)
    return solution


def climb(passedPuzzle, temperature):
      
      randowRow = int(random.random() * 9)
      randomCol1 = int(random.random() * 9)
      randomCol2 = int(random.random() * 9)
      stepState  = [[0 for _ in range(9)] for _ in range(9)]

      free = []

      for i in range(9):
            for j in range(9):
                  stepState[i][j] = passedPuzzle[i][j]

                  if initial[i][j] == 0:
                        free.append((i,j))


      #not initial puzzle

      while((randowRow, randomCol1) not in free or (randowRow, randomCol2) not in free):
            randowRow = int(random.random() * 9)
            randomCol1 = int(random.random() * 9)
            randomCol2 = int(random.random() * 9)

      #swap
      stepState[randowRow][randomCol1], stepState[randowRow][randomCol2] = stepState[randowRow][randomCol2], stepState[randowRow][randomCol1]
      
      currentErrors = errors_counter(passedPuzzle)
      stepErrors = errors_counter(stepState)

      delta =  currentErrors - stepErrors

      if (stepErrors == 0):
            print(stepErrors)
            return stepState, True, stepErrors

      elif delta > 0 or random.random() < math.exp(delta / temperature):
            print("errors " + str(stepErrors))
            return stepState, False, stepErrors

      else:
            print("errors " + str(currentErrors))
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




if __name__ == "__main__":
      df = extract_csv()
      pp = extract_puzzle(df)

      print(climbing_hill(pp))