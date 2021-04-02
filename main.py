from renderer import renderer
import shapes

r = renderer()

r.objects.append(shapes.cuboid(shapes.transform(x=0, y=0, z=-100, scale=10, x_angle=90), 500, 500, 10, x_rotate_rate = 0))
# r.objects.append(shapes.cuboid(50, 50, 10, x=-1000, y=-1000, z=-100, scale=10))

r.show()