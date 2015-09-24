from field import Field, GravitationalField, ElectricField, LoveField, Spring, Fluid

class Particle:
    def __init__(self, mass = 1, charge = 0, charm = 0, eq_distance = None, pos = PVector(0, 0, 0),\
                      vel = PVector(0, 0, 0), radius = 10, c = None, trail = 200):
        self.mass = mass
        self.charge = charge
        self.charm = charm
        self.eq_distance = eq_distance
        self.pos = pos
        self.temp_pos = pos
        self.fields = []
        if self.eq_distance != None:
            self.internal_fields = [GravitationalField(self.mass, pos = self.pos), \
                                ElectricField(self.charge, pos = self.pos), 
                                LoveField(self.charm, pos = self.pos),
                                Spring(self.eq_distance, pos = self.pos)]
        else:
            self.internal_fields = [GravitationalField(self.mass, pos = self.pos), \
                                ElectricField(self.charge, pos = self.pos), 
                                LoveField(self.charm, pos = self.pos)]                       
        self.resistive_fields = []
        self.velocity = vel
        self.radius = radius
        if c == None:
            self.r = charge * 8.99e9
            self.g = charm * 100
            self.b = -charge * 8.99e9
            self.c = color(self.r, self.g, self.b)
        else:
            self.c = c
        self.lines = []
        self.trail = trail
        
    def act(self, visible_forces = False, reduction = 1.0):
        self.accelerate(reduction, visible_forces)
        self.move()
        self.display()
    
    def add_field(self, other):
        self.fields.append(other)
    
    def add_internal_field(self, other):
        self.internal_fields.append(other)
    
    def add_spring(self, other, eq_distance = 200, k = 1e-1):
        spring1 = Spring(eq_distance, pos = self.pos, constant = k)
        spring2 = Spring(eq_distance, pos = other.pos, constant = k)
        self.internal_fields.append(spring1)
        self.fields.append(spring2)
        other.add_internal_field(spring2)
        other.add_field(spring1)
    
    def move(self, reduction = 1.0):
        self.temp_pos = PVector(self.pos.x + self.velocity.x/reduction,\
                           self.pos.y + self.velocity.y/reduction,
                           self.pos.z + self.velocity.z/reduction)
    
    def update_position(self):
        if len(self.lines) > self.trail:
            self.lines = self.lines[1:]
        self.lines.append([self.pos.x, self.pos.y, self.pos.z,\
                          self.temp_pos.x, self.temp_pos.y, self.temp_pos.z])
        self.pos = self.temp_pos    
        i = 0
        while i < len(self.internal_fields):
            self.internal_fields[i].pos = PVector(self.pos.x,\
                           self.pos.y, self.pos.z)
            i += 1 
    
    def display(self):
        pushStyle()
        pushMatrix()
        noFill()
        stroke(self.c)
        translate(self.pos.x, self.pos.y, self.pos.z)
        sphere(self.radius)
        popMatrix()
        stroke(0)
        for i in self.lines:
            line(i[0], i[1], i[2], i[3], i[4], i[5])
        popStyle()
            
    def accelerate(self, reduction = 1.0, visible = False):
        force = 0
        distance = 0
        acc_x = 0
        acc_y = 0
        acc_z = 0
        for i in self.fields:
            distance = dist(self.pos.x, self.pos.y, self.pos.z, i.pos.x, i.pos.y, i.pos.z)
            if distance < 2 * self.radius:
                distance = 2 * self.radius
            #this could be handled more generally, I'm sure.
            if i.parent == 'Resistive':
                force = i.calc_force(self) / reduction
                if self.velocity.mag() != 0:
                    d_x = 1.0 * force * self.velocity.x / self.velocity.mag()
                    d_y = 1.0 * force * self.velocity.y / self.velocity.mag()
                    d_z = 1.0 * force * self.velocity.z / self.velocity.mag()
                    if abs(d_x/self.mass) >= abs(self.velocity.x):
                        d_x, self.velocity.x = 0, 0
                    if abs(d_y/self.mass) >= abs(self.velocity.y):
                        d_y, self.velocity.y = 0, 0
                    if abs(d_z/self.mass) >= abs(self.velocity.z):
                        d_z, self.velocity.z = 0, 0
                else:
                    d_x = 0
                    d_y = 0
                    d_z = 0
                distance = 1
            else:
                force = i.calc_force(self) / reduction
                d_x = 1.0 * force * (self.pos.x - i.pos.x)
                d_y = 1.0 * force * (self.pos.y - i.pos.y)
                d_z = 1.0 * force * (self.pos.z - i.pos.z)
            if visible:
                pushStyle()
                stroke(0, 40)
                line(self.pos.x, self.pos.y, self.pos.z, self.pos.x + d_x, self.pos.y + d_y, self.pos.z + d_z)
                popStyle()
            acc_x += d_x / self.mass / distance
            acc_y += d_y / self.mass / distance
            acc_z += d_z / self.mass / distance
        self.velocity = PVector(self.velocity.x + acc_x, self.velocity.y + acc_y, self.velocity.z + acc_z)            
    
    
