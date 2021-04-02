from renderer import renderer
import shapes

r = renderer(resolutionX=800, resolutionY=800)

my_transform = shapes.transform(z=-10, x_scale=1, y_scale=5, z_scale=1, y_angle=0)
my_shape = shapes.cuboid(my_transform)
r.objects.append(my_shape) # Cuboid

my_transform = shapes.transform(x=-10, z=-20, x_scale=1, y_scale=1, z_scale=1, y_angle=0)
my_shape = shapes.cuboid(my_transform, x_rotate_rate = 0, y_rotate_rate = 0, z_rotate_rate = 1)
r.objects.append(my_shape) # Cube

r.show()