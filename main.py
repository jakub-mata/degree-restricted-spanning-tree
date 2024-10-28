from argparse import ArgumentParser
import csv

def parse_csv_file(filename: str) -> list[list[int]]:
    input_matrix = []
    with open(filename, "r") as file:
        csv_reader = csv.reader(file, delimiter=",")
        for line in csv_reader:
            input_matrix.append(list(map(int, line)))
    
    return input_matrix


def encode(input_matrix: list[list[int]]):
    cnf: list[str] = []
    return cnf, ""

    
def call_solver(cnf: list[str], vars: str, output_filename: str, solver:str = "glucose"):
    with open(output_filename, "w") as file:
        pass
    
    return 


if __name__ == "__main__":
    parser = ArgumentParser()
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Filename for csv file with input")
    parser.add_argument("-o", "--output", type=str, help="Filename for the output file in cnf format")
    parser.add_argument("-d", "--degree", type=int, help="Max degree of a spanning tree")
    args = parser.parse_args()

    input_matrix: list[list[int]] = parse_csv_file(args.input)
    cnf, vars = encode(input_matrix)
    result = call_solver(cnf, vars, args.output)
    print(result)
