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

    pastErrors = -1

    plain = 0


    #remplir aleatoirement
    current = random_fill()

    while(not isEnding):
          solution, isEnding, errors = climb(current)
          current = solution

          if(pastErrors == errors):
                plain += 1

          else:
                plain = 0

          pastErrors = errors

          if(plain >= 1000):
               current = random_fill()
               print("plain")
               plain = 0

          iteration += 1
          print(iteration)


    print(current)
    return solution


def climb(passedPuzzle):
      
      randowRow = int(random.random() * 9)
      randomCol1 = int(random.random() * 9)
      randomCol2 = int(random.random() * 9)
      stepState  = [[0 for _ in range(9)] for _ in range(9)]

      for i in range(9):
            for j in range(9):
                  stepState[i][j] = passedPuzzle[i][j]


      #swap

      stepState[randowRow][randomCol1], stepState[randowRow][randomCol2] = stepState[randowRow][randomCol2], stepState[randowRow][randomCol1]
      
      currentErrors = errors_counter(passedPuzzle)
      stepErrors = errors_counter(stepState)

      if (currentErrors <= stepErrors):

            print(currentErrors )
            return passedPuzzle, False, currentErrors

      elif (stepErrors == 0):
            print(stepErrors)
            return stepState, True, stepErrors

      else:
            print(stepErrors)
            return stepState, False, stepErrors



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