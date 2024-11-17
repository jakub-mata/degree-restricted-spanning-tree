import subprocess

def graph_from_model(model: list, vertex_amount: int):
    graph: list[list[int]] = []
    start = vertex_amount * vertex_amount
    for i in range(vertex_amount):
        row = []
        for j in range(vertex_amount):
            val = model[start+i*vertex_amount+j]
            if val < 0: row.append(0)
            else: row.append(1)
        graph.append(row)
    return graph

def write_to_file_and_call_solver(output_filename: str, cnf: list[list[int]], vars: int, solver:str = "glucose-syrup"):
    with open(output_filename, "w") as file:
        file.write("p cnf " + str(vars) + " " + str(len(cnf)) + '\n')
        for line in cnf:
            file.write(' '.join(str(literal) for literal in line) + '\n')
    
    #call the solver
    return subprocess.run(['./' + solver, '-model', '-verb=1', output_filename], stdout=subprocess.PIPE)

def print_result(result, vertex_amount):
    UNSAT: int = 20
    for line in result.stdout.decode('utf-8').split('\n'):
        print(line)

    if (result.returncode == UNSAT):
        print("RESULTS:")
        print("Unfortunately, after careful consideration, we've come to the conclusion that your graph does not satisfy given parameters.")
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

    print("CONGRATULATIONS, there is a solution.")
    print("An example (not necessarily the only one) spanning tree satisfying your conditions represented as an adjacency matrix:")
    print()

    graph: list[list[int]] = graph_from_model(model, vertex_amount)
    for row in graph:
        print(', '.join(str(x) for x in row))
    
