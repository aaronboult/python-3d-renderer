from geometry import matrix, vector
import math

class transform(object):

    def __init__(self, x = 0, y = 0, z = 0, x_angle = 0, y_angle = 0, z_angle = 0, scale = None, x_scale = 1, y_scale = 1, z_scale = 1):

        if scale != None:

            x_scale = scale if x_scale == 1 else x_scale
            y_scale = scale if y_scale == 1 else y_scale
            z_scale = scale if z_scale == 1 else z_scale

        self.position = vector([x, y, z])

        self.scale = vector([x_scale, y_scale, z_scale])

        # Convert angles in degrees to radians
        self.rotation = vector([math.pi*x_angle/180, math.pi*y_angle/180, math.pi*z_angle/180])

class shape(object):

    def __init__(self, obj_transform, x_rotate_rate = 0, y_rotate_rate = 0, z_rotate_rate = 0):

        self.transform = obj_transform

        self.rotation_rate = vector([math.pi*x_rotate_rate/180, math.pi*y_rotate_rate/180, math.pi*z_rotate_rate/180])
    
    def update(self):

        self.transform.rotation.x += self.rotation_rate.x
        self.transform.rotation.y += self.rotation_rate.y
        self.transform.rotation.z += self.rotation_rate.z

class cuboid(shape):

    def __init__(self, obj_transform, x_rotate_rate = 0, y_rotate_rate = 0, z_rotate_rate = 0):

        super().__init__(obj_transform, x_rotate_rate = x_rotate_rate, y_rotate_rate = y_rotate_rate, z_rotate_rate = z_rotate_rate)

        self.verticies = []

        x_offset = 1
        y_offset = 1
        z_offset = 1

        self.verticies.append(vertex(-x_offset, y_offset, -z_offset)) # Back top left
        self.verticies.append(vertex(-x_offset, y_offset, z_offset)) # Front top left
        self.verticies.append(vertex(x_offset, y_offset, -z_offset)) # Back top right
        self.verticies.append(vertex(x_offset, y_offset, z_offset)) # Front top right
        self.verticies.append(vertex(-x_offset, -y_offset, -z_offset)) # Back bottom left
        self.verticies.append(vertex(-x_offset, -y_offset, z_offset)) # Front bottom left
        self.verticies.append(vertex(x_offset, -y_offset, -z_offset)) # Back bottom right
        self.verticies.append(vertex(x_offset, -y_offset, z_offset)) # Front bottom right

        self.verticies[0].join_to([1, 2, 4]) # Join BTL to FTL, BTR, BBL
        self.verticies[1].join_to([0, 3, 5])
        self.verticies[2].join_to([0, 3, 6])
        self.verticies[3].join_to([1, 2, 7])
        self.verticies[4].join_to([0, 5, 6])
        self.verticies[5].join_to([1, 4, 7])
        self.verticies[6].join_to([2, 4, 7])
        self.verticies[7].join_to([3, 5, 6])
    
    def __str__(self):

        s = "Shape: Cuboid\nVerticies:"

        for v in self.verticies:

            s += f"{v}\n"
        
        return s

class vertex(object):

    def __init__(self, x, y, z):

        self.position = vector([x, y, z])

        self.joined_to = []
    
    def __str__(self):

        return f"{{ {self.position.x}, {self.position.y}, {self.position.z} }}"
    
    def join_to(self, to_join_to):

        for vert in to_join_to:

            self.joined_to.append(vert)