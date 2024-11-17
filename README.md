# degree-restricted-spanning-tree
A student project for solving the [degree constrained spanning tree](https://en.wikipedia.org/wiki/Degree-constrained_spanning_tree) problem with SAT (using the [glucose solver](https://github.com/audemard/glucose/)).

## Usage

The program is called like this
```
python3 span_restriction.py -i *input_file* -d *degree_constraint* [-o *output_file*]
```
The arguments are as follows:
1. `-i, --input`: a required argument containing the name of a file with graph input. More on the format below.
2. `-d, --degree`: a required argument representing the  maximum degree any individual vertex of the spanning tree is allowed to have
3. `-o, --output`: the name of the output file containing cnf clauses written in the [DIMACS CNF](https://jix.github.io/varisat/manual/0.2.0/formats/dimacs.html) format. The default is set to output.csv.

The result is printed to the terminal. Firstly, you recieve the output of the actual SAT solver. It shows whether the given graph is solvable or not. If yes, an example solution is printed at the end in the same format at the input (matrix representation).

## Input file format
The input file is a csv file, which represents a graph using the [adjacency matrix](https://en.wikipedia.org/wiki/Adjacency_matrix). E.g. a file containing this matrix
```
0,1,1,0,0
1,0,1,1,0
1,1,0,0,1
0,1,0,0,1
0,0,1,1,0
```
represents a graph that looks like a house (vertex 0 is the top of the roof, remaining verteces are numbered as if read by lines).

>IMPORTANT: the graph has to be undirected

Please realize the matrix has to be square and contain the same amount of numbers on all rows. The program checks for this but it's better to avoid it.

You can check for examples in the test_inputs directory.

### Example inputs
You can use example inputs in the `test_inputs` directory. Inputs with prefixes `fail_` contain somehow failing input. Usable examples include:
- `simpleGraph_house.csv`: a graph which looks like a house, it should pass all degrees above 1
- `completeGraph.csv`: contains a complete graph on 6 verteces, it should pass all degrees above 1
- `fanoPlane.csv`: contains the well known [Fano plane](https://en.wikipedia.org/wiki/Fano_plane), should pass all degrees above 1
- `k_3Satisfiable.csv`: looks like a diamond with 2 legs, both connecting at the same vertex (yes, this README requires imagination). It should not pass a degree constraint of 2, but it should pass 3 and above.


## Logic

### Variable space
- $e(i,j)$ - if there is an edge going from vertex $i$ to $j$ in the original graph
- $s(i,j)$ - if there is an edge in the spanning tree from $i$
 to $j$
- $o(i,j)$ - within the spanning tree, if vertex $i$ is above (precedes) $j$ in a typical tree top-to-bottom representation with the root at the top
- $x(i,t,j)$ - if vertex $i$ is in the path from vertex $0$ to $j$ at time (t-th on the path counting from 0) $t$. E.g. $x(5, 2, 1)$ would be true for the path $(0, 3, 5, 2, 1)$.

#### Original graph setup
`if input_matrix[i,j] == 1:` $e(i,j)$

`else:` $\neg e(i,j)$

#### Spanning tree setup
- *Is undirected*:
$$
\bigwedge_{i\neq j} s(i,j) \leftrightarrow s(j,i)
$$
- *Follows original graph*:
$$
\bigwedge_{i,j} s(i,j) \rightarrow e(i,j)
$$
- *Every vertex is withing the spanning tree*:
$$
\bigwedge_i \bigvee_j s(i,j)
$$
- *k - degree constraint*: for all (k+1) large subsets of verteces (let the set containing all these subsets be $S$)
$$
\bigwedge_i \bigvee_{j\in s, s\in S} \neg s(i,j)
$$
This ensures there isn't a vertex with (k+1) or more neighbors.

#### Order
Order is necessary for ensuring acyclicity of the spanning tree.
- root setup: a vertex that is at the top of the spanning tree
$$
\bigwedge_j o(0, j)
$$
- reflexivity:
$$
\bigwedge_i o(i,i)
$$
- anti-symmetry:
$$
\bigwedge_{j\neq i} o(i,j) \leftrightarrow \neg o(j,i)
$$
- transitivity:
$$
\bigwedge_{i\neq j\neq k} o(i,j) \wedge o(j,k) \rightarrow o(i,k)
$$
$$
\bigwedge_{i\neq j\neq k} o(i,j) \wedge s(i,j) \wedge s(j,k) \rightarrow o(j,k)
$$

#### Connectivity (reachability)
Connectivity is reached by finding out if from a certain vertex (e.g. $0$) there is a path to all other verteces in the graph. The paths can have different lengths but there are at most $|V|$ long. Hence parameter $t$ in $x(i, t, j)$ ranges from $0$ (although we don't calculate paths from $0$ to $0$ since it's unnecessary) to $|V|-1$.
- first position: vertex 0 appears at the start of the path to $j$
$$
\bigwedge_{j\neq 0} x(0, 0, j)  
$$
- end position: vertex j is somewhere on the path
$$
\bigwedge_{j\neq 0} \bigvee_{t\neq 0} x(0,t,j)
$$
- flow to neighbors: if $i \neq j$ is in the path, we need to ensure some of its neighbors are as well in the next position in time. This is a slight problem since we do not know in advance its neighbors in the spanning tree, only in the original tree. But since neighbors in the original tree are a superset, we calculate those and then ensure the given neighbor has an edge to the vertex in the spanning tree. Assume the set of neighbors of a given vertex $i$ in the original tree as $N(i)$ with elements $n^i_1, n^i_2,...$
$$
\bigwedge_{j, i \neq j, t<|V|-1} x(i,t,j) \rightarrow (x(n^i_1, t+1, j) \vee x(n^i_2, t+1, j) \vee ...)
$$
$$
\bigwedge_{j,i\neq j,n\in N(i), t<|V|-1} x(i,t,j) \wedge x(n,t+1,j) \rightarrow s(i, n) 
$$
- no 2 verteces at the same position in path:
$$
\bigwedge_{j, i_1 \neq i_2, t} x(i_1,t,j) \rightarrow \neg x(i_2,t,j)
$$
- no vertex twice in the path:
$$
\bigwedge_{j,i,t_1\neq t_2} x(i,t_1,j) \rightarrow \neg x(i,t_2,j)
$$