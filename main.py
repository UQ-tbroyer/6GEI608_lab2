import glob
import os

from data import extract_csv, extract_puzzle
import search

PUZZLE_DIR = "sudoku"
RESULT_DIR = "resultats"
NB_RUNS = 1


def run_hill_climbing(puzzle):
    """climbing_hill retourne (meilleure grille, temps en s, nb de redémarrages)."""
    best, seconds, nb_restarts = search.climbing_hill(puzzle)
    search.initial = puzzle                       # utilisé par errors_counter
    solved = best is not None and search.errors_counter(best) == 0
    return (best if solved else None), int(seconds * 1e9), nb_restarts


def run_genetic(puzzle):
    """genetic retourne (solution ou None, temps en ns, historique, nb de générations)."""
    solution, execution_time, history, nb_generations = search.genetic(puzzle)
    return solution, execution_time, nb_generations


ALGORITHMS = [
    # ("genetique", run_genetic),
    ("hill_climbing", run_hill_climbing),
]


def write_run(file_path, nb_iterations, execution_time, solution):
    """Grille solution (9 lignes), puis nombre d'itérations, puis temps (ns)."""
    with open(file_path, "w", encoding="utf-8") as f:
        if solution is not None:
            for row in solution:
                f.write(" ".join(str(v) for v in row) + "\n")
        else:
            f.write("aucune solution\n")
        f.write(f"{nb_iterations}\n")
        f.write(f"{execution_time}\n")


if __name__ == "__main__":
    puzzle_files = sorted(glob.glob(os.path.join(PUZZLE_DIR, "*.csv")))
    if not puzzle_files:
        raise SystemExit(f"Aucun fichier .csv trouvé dans '{PUZZLE_DIR}'")

    summary = []
    puzzles = []
    for puzzle_file in puzzle_files:
        df = extract_csv(puzzle_file)
        base_name = os.path.splitext(os.path.basename(puzzle_file))[0]
        for index in range(len(df)):
            name = base_name if len(df) == 1 else f"{base_name}_{index + 1:02d}"
            puzzles.append((name, puzzle_file, df, index))

    input_dir = os.path.join(PUZZLE_DIR, "inputs")
    os.makedirs(input_dir, exist_ok=True)

    for puzzle_name, puzzle_file, df, index in puzzles:
        print(f"\n===== {puzzle_name} ({puzzle_file}, ligne {index + 1}) =====")

        puzzle = extract_puzzle(df, index)
        difficulty = df["Difficulty"].iloc[index] if "Difficulty" in df.columns else "?"
        print(f"Difficulté : {difficulty}")

        # enregistrer ce puzzle dans son propre fichier
        df.iloc[[index]].to_csv(os.path.join(input_dir, f"{puzzle_name}.csv"), index=False)

        output_dir = os.path.join(RESULT_DIR, puzzle_name)
        os.makedirs(output_dir, exist_ok=True)

        for name, algo in ALGORITHMS:
            nb_found = 0
            for run in range(1, NB_RUNS + 1):
                solution, execution_time, nb_iterations = algo(puzzle)

                file_path = os.path.join(output_dir, f"{name}_essai{run}.csv")
                write_run(file_path, nb_iterations, execution_time, solution)

                found = solution is not None
                nb_found += found
                print(f"{name:>14} | essai {run:2d} | {'trouvé    ' if found else 'NON trouvé'} | "
                      f"itérations: {nb_iterations:>8} | temps: {execution_time / 1e9:8.3f} s")

            summary.append((puzzle_name, difficulty, name, nb_found))

    print("\n===== Résumé =====")
    for puzzle_name, difficulty, name, nb_found in summary:
        print(f"{puzzle_name:<20} {str(difficulty):<12} {name:<14} {nb_found}/{NB_RUNS} résolus")