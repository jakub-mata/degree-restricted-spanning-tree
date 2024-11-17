import itertools

def create_vertex_subsets(subset_size: int, vertex_amount: int) -> list[tuple[int,...]]:
    lst_of_verteces = [x for x in range(vertex_amount)]
    subsets: list[tuple[int, ...]] = list(itertools.combinations(lst_of_verteces, subset_size))
    return subsets

def encode_degree_constraint(vertex: int, cnf: list[list[int]], subsets: list[tuple[int,...]], vertex_amount: int) -> None:
    for subset in subsets:
        clause: list[int] = []
        for j in subset:
            clause.append(-spanning_tree_edge_var(vertex, j, vertex_amount))
        clause.append(0)
        cnf.append(clause)

def get_neighbors(vertex: int, input_matrix: list[list[int]]) -> list:
    neighbors = []
    vertex_row = input_matrix[vertex]
    for neighbor,val in enumerate(vertex_row):
        if val == 1:
            neighbors.append(neighbor)
    return neighbors

def encode_connectedness(cnf: list[list[int]], vertex_amount: int, input_matrix: list[list[int]]) -> None:
    '''
    var space:
        x(i,t,j): vertex i is at position t in a path ending at j
    '''

    for j in range(1, vertex_amount):  #path from (0 to j)
        #start
        cnf.append([path_var(0, 0, j, vertex_amount), 0])
        #end is somewhere
        end_clause = []
        for t in range(1, vertex_amount):
            end_clause.append(path_var(j,t,j, vertex_amount))
        end_clause.append(0)
        cnf.append(end_clause)

        #follow input
        for i in range(0, vertex_amount):
            if i == j: continue  #stop at the end of path
            neighbors = get_neighbors(i, input_matrix)
            for t in range(vertex_amount - 1):
                clause = [-path_var(i, t, j, vertex_amount)]
                for neighbor in neighbors:
                    clause.append(path_var(neighbor,t+1,j, vertex_amount))
                    cnf.append([
                        -path_var(i, t, j, vertex_amount),
                        -path_var(neighbor, t+1, j, vertex_amount),
                        spanning_tree_edge_var(i, neighbor, vertex_amount), 
                        0])
                clause.append(0)
                cnf.append(clause)
        
        #no 2 verteces at the same time in the path
        for t in range(0, vertex_amount):
            for i1 in range(vertex_amount):
                for i2 in range(i1+1, vertex_amount):
                    cnf.append([-path_var(i1, t, j, vertex_amount),-path_var(i2, t, j, vertex_amount),0])
        
        #no vertex twice on the same path
        for i in range(vertex_amount):
            for t1 in range(vertex_amount):
                for t2 in range(t1+1, vertex_amount):
                    cnf.append([-path_var(i, t1, j, vertex_amount), -path_var(i, t2, j, vertex_amount),0])
        


def original_edge_var(i: int, j: int, vertex_amount: int) -> int:
    return calculate_edge_var(i, j, 0, vertex_amount)

def spanning_tree_edge_var(i: int, j:int, vertex_amount: int) -> int:
    return calculate_edge_var(i, j, 1, vertex_amount)

def order_var(i: int, j:int, vertex_amount: int) -> int:
    return calculate_edge_var(i, j, 2, vertex_amount)

def calculate_edge_var(i: int, j: int, scale: int, vertex_amount: int) -> int:
    return (scale * vertex_amount * vertex_amount) + (i * vertex_amount + j) + 1

def path_var(i: int, position: int, end: int, vertex_amount: int) -> int:
    start = 3 * vertex_amount * vertex_amount
    path_offset = (end-1) * vertex_amount * vertex_amount  #|V| time positions, |V| verteces
    return start + path_offset + (i * vertex_amount + position) + 1
