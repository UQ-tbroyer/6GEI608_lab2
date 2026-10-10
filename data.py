import pandas as pd



def extract_csv(outpufile="sudoku/exemple.csv"):

    df = pd.read_csv(outpufile)

    print(df.to_string()) 

    return df


def extract_puzzle(dataframe):
    puzzle_raw = dataframe["Puzzle"][0]

    #print(puzzle_raw)

    puzzle_processed = []

    for i in range(9):
        puzzle_processed.append([])
        for j in range(9):
            symbol = puzzle_raw[i * 9 + j]
            #print(symbol)
            #print(type(symbol))

            if symbol != '.':
                puzzle_processed[i].append(int(symbol))

            else:
                puzzle_processed[i].append(0)


    print(puzzle_processed)
    return puzzle_processed




if __name__ == "__main__":
    df = extract_csv()
    extract_puzzle(df)