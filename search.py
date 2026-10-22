import math
import random
import time
from multiprocessing import Pool, cpu_count
from data import *

#1147688
MAX_RESTARTS=10_000_000

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


    #print(current)
    return current


def init_worker(puzzle):        
      global initial
      initial = puzzle
      random.seed()



def one_restart(_):              
      current = random_fill()
      currentErrors = errors_counter(current)
      isEnding = False
      while not isEnding:
            neighbor, errors = climb(current)
            if neighbor is None or errors >= currentErrors:
                  isEnding = True
            else:
                  current = neighbor
                  currentErrors = errors
      return current, currentErrors



def climbing_hill(puzzle, isParallel=True):

    best = None
    leastErrors = 1_000_000

    MAX_THREAD = 100
    start = time.time_ns()

    
    if (isParallel):
          nbWorkers = cpu_count()
          PRINT_EVERY = 60                 
          startTime = time.time()
          lastPrint = startTime
 
          with Pool(nbWorkers, initializer=init_worker, initargs=(puzzle,)) as pool:
                results = pool.imap_unordered(one_restart, range(MAX_RESTARTS), chunksize=16)
 
                for i, (current, currentErrors) in enumerate(results):
                      if leastErrors > currentErrors:
                            best = current
                            leastErrors = currentErrors
 
                      if leastErrors == 0:
                            break          
 
                      now = time.time()
                      if now - lastPrint >= PRINT_EVERY:
                            done = i + 1
                            elapsed = now - startTime
                            print(f"[{elapsed:6.0f}s] {done}/{MAX_RESTARTS} restarts done "
                                  f"leastError: {leastErrors}")
                            lastPrint = now
 
          print(f"finished after {i + 1} restarts in {time.time() - startTime:.1f}s, leastError: {leastErrors}")
          end = (time.time_ns() - start) / 1_000_000_000
          return best, end, i + 1

    else:
         for i in range(MAX_RESTARTS):  
            global initial
            initial = puzzle
      
            isEnding = False
            
            #remplir aleatoirement
            current = random_fill()
      
            currentErrors = errors_counter(current)
      
            while not isEnding: 
                  neighbor, errors = climb(current)
      
                  if neighbor is None or errors >= currentErrors:
                        isEnding = True
                  
                  else:    
                        current = neighbor
                        currentErrors = errors
      
            if leastErrors > currentErrors:
                  best = current
                  leastErrors = currentErrors
      
            if leastErrors == 0:
                  #break
                  end = (time.time_ns() - start) / 1_000_000_000
                  return best, end, i + 1
      
            if i % 100 == 0:     
                  print("nb climb: "+str(i))
                  print("leastError: " + str(leastErrors))



         end = (time.time_ns() - start) / 1_000_000_000
         return best, end, i + 1

def climbing_hill_logic(puzzle, best, leastErrors, i):
      global initial
      initial = puzzle

      isEnding = False
      
      #remplir aleatoirement
      current = random_fill()

      currentErrors = errors_counter(current)

      while not isEnding: 
            neighbor, errors = climb(current)

            if neighbor is None or errors >= currentErrors:
                  isEnding = True
            
            else:    
                  current = neighbor
                  currentErrors = errors

      if leastErrors > currentErrors:
            best = current
            leastErrors = currentErrors

      if leastErrors == 0:
            #break
            return best

      if i % 100 == 0:     
            print("nb climb: "+str(i))
            print("leastError: " + str(leastErrors))

      return best



def climb(passedPuzzle):

      leastErrors = 1_000_000
      bestState  = [[0 for _ in range(9)] for _ in range(9)]
      errors = errors_counter(passedPuzzle)

      for i in range(9):
            #column a remplir
            free = [] 

            for j in range(9):
            

                  if initial[i][j] == 0:
                        free.append(j)


            tailleFree = len(free)

            for j in range(tailleFree):
                  for k in range(j+1, tailleFree):
                        col1, col2 = free[j], free[k] 

                        #swap
                        passedPuzzle[i][col1], passedPuzzle[i][col2] = passedPuzzle[i][col2], passedPuzzle[i][col1]

                        errors = errors_counter(passedPuzzle)

                        if errors < leastErrors:
                              leastErrors = errors
                              bestState = [[passedPuzzle[a][b] for b in range(9)] for a in range(9)]

                        #reinitialise
                        passedPuzzle[i][col1], passedPuzzle[i][col2] = passedPuzzle[i][col2], passedPuzzle[i][col1]      
      

      #print("errors " + str(leastErrors))
      return bestState, leastErrors

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
      start = time.time_ns()
      df = extract_csv("sudoku/exemple_simple.csv")
      pp = extract_puzzle(df)
      
      print(climbing_hill(pp))
      print("----------------------")
      print(pp)
      end = time.time_ns() - start
      print(end / 1_000_000_000)