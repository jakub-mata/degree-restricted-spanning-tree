from argparse import ArgumentParser
import csv
import itertools
import subprocess

VERTEX_AMOUNT: int = 0

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

def validate_input(input_matrix: list[list[int]]) -> bool:
    if not validate_input_size(input_matrix):
        print("Incorrect matrix dimensions (not a square matrix)")
        return False
    if not validate_undirected(input_matrix):
        print("Provided graph is not undirected, check edges")
        return False
    return True

def create_subsets(subset_size: int) -> list[tuple[int,...]]:
    lst_of_verteces = [x for x in range(VERTEX_AMOUNT)]
    subsets: list[tuple[int, ...]] = list(itertools.combinations(lst_of_verteces, subset_size))
    return subsets

def encode_degree_constraint(vertex: int, cnf: list[list[int]], subsets: list[tuple[int,...]]):
    for subset in subsets:
        clause: list[int] = []
        for j in subset:
            clause.append(-spanning_tree_edge_var(vertex, j))
        clause.append(0)
        cnf.append(clause)

def encode(input_matrix: list[list[int]], degree_constraint: int):
    cnf: list[list[int]] = []

    '''
    Var space:
        - e(i,j): if an edge {i,j} is in the original graph
        - s(i,j): if an edge {i,j} is in the spanning tree
        - f(i,j): if there is a flow from vertex i to j, ensuring connectivity
        - o(i,j): given a root, if vertex i is above j in a typical top-to-bottom structure
    '''

    VERTEX_AMOUNT = len(input_matrix)
    var_count: int = 4 * (VERTEX_AMOUNT ^ VERTEX_AMOUNT)

    #construct graph
    for i in range(VERTEX_AMOUNT):
        for j in range(VERTEX_AMOUNT):
            if input_matrix[i][j] == 1:
                cnf.append([original_edge_var(i,j), 0])
            else:
                cnf.append([-original_edge_var(i,j), 0])

    #undirected_spanning_tree
    for i in range(VERTEX_AMOUNT):
        for j in range(i, VERTEX_AMOUNT):
            cnf.append([spanning_tree_edge_var(i,j), -spanning_tree_edge_var(j, i), 0])
            cnf.append([-spanning_tree_edge_var(i,j), spanning_tree_edge_var(j, i), 0])

    #follows graph input
    for i in range(VERTEX_AMOUNT):
        for j in range(i, VERTEX_AMOUNT):
            cnf.append([-spanning_tree_edge_var(i, j), original_edge_var(i, j), 0])

    #degree constraint
    for vertex in range(VERTEX_AMOUNT):
        encode_degree_constraint(vertex, cnf, create_subsets(degree_constraint + 1))

    #every_vertex_in_spanning_tree
    for i in range(VERTEX_AMOUNT):
        clause: list[int] = []
        for j in range(VERTEX_AMOUNT):
            clause.append(spanning_tree_edge_var(i, j))
        clause.append(0)
        cnf.append(clause)
    
    #CONNECTIVITY
    
    #ORDER
    #setup root
    for j in range(VERTEX_AMOUNT):
        cnf.append([order_var(0,j), 0])
    #order_symmetry
    for i in range(VERTEX_AMOUNT):
        for j in range(VERTEX_AMOUNT):
            cnf.append([order_var(i,j), -order_var(j,i), 0])
            cnf.append([-order_var(i,j), order_var(j,i), 0])
    #order transitivity
    for i in range(VERTEX_AMOUNT):
        for j in range(VERTEX_AMOUNT):
            pass
    #order follows flow

    return cnf, var_count


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
    
def write_to_file_and_call_solver(output_filename: str, cnf: list[list[int]], vars: int, solver:str = "glucose"):
    with open(output_filename, "w") as file:
        file.write("p cnf " + str(vars) + " " + str(len(cnf)) + '\n')
        for line in cnf:
            file.write(' '.join(str(literal) for literal in line) + '\n')

    #call the solver        
    return subprocess.run(['./' + solver, '-model', output_filename], stdout=subprocess.PIPE)

def print_result(result):
    UNSAT: int = 20
    for line in result.stdout.decode('utf-8').split('\n'):
        print(line)

    if (result.returncode == UNSAT):
        return
    
    model = []
    for line in result.stdout.decode('utf-8').split('\n'):
        if line.startswith("v"):    # there might be more lines of the model, each starting with 'v'
            vars = line.split(" ")
            vars.remove("v")
            model.extend(int(v) for v in vars)      
    model.remove(0)

    print()
    print("##################################################################")
    print("#####################[ Human readable result ]####################")
    print("##################################################################")
    print()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Filename for csv file with input")
    parser.add_argument("-o", "--output", type=str, help="Filename for the output file in cnf format")
    parser.add_argument("-d", "--degree", type=int, help="Max degree of a spanning tree", required=True)
    args = parser.parse_args()

    input_matrix: list[list[int]] = parse_csv_file(args.input)
    if not validate_input(input_matrix):
        raise AssertionError("Invalid input")

    cnf, vars = encode(input_matrix, args.d)
    result = write_to_file_and_call_solver(args.output, cnf, vars, args.output)
    print_result(result)
