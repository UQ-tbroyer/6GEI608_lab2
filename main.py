import glob
import os

from data import extract_csv, extract_puzzle
import search

PUZZLE_DIR = "sudoku"       # dossier qui contient tes 10 puzzles (un .csv par puzzle)
RESULT_DIR = "resultats"
NB_RUNS = 10

# (nom, fonction, pas d'écriture de l'historique)
# Le hill climbing peut faire des centaines de milliers d'itérations : on n'écrit
# qu'une ligne toutes les 1000 itérations pour ne pas créer des fichiers énormes.
ALGORITHMS = [
    ("genetique", search.genetic, 1),
    ("hill_climbing", search.climbing_hill, 1000),
]


def write_run(file_path, history, nb_iterations, execution_time, step):
    """
    Format (identique au lab 1) :
      itération <TAB> nombre d'erreurs du meilleur état   <- une ligne par itération
      ...
      nombre d'itérations                                 <- avant-dernière ligne
      temps d'exécution (ns)                              <- dernière ligne
    """
    with open(file_path, "w", encoding="utf-8") as f:
        for iteration, errors in enumerate(history, start=1):
            if iteration % step == 0 or iteration == len(history):
                f.write(f"{iteration}\t{errors}\n")
        f.write(f"{nb_iterations}\n")
        f.write(f"{execution_time}\n")


if __name__ == "__main__":
    puzzle_files = sorted(glob.glob(os.path.join(PUZZLE_DIR, "*.csv")))
    if not puzzle_files:
        raise SystemExit(f"Aucun fichier .csv trouvé dans '{PUZZLE_DIR}'")

    summary = []
    skipped = []

    # Chaque fichier peut contenir un ou plusieurs puzzles (une ligne par puzzle).
    # Chaque puzzle est enregistré dans son propre fichier dans sudoku/inputs/
    # (fichiers d'input à remettre) et ses résultats vont dans resultats/<puzzle>/.
    puzzles = []
    for puzzle_file in puzzle_files:
        try:
            df = extract_csv(puzzle_file)
        except Exception as error:
            print(f"!! Fichier ignoré ({puzzle_file}) : {error}")
            skipped.append((puzzle_file, str(error)))
            continue

        base_name = os.path.splitext(os.path.basename(puzzle_file))[0]
        for index in range(len(df)):
            name = base_name if len(df) == 1 else f"{base_name}_{index + 1:02d}"
            puzzles.append((name, puzzle_file, df, index))

    input_dir = os.path.join(PUZZLE_DIR, "inputs")
    os.makedirs(input_dir, exist_ok=True)

    for puzzle_name, puzzle_file, df, index in puzzles:
        print(f"\n===== {puzzle_name} ({puzzle_file}, ligne {index + 1}) =====")

        # lecture du puzzle : on saute la ligne si elle est mal formée
        try:
            puzzle = extract_puzzle(df, index)
        except Exception as error:
            print(f"!! Puzzle ignoré ({puzzle_name}) : {error}")
            skipped.append((puzzle_name, str(error)))
            continue

        difficulty = df["Difficulty"].iloc[index] if "Difficulty" in df.columns else "?"
        print(f"Difficulté : {difficulty}")

        # enregistrer ce puzzle dans son propre fichier
        df.iloc[[index]].to_csv(os.path.join(input_dir, f"{puzzle_name}.csv"), index=False)

        output_dir = os.path.join(RESULT_DIR, puzzle_name)
        os.makedirs(output_dir, exist_ok=True)

        for name, algo, step in ALGORITHMS:
            nb_found = 0
            for run in range(1, NB_RUNS + 1):
                solution, execution_time, history, nb_iterations = algo(puzzle)

                file_path = os.path.join(output_dir, f"{name}_essai{run}.csv")
                write_run(file_path, history, nb_iterations, execution_time, step)

                found = solution is not None
                nb_found += found
                print(f"{name:>14} | essai {run:2d} | {'trouvé    ' if found else 'NON trouvé'} | "
                      f"itérations: {nb_iterations:>8} | temps: {execution_time / 1e9:8.3f} s")

            summary.append((puzzle_name, difficulty, name, nb_found))

    print("\n===== Résumé =====")
    for puzzle_name, difficulty, name, nb_found in summary:
        print(f"{puzzle_name:<20} {str(difficulty):<12} {name:<14} {nb_found}/{NB_RUNS} résolus")

    if skipped:
        print("\n===== Fichiers ignorés =====")
        for puzzle_file, error in skipped:
            print(f"{puzzle_file} : {error}")