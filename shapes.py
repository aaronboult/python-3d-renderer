from matrix import matrix
import math

class transform(object):

    def __init__(self, x = 0, y = 0, z = 0, x_angle = 0, y_angle = 0, z_angle = 0, scale = 1):

        self.x = x
        self.y = y
        self.z = z

        self.scale = scale

        self.position = matrix( [ [self.x], [self.y], [self.z] ] )
        
        self.rotation = matrix( [ [x_angle], [y_angle], [z_angle] ] )

class shape(object):

    def __init__(self, obj_transform, x_rotate_rate = 0, y_rotate_rate = 0, z_rotate_rate = 0):

        self.transform = obj_transform

        self.rotation_rate = [(x_rotate_rate*math.pi)/180, (y_rotate_rate*math.pi)/180, (z_rotate_rate*math.pi)/180]
    
    def update(self):

        self.transform.rotation[0][0] += self.rotation_rate[0]
        self.transform.rotation[1][0] += self.rotation_rate[1]
        self.transform.rotation[2][0] += self.rotation_rate[2]

class cuboid(shape):

    def __init__(self, obj_transform, width, height, depth = -1, x_rotate_rate = 0, y_rotate_rate = 0, z_rotate_rate = 0):

        if depth < 0:

            depth = width

        super().__init__(obj_transform, x_rotate_rate = x_rotate_rate, y_rotate_rate = y_rotate_rate, z_rotate_rate = z_rotate_rate)

        self.width = width

        self.height = height

        self.depth = depth

        self.verticies = []

        x_offset = self.width / 2
        y_offset = self.height / 2
        z_offset = self.depth / 2

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

        self.x = x
        self.y = y
        self.z = z

        self.joined_to = []
    
    def __str__(self):

        return f"{{ {self.x}, {self.y}, {self.z} }}"
    
    def join_to(self, to_join_to):

        for vert in to_join_to:

            self.joined_to.append(vert)

    def to_matrix(self):

        return matrix(
            [
                [self.x],
                [self.y],
                [self.z]
            ]
        )