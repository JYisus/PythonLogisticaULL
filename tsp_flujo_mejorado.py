from ortools.linear_solver import pywraplp
import random as rand

solver = pywraplp.Solver('TSPflujo', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

# x and y are integer non-negative variables.
nodes = 4
cost = []
rand.seed(42)
for i in range(nodes):
    row = []
    for j in range(nodes):
        row.append(rand.randint(10,100))
    cost.append(row)
for i in range(nodes):
    cost[i][i] = 200
# print(cost)
# cost = [[0,10,15,20],
#    [10,0,35,25],
#    [15,35,0,30],
#    [20,25,30,0]]
x = {}
for i in range(nodes):
    for j in range(nodes):
        x[i, j] = solver.BoolVar('x[%i, %i]' % (i, j))
f = {}
for i in range(nodes):
    for j in range(nodes):
        f[i, j] = solver.IntVar(0.0,solver.infinity(),'f[%i, %i]' % (i, j))

solver.Minimize(solver.Sum([cost[i][j]*x[i,j] for i in range(nodes) for j in range(nodes)]))

for i in range(nodes):
    solver.Add(solver.Sum([x[i,j] for j in range(nodes)]) == 1)

for j in range(nodes):
    solver.Add(solver.Sum([x[i,j] for i in range(nodes)]) == 1)

for i in range(1,nodes):
    solver.Add((solver.Sum([f[i,j] for j in range(nodes)])-solver.Sum([f[j,i] for j in range(nodes)]))==1)
    #solver.Add(solver.Sum(f[i,j] for i in range(1,nodes) for j in range(1,nodes))-solver.Sum[j,i] for i in range(1,nodes) for j in range(1,nodes))
for i in range(1,nodes):
    for j in range(1,nodes):
        solver.Add(x[i,j]<=f[i,j]<=(nodes-2)*x[i,j])

for i in range(1,nodes):
    solver.Add(f[i,0]==(nodes-1)*x[i,0])
for i in range(1,nodes):
    solver.Add(f[0,i]==0)

sol = solver.Solve()
if sol == solver.OPTIMAL:
        print('Costo total =', solver.Objective().Value())
        recorrido = '0'
        i=0
        while i != -1:
            for j in range(nodes):
                if x[i, j].solution_value() > 0:
                    recorrido += ' -c(' + str(cost[i][j]) +')-> ' + str(j)
                    aux = j
            if aux != 0:
                i = aux
            else:
                i = -1
        print(recorrido)
