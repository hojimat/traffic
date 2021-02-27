from architecture import Road, Car
from matplotlib import pyplot as plt

T = 300
X = 2000
N = 20
ff = 0.25
vf = 20
red = 40
PROB = 0.0

road = Road(X,T,ff,vf,red,p=PROB)
road.play(N)

plt.contourf(road.history, origin="lower")
plt.xlabel("Time period")
plt.ylabel("Traffic situation")
plt.show()

