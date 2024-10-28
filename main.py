from argparse import ArgumentParser
import csv

VERTEX_AMOUNT: int = 0

def parse_csv_file(filename: str) -> list[list[int]]:
    input_matrix = []
    with open(filename, "r") as file:
        csv_reader = csv.reader(file, delimiter=",")
        for line in csv_reader:
            input_matrix.append(list(map(int, line)))
    
    return input_matrix

def encode(input_matrix: list[list[int]]):
    cnf: list[list[int]] = []

    '''
    Var space:
        - e(i,j): if an edge {i,j} is in the original graph
        - s(i,j): if an edge {i,j} is in the spanning tree
        - f(i,j): if there is a flow from vertex i to j, ensuring connectivity
        - o(i,j): given a root, if vertex i is above j in a typical top-to-bottom structure
    '''

    VERTEX_AMOUNT = len(input_matrix)
    var_count = 4 * (VERTEX_AMOUNT ^ VERTEX_AMOUNT)

    #construct graph
    for i in range(VERTEX_AMOUNT):
        for j in range(VERTEX_AMOUNT):
            if input_matrix[i][j] == 1:
                cnf.append([original_edge_var(i,j), 0])
            else:
                cnf.append([-original_edge_var(i,j), 0])

    #undirected_graph
    for i in range(VERTEX_AMOUNT):
        for j in range(i, VERTEX_AMOUNT):
            cnf.append([original_edge_var(i,j), -original_edge_var(j, i), 0])
            cnf.append([-original_edge_var(i,j), original_edge_var(j, i), 0])

    for i in range(VERTEX_AMOUNT):
        for j in range(i, VERTEX_AMOUNT):
            cnf.append([spanning_tree_edge_var(i,j), -spanning_tree_edge_var(j, i), 0])
            cnf.append([-spanning_tree_edge_var(i,j), spanning_tree_edge_var(j, i), 0])

    ##follows graph input
    for i in range(VERTEX_AMOUNT):
        for j in range(i, VERTEX_AMOUNT):
            cnf.append([-spanning_tree_edge_var(i, j), original_edge_var(i, j), 0])

    #degree constraint

    #every_vertex_in_spanning_tree
    for i in range(VERTEX_AMOUNT):
        clause: list[int] = []
        for j in range(VERTEX_AMOUNT):
            clause.append(spanning_tree_edge_var(i, j))
        clause.append(0)
        cnf.append(clause)
    
    #connectivity
    
    #order

    return cnf, ""


def original_edge_var(i: int, j: int) -> int:
    return calculate_edge_var(i, j, 1)
def spanning_tree_edge_var(i: int, j:int) -> int:
    return calculate_edge_var(i, j, 2)
def flow_var(i: int, j:int) -> int:
    return calculate_edge_var(i, j, 3)
def order_var(i: int, j:int) -> int:
    return calculate_edge_var(i, j, 4)

def calculate_edge_var(i: int, j: int, scale: int) -> int:
    return scale * (i * VERTEX_AMOUNT + j) + 1
    
def call_solver(cnf: list[list[int]], vars: str, output_filename: str, solver:str = "glucose"):
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
