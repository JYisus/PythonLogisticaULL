from ortools.linear_solver import pywraplp
import random as rand

solver = pywraplp.Solver('TSP2', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

# x and y are integer non-negative variables.
nodes = 4
pilas = 3
q = 5
rand.seed(42)
cost_t = { (i,j): rand.randint(10,100) for i in range(nodes) for j in range(nodes) if i!=j}
cost_g = { (i,j): rand.randint(10,100) for i in range(nodes) for j in range(nodes) if i!=j}

x_t = {}
for i in range(nodes):
    for j in range(nodes):
        if i!=j:
            x_t[i, j] = solver.BoolVar('x_t[%i, %i]' % (i, j))

x_g = {}
for i in range(nodes):
    for j in range(nodes):
        if i!=j:
            x_g[i, j] = solver.BoolVar('x[%i, %i]' % (i, j))

v_t = {}
for i in range(1, nodes):
    for j in range(1, nodes):
        if i != j:
            v_t[i, j] = solver.BoolVar('v_t[%i, %i]' % (i, j))

v_g = {}
for i in range(1, nodes):
    for j in range(1, nodes):
        if i != j:
            v_g[i, j] = solver.BoolVar('v_g[%i, %i]' % (i, j))

z = {}
for i in range(1,nodes):
    for k in range(pilas):
        z[i,k] = solver.BoolVar('z[%i, %i' % (i,k))


solver.Minimize(solver.Sum([cost_t[i,j]*x_t[i,j] for i in range(nodes) for j in range(nodes) if i!=j])+solver.Sum([cost_g[i,j]*x_g[i,j] for i in range(nodes) for j in range(nodes) if i!=j]))

for i in range(nodes):
    solver.Add(solver.Sum([x_t[i,j] for j in range(nodes) if i!=j]) == 1)

for j in range(nodes):
    solver.Add(solver.Sum([x_t[i,j] for i in range(nodes) if i!=j]) == 1)

for i in range(nodes):
    solver.Add(solver.Sum([x_g[i,j] for j in range(nodes) if i!=j]) == 1)

for j in range(nodes):
    solver.Add(solver.Sum([x_g[i,j] for i in range(nodes) if i!=j]) == 1)

for i in range(1,nodes):
    for j in range(1,nodes):
        if i != j:
            solver.Add((v_t[i,j]+v_t[j,i]) == 1)
            solver.Add((v_g[i,j]+v_g[j,i]) == 1)

for i in range(1,nodes):
    for j in range(1,nodes):
        if i != j:
            for k in range(1, nodes):
                if (k != i) & (k != j):
                    solver.Add( v_t[i,j]+v_t[j,k] <= v_t[i,k]+1 )
                    solver.Add( v_g[i,j]+v_g[j,k] <= v_g[i,k]+1 )

for i in range(1,nodes):
    for j in range(1,nodes):
        if i != j:
            solver.Add(x_t[i,j] <= v_t[i,j])
            solver.Add(x_g[i,j] <= v_g[i,j])

for i in range(1,nodes):
    for k in range(pilas):
        solver.Add(z[i,k] == 1)
        solver.Add(z[i,k] <= q)

for i in range(1,nodes):
    for j in range(1,nodes):
        if i!=j:
            for k in range(pilas):
                solver.Add(v_t[i,j]+v_g[i,j]+z[i,k]+z[j,k] <= 3)

sol = solver.Solve()
if sol == solver.OPTIMAL:
        print('Costo total =', solver.Objective().Value())
        recorrido = '0'
        i=0
        while i != -1:
            for j in range(nodes):
                if i!=j:
                    if x_t[i, j].solution_value() > 0:
                        recorrido += ' -c(' + str(cost_t[i,j]) +')-> ' + str(j)
                        aux = j
            if aux != 0:
                i = aux
            else:
                i = -1
        print("T ::: " + recorrido)
        recorrido = '0'
        i=0
        while i != -1:
            for j in range(nodes):
                if i!=j:
                    if x_g[i, j].solution_value() > 0:
                        recorrido += ' -c(' + str(cost_g[i,j]) +')-> ' + str(j)
                        aux = j
            if aux != 0:
                i = aux
            else:
                i = -1
        print("G ::: " + recorrido)
