import numpy as np

class Car:
    ''' A class that represents each car as an Agent '''
    def __init__(self,env,loc=0,v=0):
        self.id = len(env.cars)
        self.env = env # the road
        self.X = env.X # the road length
        self.loc = loc # own location
        self.v = v # velocity
        self.floc = None #front car's location

    def report(self):
        self.env.status[self.loc] = 1

    def observe(self):
        self.floc = self.env.infoboard[self.loc]

    def accelerate(self,by=1):
        self.v = min([(self.v + by),self.X])

    def slow_down(self):
        # observe front loc
        fdist = (self.floc - self.loc) % self.X
        if fdist < self.v:
            self.accelerate(by=(fdist-self.v))
        # if more than velocity slow down

    def move(self):
        self.loc = (self.loc + self.v) % self.X
        

class Road:
    ''' A class that represents the road / environment '''
    def __init__(self,X,T):
        self.X = X # road length
        self.T = T
        self.N = None # number of cars
        self.status = np.zeros(X,dtype=int) # current status
        self.history = np.zeros((T,X),dtype=int) # status archive
        self.infoboard = None
        self.cars = [] # cars registry
    
    def populate(self,N):
        '''
        Create cars and place them on the road
        '''
        self.N = N
        locs = None
        try:
            locs = np.random.choice(range(self.X),N,replace=False)
        except ValueError:
            print("More cars than road capacity.")
            return(None)

        for i in locs:
           self.cars.append(Car(loc=i,env=self)) 
           self.status[i] = 1
          

    def archive(self,t):
        self.history[t,:] = self.status
        self.status = np.zeros(self.X,dtype=int)

    def observe(self):
        locs = np.where(self.status>0)[0]
        flocs = np.roll(locs,-1)
        self.infoboard = dict(zip(locs,flocs))

    def play(self,N):
        self.populate(N)
        self.observe()
        print(self.status)
        print(self.infoboard)
        self.archive(0)
        for t in range(1,self.T):
            print(f"time={t}")
            for car in self.cars:
                car.accelerate()
                car.observe()
                car.slow_down()
                car.move()
                car.report()
            print(self.status)
            print(self.infoboard)
            self.observe()
            self.archive(t)
