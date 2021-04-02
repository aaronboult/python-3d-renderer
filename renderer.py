import os
import pygame
import math
from geometry import matrix, vector
import shapes

class renderer(object):

    def __init__(self, resolutionX = 400, resolutionY = 400, frame_rate = 60):

        self.screen = pygame.display.set_mode([resolutionX, resolutionY])

        self.resolutionX = resolutionX

        self.resolutionY = resolutionY

        self.open = False

        self.objects = []

        self.camera_position = vector([0, 0, 0])

        self.camera_rotation = vector([0, 0, 0])

        # Top left and bottom right corners
        self.camera_view_plane = (
            (-1, 1),
            (1, -1)
        )

        self.camera_view_plane_z = -1

        self.frame_rate = frame_rate

        self.clock = pygame.time.Clock()

        os.environ["SDL_VIDEO_CENTERED"] = '1'

        pygame.init()

    def show(self):

        self.open = True

        while self.open:

            self.clock.tick(self.frame_rate)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    self.open = False
            
            self.screen.fill((255, 255, 255))

            self.update_shape()

            pygame.display.update()

            pygame.display.set_caption("3D Projection")
    
    def update_shape(self):

        for obj in self.objects:

            coord_cache = {}

            for i in range(len(obj.verticies)):
                
                coords = self.calculate_projection(obj.verticies[i].position, obj.transform.scale, obj.transform.position, obj.transform.rotation)

                coord_cache[i] = coords
                
                pygame.draw.circle(self.screen, (0, 0, 255), coords, 1)

            for vertex_index in range(len(obj.verticies)):

                for connection in obj.verticies[vertex_index].joined_to:
                    
                    pygame.draw.line(self.screen, (0, 0, 0), coord_cache[vertex_index], coord_cache[connection], 1)
            
            obj.update()

    def calculate_projection(self, point, scale, position, rotation):

        # reference: https://en.wikipedia.org/wiki/3D_projection#Mathematical_formula
    
        d = point * scale # Scale the point
        d = renderer.calculate_rotation_matrix(rotation) * d # Rotate point about origin based on rotation
        d = d + position - self.camera_position # Adjust point position relative to camera and based on world position

        d_x = d[0]
        d_y = d[1]
        d_z = d[2]
        recording_size_x = self.camera_view_plane[1][0] - self.camera_view_plane[0][0]
        recording_size_y = self.camera_view_plane[1][1] - self.camera_view_plane[0][1]

        x = 0
        y = 0

        if d_z != 0:

            x = (d_x * self.resolutionX) / (d_z * recording_size_x) * self.camera_view_plane_z
            y = (d_y * self.resolutionY) / (d_z * recording_size_y) * self.camera_view_plane_z

        return (self.resolutionX // 2 + int(x), self.resolutionY // 2 + int(y))
    
    def calculate_x_rotation_matrix(x_angle):

        return matrix(
            [
                [1, 0, 0],
                [0, math.cos(x_angle), -math.sin(x_angle)],
                [0, math.sin(x_angle), math.cos(x_angle)]
            ]
        )
    
    def calculate_y_rotation_matrix(y_angle):

        return matrix(
            [
                [math.cos(y_angle), 0, -math.sin(y_angle)],
                [0, 1, 0],
                [math.sin(y_angle), 0, math.cos(y_angle)]
            ]
        )
    
    def calculate_z_rotation_matrix(z_angle):

        return matrix(
            [
                [math.cos(z_angle), -math.sin(z_angle), 0],
                [math.sin(z_angle), math.cos(z_angle), 0],
                [0, 0, 1]
            ]
        )
        
    def calculate_rotation_matrix(angles):

        x_angle = angles[0]
        y_angle = angles[1]
        z_angle = angles[2]

        return renderer.calculate_x_rotation_matrix(z_angle) * renderer.calculate_y_rotation_matrix(y_angle) * renderer.calculate_z_rotation_matrix(x_angle)

if __name__ == "__main__":

    r = renderer()

    my_transform = shapes.transform(z=-10, x_scale=1, y_scale=5, z_scale=1, y_angle=0)
    my_shape = shapes.cuboid(my_transform, x_rotate_rate = 0, y_rotate_rate = 1, z_rotate_rate = 0)
    r.objects.append(my_shape)

    my_transform = shapes.transform(x=-10, z=-20, x_scale=1, y_scale=1, z_scale=1, y_angle=0)
    my_shape = shapes.cuboid(my_transform, x_rotate_rate = 0, y_rotate_rate = 0, z_rotate_rate = 1)
    r.objects.append(my_shape)

    r.show()