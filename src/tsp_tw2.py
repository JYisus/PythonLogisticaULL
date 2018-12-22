from ortools.linear_solver import pywraplp
import random as rand

solver = pywraplp.Solver('TSP Time Windows', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

# x and y are integer non-negative variables.
nodes = 3
rand.seed(42)
cost = { (i,j): rand.randint(10,100) for i in range(nodes) for j in range(nodes) if i!=j}
# early time
e = {i: rand.randint(800, 1900) for i in range(nodes)}
""" e = []
for i in range(1,nodes):
    e.append(rand.randint(800,1900)) """
print("Early times: " + str(e))
# late time
l = []
for i in range(nodes):
    aux = rand.randint(900,2000)
    while aux <= e[i]:
        aux = rand.randint(900,2000)
    l.append(aux)
l[0] = e[0]
print("Late times: " + str(l))
# service time
s ={i: rand.randint(1,5) for i in range(nodes)}

""" s = []
for i in range(1,nodes):
    s.append(rand.randint(100,200)) """
print("Service times: " + str(s))
# tiempos de ruta
t = {(i,j): rand.randint(1,5) for i in range(nodes) for j in range(nodes) if i!=j}
""" t = []
for i in range(nodes):
    aux = []
    for j in range(nodes):
        aux.append(rand.randint(100,200))
    t.append(aux) """
# print("Tiempos de ruta: " + str(t))

x = {}
for i in range(nodes):
    for j in range(nodes):
        if i!=j:
            x[i, j] = solver.BoolVar('x[%i, %i]' % (i, j))
f = {}
for i in range(nodes):
    for j in range(nodes):
        if i!=j:
            f[i, j] = solver.IntVar(0.0,solver.infinity(),'f[%i, %i]' % (i, j))

solver.Minimize(solver.Sum([cost[i,j]*x[i,j] for i in range(nodes) for j in range(nodes) if i!=j]))

for i in range(nodes):
    solver.Add(solver.Sum([x[i,j] for j in range(nodes) if i!=j]) == 1)

for j in range(nodes):
    solver.Add(solver.Sum([x[i,j] for i in range(nodes) if i!=j]) == 1)

for i in range(1,nodes):
    solver.Add((solver.Sum([f[i,j] for j in range(nodes) if i!=j])-solver.Sum([f[j,i] for j in range(nodes) if i!=j]))==1)

for i in range(nodes):
    for j in range(nodes):
        if i!=j:
            solver.Add((0<=f[i,j]<=(2000)*x[i,j]))

for i in range(1,nodes):
    solver.Add((e[i] <= solver.Sum(f[i,j] for j in range(1,nodes) if i!=j) <=l[i-1]))

for i in range(1,nodes):
    solver.Add((solver.Sum(f[i,j] for j in range(1,nodes) if i!=j) >= solver.Sum((f[k,i]+(s[k]+t[k,i])*x[k,i]) for k in range(1,nodes) if i!=k)))

""" for i in range(1, nodes):
    solver.Add(e[i]<=u[i]<=l[i-1])

for i in range(1,nodes):
    for j in range(1,nodes):
        if i!=j:
            solver.Add(u[j]>=(u[i]+(s[i]+t[i,j])*x[i,j]-(max(l)-min(l)-min(s))*(1-x[i,j]))) """

sol = solver.Solve()
if sol == solver.OPTIMAL:
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