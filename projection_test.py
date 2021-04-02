import math
from matrix import matrix

camera_position = matrix(
    [
        [0],
        [0],
        [0]
    ]
)


camera_orientation = matrix(
    [
        [0],
        [0],
        [0]
    ]
)

camera_screen_space = matrix(
    [
        [0],
        [0],
        [-1]
    ]
)

point = matrix(
    [
        [5],
        [5],
        [-10]
    ]
)


x_rotation = camera_orientation[0][0]
y_rotation = camera_orientation[1][0]
z_rotation = camera_orientation[2][0]

x_rotation_matrix = matrix(
    [
        [1, 0, 0],
        [0, math.cos(x_rotation), math.sin(x_rotation)],
        [0, -math.sin(x_rotation), math.cos(x_rotation)]
    ]
)

y_rotation_matrix = matrix(
    [
        [math.cos(y_rotation), 0, -math.sin(y_rotation)],
        [0, 1, 0],
        [math.sin(y_rotation), 0, math.cos(y_rotation)]
    ]
)

z_rotation_matrix = matrix(
    [
        [math.cos(z_rotation), math.sin(z_rotation), 0],
        [-math.sin(z_rotation), math.cos(z_rotation), 0],
        [0, 0, 1]
    ]
)

d = x_rotation_matrix * y_rotation_matrix * z_rotation_matrix * (point - camera_position)

screen_space_x = camera_screen_space[0][0]
screen_space_y = camera_screen_space[1][0]
screen_space_z = camera_screen_space[2][0]

f = matrix(
    [
        [1, 0, screen_space_x / screen_space_z],
        [0, 1, screen_space_y / screen_space_z],
        [0, 0, 1 / screen_space_z]
    ]
) * d

print(f)

if f[2][0] > 0:

    scale = 100

    b_x = f[0][0] / f[2][0] * scale
    b_y = f[1][0] / f[2][0] * scale

    print(int(b_x))
    print(int(b_y))

else:

    print("Object out of frame")