import itertools

def create_vertex_subsets(subset_size: int, vertex_amount: int) -> list[tuple[int,...]]:
    lst_of_verteces = [x for x in range(vertex_amount)]
    subsets: list[tuple[int, ...]] = list(itertools.combinations(lst_of_verteces, subset_size))
    return subsets

def encode_degree_constraint(vertex: int, cnf: list[list[int]], subsets: list[tuple[int,...]], vertex_amount: int):
    for subset in subsets:
        clause: list[int] = []
        for j in subset:
            clause.append(-spanning_tree_edge_var(vertex, j, vertex_amount))
        clause.append(0)
        cnf.append(clause)

def create_edge_subsets(subset_size: int) -> list[tuple[tuple[int, int],...]]:
    raise NotImplementedError("edge subsets not implemented") 

def encode_edge_amount(cnf: list[list[int]], edge_subsets: list[tuple[tuple[int, int],...]]) -> None:
    raise NotImplementedError("edge amount not implemented")


def original_edge_var(i: int, j: int, vertex_amount: int) -> int:
    return calculate_edge_var(i, j, 1, vertex_amount)
def spanning_tree_edge_var(i: int, j:int, vertex_amount: int) -> int:
    return calculate_edge_var(i, j, 2, vertex_amount)
def order_var(i: int, j:int, vertex_amount: int) -> int:
    return calculate_edge_var(i, j, 3, vertex_amount)

def calculate_edge_var(i: int, j: int, scale: int, vertex_amount: int) -> int:
    return scale * (i * vertex_amount + j) + 1
 