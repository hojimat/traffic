from architecture import Road, Car
from matplotlib import pyplot as plt

T = 300
X = 2000
N = 2
ff = 0.25
vf = 20
red = 40
tau = 1 # 1 time period ~ 0.1 seconds
c = 1 # sensitivity parameter

road = Road(X,T,N,ff,tau,c,vf,red)
road.play()

print(road.hist_a)
plt.contourf(road.hist_status, origin="lower")
plt.xlabel("Time period")
plt.ylabel("Traffic situation")
plt.show()
