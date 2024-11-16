import csv


#WHAT IF DEGREE CONSTRAINT IS LARGER THAN VERTEX_AMOUNT

def parse_csv_file(filename: str) -> list[list[int]]:
    input_matrix = []
    try:
        with open(filename, "r") as file:
            csv_reader = csv.reader(file, delimiter=",")
            for line in csv_reader:
                input_matrix.append(list(map(int, line)))
    except IOError as e:
        print ("file error")
        print (e)

    return input_matrix


def validate_input_size(input_matrix: list[list[int]]) -> bool:
    size: int = len(input_matrix[0])
    for row in input_matrix:
        if len(row) != size:
            return False
    return True

def validate_undirected(input_matrix: list[list[int]]) -> bool:
    for i in range(len(input_matrix[0])):
        for j in range(len(input_matrix[0])):
            if input_matrix[i][j] != input_matrix[j][i]:
                return False
    return True

def edge_to_itself(input_matrix: list[list[int]]) -> bool:
    for vertex in range(len(input_matrix)):
        if input_matrix[vertex][vertex] == 1:
            return True
    return False

def validate_input(input_matrix: list[list[int]]) -> bool:
    if not validate_input_size(input_matrix):
        print("Incorrect matrix dimensions (not a square matrix)")
        return False
    if not validate_undirected(input_matrix):
        print("Provided graph is not undirected, check edges")
        return False
    if edge_to_itself(input_matrix):
        print("Edge to itself is not allowed")
        return False
    return True
