from ortools.linear_solver import pywraplp
import random as rand

solver = pywraplp.Solver('TSPflujo', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

# x and y are integer non-negative variables.
nodes = 6
rand.seed(42)
cost = { (i,j): rand.randint(10,100) for i in range(nodes) for j in range(nodes) if i!=j}

x = {}
for i in range(nodes):
    for j in range(nodes):
        x[i, j] = solver.BoolVar('x[%i, %i]' % (i, j))

f = {}
for i in range(nodes):
    for j in range(nodes):
        f[i, j] = solver.IntVar(0.0,solver.infinity(),'f[%i, %i]' % (i, j))

solver.Minimize(solver.Sum([cost[i,j]*x[i,j] for i in range(nodes) for j in range(nodes) if i!=j]))

for i in range(nodes):
    solver.Add(solver.Sum([x[i,j] for j in range(nodes)]) == 1)

for j in range(nodes):
    solver.Add(solver.Sum([x[i,j] for i in range(nodes)]) == 1)

for i in range(1,nodes):
    solver.Add((solver.Sum([f[i,j] for j in range(nodes)])-solver.Sum([f[j,i] for j in range(nodes)]))==1)
    #solver.Add(solver.Sum(f[i,j] for i in range(1,nodes) for j in range(1,nodes))-solver.Sum[j,i] for i in range(1,nodes) for j in range(1,nodes))
for i in range(nodes):
    for j in range(nodes):
        solver.Add(0<=f[i,j]<=(nodes-1)*x[i,j])

sol = solver.Solve()
if sol == solver.OPTIMAL:
    print('Wall time = ' + str(solver.WallTime()) + ' ms')
    print('Número de variables =', solver.NumVariables())
    print('Número de restricciones =', solver.NumConstraints())
    print('Costo total =', solver.Objective().Value())
    recorrido = '0'
    i=0
    while i != -1:
        for j in range(nodes):
            if i!=j:
                if x[i, j].solution_value() > 0:
                    recorrido += ' -c(' + str(cost[i,j]) +')-> ' + str(j)
                    aux = j
        if aux != 0:
            i = aux
        else:
            i = -1
    print(recorrido)
