import pandas as pd


def extract_csv(outpufile="sudoku/exemple.csv"):
    """Lit un fichier CSV de puzzles (format qqwing)."""
    df = pd.read_csv(outpufile, index_col=False)
    print(df.to_string())
    return df


def extract_puzzle(dataframe, index=0):
    """Retourne le puzzle de la ligne `index` du fichier (0 = premier puzzle) sous forme de grille 9x9."""
    if dataframe.empty:
        raise ValueError("le fichier ne contient aucune ligne de puzzle")

    puzzle_raw = str(dataframe["Puzzle"].iloc[index]).strip()

    if len(puzzle_raw) != 81:
        raise ValueError(f"le puzzle doit contenir 81 caractères, il en contient {len(puzzle_raw)}")

    puzzle_processed = []
    for i in range(9):
        puzzle_processed.append([])
        for j in range(9):
            symbol = puzzle_raw[i * 9 + j]
            if symbol != '.':
                puzzle_processed[i].append(int(symbol))
            else:
                puzzle_processed[i].append(0)

    print(puzzle_processed)
    return puzzle_processed


if __name__ == "__main__":
    df = extract_csv("sudoku/exemple.csv")
    pp = extract_puzzle(df, 0)