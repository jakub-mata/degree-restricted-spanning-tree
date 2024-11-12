import subprocess


def write_to_file_and_call_solver(output_filename: str, cnf: list[list[int]], vars: int, solver:str = "glucose-syrup"):
    with open(output_filename, "w") as file:
        file.write("p cnf " + str(vars) + " " + str(len(cnf)) + '\n')
        for line in cnf:
            file.write(' '.join(str(literal) for literal in line) + '\n')

    #call the solver        
    return subprocess.run(['./' + solver, '-model', '-verb=1', output_filename], stdout=subprocess.PIPE)

def print_result(result):
    UNSAT: int = 20
    for line in result.stdout.decode('utf-8').split('\n'):
        print(line)

    if (result.returncode == UNSAT):
        return
    
    '''
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
    '''
