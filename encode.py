import encoding_helpers
from encoding_helpers import original_edge_var
from encoding_helpers import spanning_tree_edge_var
from encoding_helpers import order_var


def encode(input_matrix: list[list[int]], degree_constraint: int):
    cnf: list[list[int]] = []

    '''
    Var space:
        - e(i,j): if an edge {i,j} is in the original graph
        - s(i,j): if an edge {i,j} is in the spanning tree
        - o(i,j): given a root, if vertex i is above j in a typical top-to-bottom tree structure
        - r(i,j): if there exists a path between i and j (reachability)
    '''

    VERTEX_AMOUNT: int = len(input_matrix)
    var_count: int = 4 * (VERTEX_AMOUNT * VERTEX_AMOUNT)

    #construct graph
    for i in range(VERTEX_AMOUNT):
        for j in range(VERTEX_AMOUNT):
            if input_matrix[i][j] == 1:
                cnf.append([original_edge_var(i,j, VERTEX_AMOUNT), 0])
            else:
                cnf.append([-original_edge_var(i,j, VERTEX_AMOUNT), 0])

    #undirected_spanning_tree
    for i in range(VERTEX_AMOUNT):
        for j in range(i, VERTEX_AMOUNT):
            cnf.append([spanning_tree_edge_var(i,j, VERTEX_AMOUNT), -spanning_tree_edge_var(j, i, VERTEX_AMOUNT), 0])
            cnf.append([-spanning_tree_edge_var(i,j, VERTEX_AMOUNT), spanning_tree_edge_var(j, i, VERTEX_AMOUNT), 0])

    #follows graph input
    for i in range(VERTEX_AMOUNT):
        for j in range(VERTEX_AMOUNT):
            cnf.append([-spanning_tree_edge_var(i, j, VERTEX_AMOUNT), original_edge_var(i, j, VERTEX_AMOUNT), 0])

    #degree constraint
    for vertex in range(VERTEX_AMOUNT):
        encoding_helpers.encode_degree_constraint(vertex, cnf, encoding_helpers.create_vertex_subsets(degree_constraint + 1, VERTEX_AMOUNT), VERTEX_AMOUNT)

    #every_vertex_in_spanning_tree
    for i in range(VERTEX_AMOUNT):
        clause: list[int] = []
        for j in range(VERTEX_AMOUNT):
            clause.append(spanning_tree_edge_var(i, j, VERTEX_AMOUNT))
        clause.append(0)
        cnf.append(clause)
    
    #ORDER (acyclicity)
    #setup root
    for j in range(VERTEX_AMOUNT):
        cnf.append([order_var(0,j, VERTEX_AMOUNT), 0])
    #order reflexivity
    for i in range(VERTEX_AMOUNT):
        cnf.append([order_var(i, i, VERTEX_AMOUNT), 0])
    #order_antisymmetry
    for i in range(VERTEX_AMOUNT):
        for j in range(VERTEX_AMOUNT):
            if j == i: #breaks reflexivity
                continue
            cnf.append([order_var(i,j, VERTEX_AMOUNT), -order_var(j,i, VERTEX_AMOUNT), 0])
            cnf.append([-order_var(i,j, VERTEX_AMOUNT), order_var(j,i,VERTEX_AMOUNT), 0])
    #order transitivity (through edges and order itself)
    for i in range(VERTEX_AMOUNT):
        for j in range(VERTEX_AMOUNT):
            for k in range(VERTEX_AMOUNT):
                if i == j or j == k or i == k:
                    continue
                cnf.append([-order_var(i,j,VERTEX_AMOUNT),-order_var(j,k,VERTEX_AMOUNT),order_var(i,k,VERTEX_AMOUNT), 0])
                cnf.append([-order_var(i,j,VERTEX_AMOUNT),-spanning_tree_edge_var(j,k,VERTEX_AMOUNT),order_var(i,k,VERTEX_AMOUNT), 0])

    #REACHABILITY
    encoding_helpers.encode_edge_count(cnf, VERTEX_AMOUNT)


    return cnf, var_count
