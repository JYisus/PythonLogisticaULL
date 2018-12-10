from ortools.linear_solver import pywraplp
import random as rand

solver = pywraplp.Solver('TSP2', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

# x and y are integer non-negative variables.
nodes = 4
rand.seed(42)
cost = { (i,j): rand.randint(10,100) for i in range(nodes) for j in range(nodes) if i!=j}

x = {}
for i in range(nodes):
    for j in range(nodes):
        x[i, j] = solver.BoolVar('x[%i, %i]' % (i, j))
u = {}
for i in range(1,nodes):
    u[i] = solver.IntVar(1.0,solver.infinity(),'u[%i]' % (i))

solver.Minimize(solver.Sum([cost[i,j]*x[i,j] for i in range(nodes) for j in range(nodes) if i!=j]))

for i in range(nodes):
    solver.Add(solver.Sum([x[i,j] for j in range(nodes)]) == 1)

for j in range(nodes):
    solver.Add(solver.Sum([x[i,j] for i in range(nodes)]) == 1)

for i in range(1,nodes):
    for j in range(1,nodes):
        solver.Add(u[j]>=(u[i]+x[i,j]-(nodes-2)*(1-x[i,j])+(nodes-3)*x[j,i]))

sol = solver.Solve()
if sol == solver.OPTIMAL:
        print('Costo total =', solver.Objective().Value())
        recorrido = '0'
        i=0
        while i != -1:
            for j in range(nodes):
                if x[i, j].solution_value() > 0:
                    recorrido += ' -c(' + str(cost[i,j]) +')-> ' + str(j)
                    aux = j
            if aux != 0:
                i = aux
            else:
                i = -1
        print(recorrido)