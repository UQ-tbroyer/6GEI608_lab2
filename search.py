import math
import random
from data import *

def random_fill():
    current  = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(9):
       for j in range(9):
            if initial[i][j] == 0:
                  current[i][j] = int(random.random() * 9) + 1
            else:
                 current[i][j] = initial[i][j]
                  
    print(current)
    return current

def climbing_hill(puzzle):
    global initial
    initial = puzzle
    current  = [[0 for _ in range(9)] for _ in range(9)]
    
    #for i in range(9):
        #for j in range(9):
            #current[i][j] = puzzle[i][j]

    isEnding = False
    iteration = 0

    pastErrors = -1

    plain = 0

    #row = [1,2,3,4,5,6,7,8,9]

    #remplir aleatoirement
    current = random_fill()

    while(not isEnding):
          solution, isEnding, errors = climb(current)
          current = solution

          if(pastErrors == errors):
                plain += 1

          pastErrors = errors

          if(plain >= 100):
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


      #temp = stepState[randowRow][randomCol1]
      #stepState[randowRow][randomCol1] = stepState[randowRow][randomCol2]
      #stepState[randowRow][randomCol2] = temp

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
    seen = set()
    duplicates = set()

    for number in section:
        
        if number in seen:
            duplicates.add(number)
        else:
            seen.add(number)

    return len(list(duplicates))
      

def errors_counter(sudoku):
      errorsNumber = 0
      sectionRow = [[],[],[],[],[],[],[],[],[]]
      sectionCol = sudoku
      section3x3 = [[],[],[],[],[],[],[],[],[]]

      for i in range(9):
                for j in range(9):
                        if (sudoku[i][j] == 0):
                              print("zero")
                        if (sudoku[i][j] != initial[i][j]):
                              errorsNumber +=1

                        sectionRow[j].append(sudoku[i][j])

                        section3x3[i % 3 + int(j / 3)].append(sudoku[i][j])

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