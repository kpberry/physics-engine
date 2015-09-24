
from particle import Particle
from field import Field, ElectricField, LoveField, Fluid, Spring
from particleSystem import ParticleSystem

def setup():
    # sets up the particle system, display variables, and the camera x and y
    global ps, static, bg, cx, cy, cz, recording
    bg = 200
    recording = False
    background(bg)
    size(1000, 600, P3D)
    sphereDetail(10)
    cx, cy, cz = 1024, 512, 512
    static = False
    ps = ParticleSystem(False)
    switch = -1
    
    #change this num variable to add a lattice of particles with num squared members
    num = 0
    for i in range(-num, num):
        for j in range(-num, num):
            ps.add_particle(Particle(pos=PVector(i * 10, j * 10, (i + j) * switch * 10),
                                     eq_distance=200,
                                     vel=PVector(switch, -switch), 
                                     mass=100, charm=10, 
                                     charge=0.001 * switch, 
                                     radius=5, trail=1000))
            switch = -switch
        switch = -switch
    switch = -1
    
    #for the rest of these loops, changing the 0s spawns various particles
    for i in range(0):
        for j in range(0):
            ps.add_particle(Particle(pos=PVector(i * 40, j * 40, (i + j) * switch * 20),
                                     vel=PVector(switch, -switch),
                                     mass=100, charm=10,
                                     charge=0.001 * switch,
                                     radius=5, trail=100))
            switch = -switch
        switch = -switch
    for i in range(0):
        ps.add_particle(Particle(pos=PVector(random(-1, 1), random(-1, 1), random(-1, 1)),
                                 vel=PVector(0, 0, 0),
                                 eq_distance=200, mass=10,
                                 radius=5, trail=0))
    for i in range(0):
        ps.add_particle(Particle(mass=10, 
                                 pos=PVector(random(-50, 50), random(-50, 50), random(-100, 100)),
                                 vel=PVector(0, 5),
                                 radius=10,
                                 trail=1000))
    for i in range(0):
        ps.add_particle(Particle(mass = 1000,
                                 pos = PVector(0, 0, 0),
                                 vel = PVector(0, -0.1),
                                 radius = 10,
                                 trail = 1000))
    for i in range(0):
        ps.add_particle(Particle(pos=PVector(random(-100, 100), random(-100, 100), random(-300, 300)),
                                   vel = PVector(0, 0),
                                   mass=100,
                                   charm = 1,
                                   charge = random(-0.01, 0.01),
                                   radius = 5,
                                   trail = 1000))
    for i in range(20):
        ps.add_particle(Particle(pos=PVector(random(-100, 100), random(-100, 100), random(-300, 300)),
                                   vel = PVector(0, 0),
                                   mass=50,
                                   charm = 5,
                                   charge = random(-0.01, 0.01),
                                   radius = 5,
                                   trail = 100))
    #Uncomment this to add a resistive fluid force to the particle system
    #ps.add_field(Fluid(constant=5))
    
    #the reduction divides all forces by a given factor, then performs
    #the ps.act() method factor times per frame
    #e.g. a reduction of ten means that there will be ten time updates
    #per frame, but the updates will each be ten times as small, which
    #aids in precision
    ps.set_reduction(1)

def draw():
    global static, cx, cy, recording
    if keyPressed:
        if key == 'l':
            static = True
            blur = False
        if key == 'j':
            static = False
            blur = False
        if key == 'i':
            ps.make_invisible()
        if key == 'k':
            recording = False
        if key == 'u':
            ps.make_visible()
    if static:
        pass
    else:
        background(bg)
    ps.act()
    #ps.set_rotation(PVector(0, frameCount / 60.0))
    if frameCount > 0:
        recording = False
    if frameCount < 0:
        ps.make_visible()
    if recording:
        saveFrame('frames/####.png')
    

