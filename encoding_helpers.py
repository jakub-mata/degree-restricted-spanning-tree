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
        x(i,t,p): vertex i is at position t in path p
    '''

    for j in range(1, vertex_amount):
        #path from (0 to j)
        path = path_offset(0, j, vertex_amount)

        #start
        cnf.append([path_var(0, 0, path, vertex_amount), 0])

        #end is somewhere
        for t in range(0, vertex_amount):
            cnf.append([path_var(0,t,path, vertex_amount), 0])

        #follow input
        for i in range(0, vertex_amount):
            if i == j: continue  #stop at the end of path
            for t in range(vertex_amount - 1):
                neighbors = get_neighbors(i, input_matrix)
                clause = [path_var(i, t, path, vertex_amount)]
                for neighbor in neighbors:
                    clause.append(path_var(neighbor,t+1,path, vertex_amount))
                    cnf.append([
                        -path_var(i, t, path, vertex_amount),
                        -path_var(neighbor, t+1, path, vertex_amount),
                        spanning_tree_edge_var(i, neighbor, vertex_amount), 
                        0])
                clause.append(0)
                cnf.append(clause)

        #no 2 verteces at the same time in the path
        for t in range(0, vertex_amount):
            for i in range(vertex_amount):
                for j in range(i+1, vertex_amount):
                    cnf.append([-path_var(i, t, path, vertex_amount),-path_var(j, t, path, vertex_amount),0])

        #no vertex twice on the same path
        for i in range(vertex_amount):
            for t1 in range(vertex_amount):
                for t2 in range(t1+1, vertex_amount):
                    cnf.append([-path_var(i, t1, path, vertex_amount), -path_var(i, t2, path, vertex_amount),0])


def original_edge_var(i: int, j: int, vertex_amount: int) -> int:
    return calculate_edge_var(i, j, 0, vertex_amount)
def spanning_tree_edge_var(i: int, j:int, vertex_amount: int) -> int:
    return calculate_edge_var(i, j, 1, vertex_amount)
def order_var(i: int, j:int, vertex_amount: int) -> int:
    return calculate_edge_var(i, j, 2, vertex_amount)

def calculate_edge_var(i: int, j: int, scale: int, vertex_amount: int) -> int:
    return (scale * vertex_amount * vertex_amount) + (i * vertex_amount + j) + 1

def path_var(i: int, position: int, path: int, vertex_amount: int) -> int:
    start = 3 * vertex_amount * vertex_amount
    offset = (path-1) * vertex_amount * vertex_amount
    return start + offset + (i * vertex_amount + position) + 1

def path_offset(i: int, j: int, vertex_amount: int) -> int:
    return i*vertex_amount + j


    
 


















'''
 def encode_edge_count(cnf: list[list[int]], vertex_amount: int) -> None:
    edges = create_vertex_subsets(2, vertex_amount)
    
    #cannot have |V| edges or more
    v_long_edges_subsets: list[tuple[tuple[int,...],...]] = list(itertools.combinations(edges, vertex_amount))
    for edge_subset in v_long_edges_subsets:
        clause: list[int] = []
        for edge in edge_subset:
            clause.append(-spanning_tree_edge_var(edge[0], edge[1], vertex_amount))
        clause.append(0)
        cnf.append(clause)

    #cannot have less than |V|-1 edges
    v_minus_one_long_edges_subsets: list[tuple[tuple[int,...],...]] = list(itertools.combinations(edges, vertex_amount-1))
    dnf = []
    for edge_subset in v_minus_one_long_edges_subsets:
        dnf_clause: list[int] = []
        for edge in edge_subset:
            dnf_clause.append(spanning_tree_edge_var(edge[0], edge[1], vertex_amount))
        dnf.append(clause)

    print(len(dnf))
    variations = variation_with_repetition(len(dnf), vertex_amount - 1)
    for variation in variations:
        cnf_clause = []
        for pos, val in enumerate(variation):
            cnf_clause.append(dnf[pos][val])
        cnf.append(cnf_clause)

def variation_with_repetition(length: int, top_value: int) -> list[tuple[int,...]]:
    numbers = [x for x in range(0, top_value)]
    return list(itertools.product(numbers, repeat=length))
 '''