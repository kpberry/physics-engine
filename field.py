class Field:
    name = None
    parent = None
    
    def __init__(self, parameter = 1, pos = PVector(0, 0), magnitude_function = lambda x: 1/x**2,\
                     constant = None):
        self.pos = pos
        self.magnitude_function = magnitude_function
        if constant != None:
            self.init_constants(parameter, constant)
        else:
            self.init_constants(parameter)
    
    def add_field(self, other):
        other.add_field(self)
    
    def calc_force(self, other):
        #to be overriden in child classes
        pass
    
    def init_constants(self):
        #to be overriden in child classes
        pass
    
    def __str__(self):
        return str(type(self)) + str(self.pos)
    
    def __repr__(self):
        return str(self)

class GravitationalField(Field):
    name = 'Gravitational'
    
    def init_constants(self, mass = 1, constant = 6.673e-1):
        self.constant = constant
        self.mass = mass
        self.magnitude_function = lambda x: 1/x**2
    
    def calc_force(self, other):
        distance = dist(self.pos.x, self.pos.y, self.pos.z, other.pos.x, other.pos.y, other.pos.z)
        return -self.constant * self.mass * other.mass * self.magnitude_function(distance)

class ElectricField(Field):
    name = 'Electric'
    
    def init_constants(self, charge = 1e-9, constant = 8.99e9):
        self.constant = constant
        self.charge = charge
    
    def calc_force(self, other):
        distance = dist(self.pos.x, self.pos.y, self.pos.z, other.pos.x, other.pos.y, other.pos.z)
        return self.constant * self.charge * other.charge * self.magnitude_function(distance)
    
class LoveField(Field):
    name = 'Love'
    
    def init_constants(self, charm = 1, constant = 1e-7):
        self.constant = constant
        self.charm = charm
        self.magnitude_function = lambda x: x ** 2
    
    def calc_force(self, other):
        distance = dist(self.pos.x, self.pos.y, self.pos.z, other.pos.x, other.pos.y, other.pos.z)
        return -self.constant * self.charm * other.charm * self.magnitude_function(distance)

class Spring(Field):
    name = 'Spring'
    
    #takes equilibrium distance as a parameter rather than
    # an intrinsic property of the constituent charge
    def init_constants(self, eq_distance = 100, constant = 1e-1):
        self.constant = constant
        self.eq_distance = eq_distance
        self.magnitude_function = lambda x: x
    
    def calc_force(self, other):
        distance = dist(self.pos.x, self.pos.y, self.pos.z, other.pos.x, other.pos.y, other.pos.z)
        self.display(other, distance)
        return -self.constant * (self.magnitude_function(distance) - self.eq_distance)/2
    
    def display(self, other, distance):
        pushStyle()
        if distance >= self.eq_distance:
            stroke(0, 0, distance - self.eq_distance)
        else:
            stroke(self.eq_distance - distance, 0, 0)
        line(self.pos.x, self.pos.y, self.pos.z, other.pos.x, other.pos.y, other.pos.z)
        popStyle()

class Fluid(Field):
    name = 'Fluid'
    parent = 'Resistive'
    
    def init_constants(self, parameter = 1, constant = 1):
        self.constant = constant
        self.parameter = parameter
        self.magnitude_function = lambda x: 1
        self.damping_function = lambda x: x ** 2
    
    def calc_force(self, other):
        distance = dist(self.pos.x, self.pos.y, self.pos.z, other.pos.x, other.pos.y, other.pos.z)
        force = -self.constant * self.magnitude_function(distance) \
        * self.damping_function(sqrt(other.velocity.x ** 2 + other.velocity.y ** 2 + other.velocity.z ** 2))
        return force
        
        

        
