from ortools.linear_solver import pywraplp
import random as rand

solver = pywraplp.Solver('TSPrecogidasYEntregas1Mercancia', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

nodes = 6
cost = []
rand.seed(42)
for i in range(nodes):
    row = []
    for j in range(nodes):
        row.append(rand.randint(10,100))
    cost.append(row)
for i in range(nodes):
    cost[i][i] = 200

# Demandas
aux = 0
d = []
for i in range(1,nodes):
    x = rand.randint(-10,10)
    d.append(x)
    aux+=x
d.append(-aux)
# NOTA
# Al hacerlo aleatorio, para saber la demanda del primer nodo se está
# haciendo una suma de la demanda de todos los nodos y luego poniéndose
# la inversa de este número como la demanda del almacén.
# Por esto hay que controlar manualmente la Q (carga máxima del camión),
# pues esta ha de ser mayor que las demandas y la demanda del almacen
# puede ser muy alta por lo previamente explicado.

print(d)
# Carga máxima del camión
Q = 23

x = {}
for i in range(nodes):
    for j in range(nodes):
        x[i, j] = solver.BoolVar('x[%i, %i]' % (i, j))
f = {}
for i in range(nodes):
    for j in range(nodes):
        f[i, j] = solver.IntVar(0.0,solver.infinity(),'f[%i, %i]' % (i, j))
u = {}
for i in range(1,nodes):
    u[i] = solver.IntVar(1.0,solver.infinity(),'u[%i]' % (i))

solver.Minimize(solver.Sum([cost[i][j]*x[i,j] for i in range(nodes) for j in range(nodes)]))

for i in range(nodes):
    solver.Add(solver.Sum([x[i,j] for j in range(nodes)]) == 1)

for j in range(nodes):
    solver.Add(solver.Sum([x[i,j] for i in range(nodes)]) == 1)

for i in range(1,nodes):
    for j in range(1,nodes):
        solver.Add(u[j]>=(u[i]+x[i,j]-(nodes-2)*(1-x[i,j])+(nodes-3)*x[j,i]))

for i in range(nodes):
    solver.Add((solver.Sum([f[j,i] for j in range(nodes)])-solver.Sum([f[i,j] for j in range(nodes)])) == d[i])
    #solver.Add(solver.Sum(f[i,j] for i in range(1,nodes) for j in range(1,nodes))-solver.Sum[j,i] for i in range(1,nodes) for j in range(1,nodes))
for i in range(nodes):
    for j in range(nodes):
        solver.Add(0<=f[i,j]<=Q*x[i,j])

sol = solver.Solve()
if sol == solver.OPTIMAL:
        print('Costo total =', solver.Objective().Value())
        recorrido = '0'
        i=0
        while i != -1:
            for j in range(nodes):
                if x[i, j].solution_value() > 0:
                    """ recorrido += ' -c(' + str(cost[i][j]) +')-> ' + str(j) """
                    recorrido += ' --f(' + str(f[i,j].solution_value()) +'),c(' + str(cost[i][j]) +')--> ' + str(j)
                    aux = j
            if aux != 0:
                i = aux
            else:
                i = -1
        print(recorrido)
