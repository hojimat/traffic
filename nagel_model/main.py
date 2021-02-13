from architecture import Road, Car
from matplotlib import pyplot as plt

T = 50
X = 100
N = 50
PROB = 0.5

road = Road(X,T,p=PROB)
road.play(N)

plt.imshow(road.history)
plt.xlabel("Traffic situation")
plt.ylabel("Time period")
plt.show()

