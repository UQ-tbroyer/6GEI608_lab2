import pandas as pd



def extract_csv(outpufile="sudoku/exemple.csv"):
    df = pd.read_csv(outpufile, index_col=False)

    print(df.to_string())

    return df


def extract_puzzle(dataframe, index=0):

    puzzle_raw = str(dataframe["Puzzle"].iloc[index]).strip()


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


def extract_multiple_puzzle(dataframe, index=0):

    puzzle_raw = str(dataframe["Puzzle"].iloc[index]).strip()

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
    df = extract_csv()
    extract_puzzle(df)