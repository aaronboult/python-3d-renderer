import os
import pygame
from math import sin, cos
from matrix import matrix
import shapes

class renderer(object):

    def __init__(self, resolutionX = 400, resolutionY = 400, frame_rate = 60):

        self.screen = pygame.display.set_mode([resolutionX, resolutionY])

        self.resolutionX = resolutionX

        self.resolutionY = resolutionY

        self.open = False

        self.objects = []

        self.camera_position = matrix( [ [0], [0], [0] ] )

        self.camera_rotation = matrix( [ [0], [0], [0] ] )

        self.camera_view_plane = matrix ( [ [0], [0], [-1] ] )

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
                
                coords = self.calculate_projection(obj.verticies[i].to_matrix(), obj.transform.scale, obj.transform.position, obj.transform.rotation)

                coord_cache[i] = coords
                
                pygame.draw.circle(self.screen, (0, 0, 255), coords, 1)

            for vertex_index in range(len(obj.verticies)):

                for connection in obj.verticies[vertex_index].joined_to:
                    
                    pygame.draw.line(self.screen, (0, 0, 0), coord_cache[vertex_index], coord_cache[connection], 1)
            
            obj.update()

    def calculate_projection(self, point, scale, position, rotation):

        # reference: https://en.wikipedia.org/wiki/3D_projection#Mathematical_formula

        d = point
        d = renderer.calculate_rotation_matrix(rotation) * d
        d - self.camera_position
        # d = (point - self.camera_position)
        d = renderer.calculate_rotation_matrix(self.camera_rotation) * d
        d = scale * d + position

        screen_space_x = self.camera_view_plane[0][0]
        screen_space_y = self.camera_view_plane[1][0]
        screen_space_z = self.camera_view_plane[2][0]

        f_xyw = matrix(
            [
                [1, 0, screen_space_x / screen_space_z],
                [0, 1, screen_space_y / screen_space_z],
                [0, 0, 1 / screen_space_z]
            ]
        ) * d

        if f_xyw[2][0] != 0:

            x = f_xyw[0][0] / f_xyw[2][0]
            y = f_xyw[1][0] / f_xyw[2][0]

            print((x, y))

            return (self.resolutionX // 2 + int(x), self.resolutionY // 2 + int(y))

        else:

            return (-1, -1)
    
    def calculate_x_rotation_matrix(x_angle):

        return matrix(
            [
                [1, 0, 0],
                [0, cos(x_angle), -sin(x_angle)],
                [0, sin(x_angle), cos(x_angle)]
            ]
        )
    
    def calculate_y_rotation_matrix(y_angle):

        return matrix(
            [
                [cos(y_angle), 0, -sin(y_angle)],
                [0, 1, 0],
                [sin(y_angle), 0, cos(y_angle)]
            ]
        )
    
    def calculate_z_rotation_matrix(z_angle):

        return matrix(
            [
                [cos(z_angle), -sin(z_angle), 0],
                [sin(z_angle), cos(z_angle), 0],
                [0, 0, 1]
            ]
        )
        
    def calculate_rotation_matrix(angles):

        x_angle = angles[0][0]
        y_angle = angles[1][0]
        z_angle = angles[2][0]

        rotation = renderer.calculate_x_rotation_matrix(z_angle) * renderer.calculate_y_rotation_matrix(y_angle) * renderer.calculate_z_rotation_matrix(x_angle)

        return  rotation

if __name__ == "__main__":

    r = renderer()

    r.objects.append(shapes.cuboid(shapes.transform(x=0, y=0, z=-200, scale=30, x_angle=0), 500, 500, 10, y_rotate_rate = 0.1))

    r.show()