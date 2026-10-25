import glob
import os

from data import *
import search

PUZZLE_DIR = "sudoku"    
RESULT_DIR = "resultats"
NB_RUNS = 1

ALGORITHMS = [
    ("genetique", search.genetic, 1),
    ("hill_climbing", search.climbing_hill, 1000),
]


def write_run_history(file_path, history, nb_iterations, execution_time, step):
   
    with open(file_path, "w", encoding="utf-8") as f:
        for iteration, errors in enumerate(history, start=1):
            if iteration % step == 0 or iteration == len(history):
                f.write(f"{iteration}\t{errors}\n")
        f.write(f"{nb_iterations}\n")
        f.write(f"{execution_time}\n")

def write_run(file_path,nb_iterations, execution_time, solution):
   
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"{solution}\n")
        f.write(f"{nb_iterations}\n")
        f.write(f"{execution_time}\n")


if __name__ == "__main__":
    puzzle_files = sorted(glob.glob(os.path.join(PUZZLE_DIR, "*.csv")))

    summary = []
  

    puzzles = []
    for puzzle_file in puzzle_files:
       
        df = extract_csv(puzzle_file)

        base_name = os.path.splitext(os.path.basename(puzzle_file))[0]
        for index in range(len(df)):
            name = base_name if len(df) == 1 else f"{base_name}_{index + 1:02d}"
            puzzles.append((name, puzzle_file, df, index))

    input_dir = os.path.join(PUZZLE_DIR, "inputs")

    for puzzle_name, puzzle_file, df, index in puzzles:
        print(f"\n===== {puzzle_name} ({puzzle_file}, ligne {index + 1}) =====")

        puzzle = extract_multiple_puzzle(df, index)
       

        difficulty = df["Difficulty"].iloc[index] if "Difficulty" in df.columns else "?"
        print(f"Difficulté : {difficulty}")


        output_dir = os.path.join(RESULT_DIR, puzzle_name)
        os.makedirs(output_dir, exist_ok=True)

        for name, algo, step in ALGORITHMS:
            nb_found = 0
            for run in range(1, NB_RUNS + 1):


                solution, execution_time, history, nb_iterations = algo(puzzle)

                file_path = os.path.join(output_dir, f"{name}_essai{run}.csv")
                write_run(file_path, nb_iterations, execution_time, solution)

                found = solution is not None
                nb_found += found
                print(f"{name:>14} | essai {run:2d} | {'trouvé    ' if found else 'NON trouvé'} | "
                      f"itérations: {nb_iterations:>8} | temps: {execution_time / 1e9:8.3f} s")

            summary.append((puzzle_name, difficulty, name, nb_found))