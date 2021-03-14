import numpy as np

class Car:
    ''' A class that represents each car as an Agent '''
    def __init__(self,env,loc=0,v=1,a=1):
        self.id = len(env.cars)
        self.env = env # the road
        self.x = x # own location
        self.v = v # velocity
        self.a = a # acceleration plan vector
        self.vf = env.vf
        self.tau = env.tau # reaction time
        self.c = env.c
        self.xL = None # Leader's location
        self.vF = None # Follower's velocity tau periods ago
        self.vL = None # Leader's velocity tau periods ago

    def report(self):
        status = {"x": self.x, "v": self.v}
        self.env.status[self.id] = status
        #self.env.a[self.id] = self.a

    def observe(self):
        #xL = self.env.infoboard[self.x]

        if xL > self.x:
            self.xL = xL
        else:
            self.xL = self.env.X

    def set_velocity(self):
        vL = self.vL
        vF = self.vF
        v = self.v
        c = self.c
        tau = self.tau
        # linear car following model
        self.a = (c / tau) * (vL - vF)

    def move(self):
        newloc = self.x + self.v
        if newloc <= self.env.X-1 and newloc < self.xL:
            self.x = newloc

class Road:
    ''' A class that represents the road / environment '''
    def __init__(self,X,T,N,cap,tau,c,vf,p=0.0):
        self.X = X # road length
        self.T = T
        self.N = N # number of cars
        self.cap = cap # free flow capacity
        self.vf = vf # free flow speed PRETTY SURE SHOULD BE ENDOGENOUS
        self.p = p
        self.tau = tau
        self.c = c
        self.status = [0]*X # current status
        self.a = np.zeros(N)
        self.v = np.zeros(N)
        self.hist_status = np.zeros((X,T),dtype=int) # road status hist
        self.hist_v = np.zeros((N,T),dtype=int) # velocity hist
        self.hist_a = np.zeros((N,T),dtype=int) # acceleration hist
        self.infoboard = None
        self.cars = [] # cars registry
    
    def populate(self):
        '''
        Create cars and place them on the road
        '''
        N = self.N
        locs = None
        cap = self.cap
        if N > cap:
            print("More cars than road capacity")
            return None
        locs = np.random.choice(range(cap),N,replace=False)

        for i in locs:
            car = Car(x=i,env=self)
            self.cars.append(car)
            self.status[i] = {"id":car.id,"v":car.v}

    def archive(self,t):
        self.hist_status[:,t] = self.status
        self.hist_a[:,t] = self.a
        self.status = np.zeros(self.X,dtype=int)
        self.a = np.zeros(self.N)

    def scan(self):
        #locs = np.where(self.status>0)[0]
        #xLs = np.roll(locs,-1)
        #self.infoboard = dict(zip(locs,xLs))

    def play(self):
        self.populate()
        self.scan()
        self.archive(0)
        for t in range(1,self.T):
            for car in self.cars:
                car.observe()
                car.set_velocity()
                car.move()
                car.report()
            self.scan()
            self.archive(t)
