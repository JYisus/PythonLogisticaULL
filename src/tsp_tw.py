from ortools.linear_solver import pywraplp
import random as rand

solver = pywraplp.Solver('TSP Time Windows', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

# x and y are integer non-negative variables.
nodes = 5
rand.seed(42)
cost = { (i,j): rand.randint(1,10) for i in range(nodes) for j in range(nodes) if i!=j}

""" EJEMPLO A MANO
cost = {(i,j): 0 for i in range(nodes) for j in range(nodes) if i!=j }
cost[0,1] = 6
cost[0,2] = 3
cost[0,3] = 4
cost[0,4] = 4
cost[1,0] = 2
cost[1,2] = 1
cost[1,3] = 3
cost[1,4] = 3
cost[2,0] = 7
cost[2,1] = 5
cost[2,3] = 4
cost[2,4] = 4
cost[3,0] = 8
cost[3,1] = 2
cost[3,2] = 4
cost[3,4] = 4
cost[4,0] = 4
cost[4,1] = 4
cost[4,2] = 4
cost[4,4] = 4

e = [1400, 900, 1200, 800, 700]
l = [1400, 1100, 1300, 1000, 900]
t = {(i,j): 100 for i in range(nodes) for j in range(nodes) if i!=j}
s ={i: 100 for i in range(nodes)} """
#print(cost)
# early time
e = {i: rand.randint(800, 1900) for i in range(nodes)}
""" e = []
for i in range(1,nodes):
    e.append(rand.randint(800,1900)) """
# print("Early times: " + str(e))
# late time
l = []
for i in range(nodes):
    aux = rand.randint(900,2000)
    while aux <= e[i]:
        aux = rand.randint(900,2000)
    l.append(aux)

e[0] = l[0]
# print("Late times: " + str(l))

# service time
s ={i: rand.randint(100,100) for i in range(nodes)}

""" s = []
for i in range(1,nodes):
    s.append(rand.randint(100,200)) """
# print("Service times: " + str(s))
# tiempos de ruta
t = {(i,j): rand.randint(100,100) for i in range(nodes) for j in range(nodes) if i!=j}
""" t = []
for i in range(nodes):
    aux = []
    for j in range(nodes):
        aux.append(rand.randint(100,200))
    t.append(aux) """
# print("Tiempos de ruta: " + str(t))

e = [1400, 900, 1200, 800, 700]
l = [1400, 1100, 1300, 1000, 900]
t = {(i,j): 100 for i in range(nodes) for j in range(nodes) if i!=j}
s ={i: 100 for i in range(nodes)}

x = {}
for i in range(nodes):
    for j in range(nodes):
        if i!=j:
            x[i, j] = solver.BoolVar('x[%i, %i]' % (i, j))

u = {}
for i in range(1,nodes):
    u[i] = solver.IntVar(1.0,solver.infinity(),'u[%i]' % (i))

solver.Minimize(solver.Sum([cost[i,j]*x[i,j] for i in range(nodes) for j in range(nodes) if i!=j]))

for i in range(nodes):
    solver.Add(solver.Sum([x[i,j] for j in range(nodes) if i!=j]) == 1)

for j in range(nodes):
    solver.Add(solver.Sum([x[i,j] for i in range(nodes) if i!=j]) == 1)

for i in range(1,nodes):
    solver.Add(e[i]<=u[i]<=l[i])

for i in range(1,nodes):
    for j in range(1,nodes):
        if i!=j:
            solver.Add(u[j]>=u[i]+(s[i]+t[i,j])*x[i,j]-(l[i]-e[j])*(1-x[i,j]))

sol = solver.Solve()
if sol == solver.OPTIMAL:
    print('Costo total =', solver.Objective().Value())
    recorrido = '0'
    print(x)
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