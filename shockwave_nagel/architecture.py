import numpy as np

class Car:
    ''' A class that represents each car as an Agent '''
    def __init__(self,env,loc=0,v=1):
        self.id = len(env.cars)
        self.env = env # the road
        self.X = env.X # the road length
        self.loc = loc # own location
        self.v = v # velocity
        self.vf = env.vf
        self.floc = None #front car's location
        self.rloc = None #front red light location

    def report(self):
        self.env.status[self.loc] = 1

    def accelerate(self,by=1):
        self.v = min([(self.v + by),self.vf])

    def observe(self):
        floc = self.env.infoboard[self.loc]
        redlight = self.env.redlight
        if floc > self.loc:
            self.floc = floc
        else:
            self.floc = self.X
        if redlight:
            self.rloc = 1000
        else:
            self.rloc = self.X

    def slow_down(self):
        # observe front loc
        fdist = self.floc - self.loc
        if fdist < self.v:
            self.accelerate(by=(fdist-self.v))
        # if more than velocity slow down

    def stop_at_red(self):
        fdist = self.floc - self.loc
        rdist = self.rloc - self.loc
        if rdist > 0 and rdist < fdist:
            self.v = 0

    def move(self):
        newloc = self.loc + self.v
        if newloc <= self.X-1 and newloc < self.floc:
            self.loc = newloc
    
    def shock(self,prob):
        shock_occurs = np.random.choice([True,False],p=[prob,(1-prob)])
        if shock_occurs:
            self.accelerate(by=-1)

class Road:
    ''' A class that represents the road / environment '''
    def __init__(self,X,T,ff,vf,red,p=0.5):
        self.X = X # road length
        self.T = T
        self.N = None # number of cars
        self.ff = ff # free flow capacity (<1)
        self.vf = vf # free flow speed
        self.red = red
        self.p = p
        self.status = np.zeros(X,dtype=int) # current status
        self.history = np.zeros((X,T),dtype=int) # status archive
        self.infoboard = None
        self.redlight = False
        self.cars = [] # cars registry
    
    def populate(self,N):
        '''
        Create cars and place them on the road
        '''
        self.N = N
        locs = None
        try:
            ffcapacity = int(self.X*self.ff)
            locs = np.random.choice(range(ffcapacity),N,replace=False)
        except ValueError:
            print("More cars than road capacity.")
            return(None)

        for i in locs:
           self.cars.append(Car(loc=i,env=self)) 
           self.status[i] = 1
          

    def archive(self,t):
        self.history[:,t] = self.status
        self.status = np.zeros(self.X,dtype=int)

    def observe(self):
        locs = np.where(self.status>0)[0]
        flocs = np.roll(locs,-1)
        self.infoboard = dict(zip(locs,flocs))

    def play(self,N):
        self.populate(N)
        self.observe()
        self.archive(0)
        for t in range(1,self.T):
            if t==self.red:
                self.redlight = True
            if t==(self.red+50):
                self.redlight = False
            for car in self.cars:
                car.accelerate()
                car.observe()
                car.stop_at_red()
                car.slow_down()
                car.move()
                car.report()
            self.observe()
            self.archive(t)
