from field import Spring

class ParticleSystem:
    def __init__(self, visible_forces = False):
        self.particles = []
        self.abstract_fields = []
        #center of mass
        self.cmx, self.cmy, self.cmz = 0, 0, 0
        #used to initialize center of mass for translation purposes
        #center of charge
        self.cqx, self.cqy = 0, 0
        self.reduction = 1.0
        self.rotation = PVector(0, 0)
        self.visible_forces = visible_forces
    
    def add_particle(self, particle):
        i = 0
        while i < len(self.particles):
            for j in particle.internal_fields:
                self.particles[i].add_field(j)
            for j in self.particles[i].internal_fields:
                particle.add_field(j)
            for j in self.abstract_fields:
                particle.add_field(j)
            i += 1
        self.particles.append(particle)

    
    def add_field(self, field):
        i = 0
        while i < len(self.particles):
            self.particles[i].add_field(field)
            i += 1
        self.abstract_fields.append(field)
    
    def add_spring(self, index1, index2, eq_distance = 200, k = 1e-1):
        try:
            self.particles[index1].add_spring(self.particles[index2], eq_distance, k)
        except:
            pass
    
    #still buggy
    def add_rod(self, index1, index2):
        try:
            self.particles[index1].add_spring(self.particles[index2],\
                                              dist(self.particles[index1].pos.x, self.particles[index1].pos.y, self.particles[index1].pos.z,\
                                                   self.particles[index2].pos.x, self.particles[index2].pos.y, self.particles[index2].pos.z),\
                                                   10)
        except:
            pass
        
    def act(self):
        pushMatrix()
        translate(width/2, height/2)
        rotateX(self.rotation.x)
        rotateY(self.rotation.y)
        for j in range(int(self.reduction)):
            for i in self.particles:
                #force gets divided by the reduction factor
                i.act(self.visible_forces, self.reduction)
        for i in self.particles:
            i.update_position()
        popMatrix()
            
    def delta_cm(self):
        prev_x = self.cmx
        prev_y = self.cmy
        prev_z = self.cmz
        x = 0
        y = 0
        z = 0
        m = 0
        for i in self.particles:
            x += i.pos.x * i.mass
            y += i.pos.y * i.mass
            z += i.pos.z * i.mass
            m += i.mass
          
        x /= m
        y /= m
        z /= m
        self.cmx = x
        self.cmy = y
        self.cmz = z
        return sqrt((x - prev_x) ** 2 + (y - prev_y) ** 2 + (z - prev_z) ** 2)
    
    def get_momentum(self):
        momentum_x, momentum_y, momentum_z = 0, 0, 0
        for i in self.particles:
            momentum_x += i.velocity.x * i.mass
            momentum_y += i.velocity.y * i.mass
            momentum_z += i.velocity.z * i.mass
        return PVector(momentum_x, momentum_y, momentum_z)
    
    def get_ke(self):
        p = self.get_momentum()
        return (p.x**2 + p.y**2 + p.z**2)/2
    
    def display_ke(self):
        text('Kinetic Energy of System: ' + str(self.get_ke()), 20, 50)
    
    def get_pe(self):
        pass
    
    def display_cm(self):
        text('Velocity of Center of Mass: ' + str(self.delta_cm()), 20, 20)
    
    def make_visible(self):
        self.visible_forces = True
        
    def make_invisible(self):
        self.visible_forces = False
    
    def set_reduction(self, reduction):
        self.reduction = float(reduction)
    
    def set_rotation(self, rotation):
        self.rotation = rotation
            
