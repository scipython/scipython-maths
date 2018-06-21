import sys
import math

# Create SVG images of Reuleaux polygons, as described at
# https://scipython.com/blog/constructing-reuleaux-polygons/
# Christian Hill, June 2018.

# Image size (pixels)
SIZE = 600

def draw_poly(n, a, phi=0, show_centres=False, colour='#888',
              filename='reuleaux.svg'):
    """Draw a Reuleaux polygon with n vertices.

    a is the side-length of the straight-sided inscribed polygon, phi is the
    phase, describing the rotation of the polygon as depicted. If show_centres
    is True, markers are placed at the centres of the constructing circles.
    colour is the fill colour of the polygon and filename the name of the SVG
    file created. Note that n must be odd.

    """

    if not n % 2:
        sys.exit('Error in draw_poly: n must be odd')

    fo = open(filename, 'w')
    # The SVG preamble and styles.
    print('<?xml version="1.0" encoding="utf-8"?>\n'

    '<svg xmlns="http://www.w3.org/2000/svg"\n' + ' '*5 +
         'xmlns:xlink="http://www.w3.org/1999/xlink" width="{}" height="{}" >'
            .format(SIZE, SIZE), file=fo)
    print("""
    <defs>
    <style type="text/css"><![CDATA[

    circle {
        stroke-width: 2px;
        stroke: #000;
        fill: none;
    }
    .marker { stroke-width: 0; fill: #000;}
    .circle {stroke: #888;}

    path {
        stroke-width: 4px;
        stroke: #000;
        fill: %s;
    }

    ]]></style>
    </defs>
    """ % colour, file=fo)

    c0x = c0y = SIZE // 2
    # Calculate the radius of each of the constructing circles.
    alpha = math.pi * (1 - 1/n)
    r = a / 2 / math.sin(alpha/2)

    if show_centres:
        print('<circle cx="{}" cy="{}" r="3" class="marker"/>'.format(c0x, c0y),
            file=fo)

    # Caclulate the (x, y) positions of the polygon's vertices.
    v = []
    for i in range(n):
        # The centre, (cx, cy), of this constructing circle.
        cx = c0x + r * math.cos(2*i*math.pi/n + phi)
        cy = c0y + r * math.sin(2*i*math.pi/n + phi)
        v.append((cx, cy))
        if show_centres:
            print('<circle cx="{}" cy="{}" r="5" class="marker"/>'
                .format(cx, cy), file=fo)
        print('<circle cx="{}" cy="{}" r="{}" class="circle"/>'.format(
            cx, cy, a), file=fo)

    def make_A(x,y):
        """Return the SVG arc path designation for the side ending at (x,y)."""

        return 'A {},{},0,0,1,{},{}'.format(a,a,x,y)

    d = 'M {},{}'.format(v[0][0], v[0][1])
    for i in range(n):
        x, y = v[(i+1)%n]
        d += ' ' + make_A(x, y)
    print('<path d="{}"/>'.format(d), file=fo)

    print('</svg>', file=fo)
    fo.close()

draw_poly(3, 175, colour='#eea', filename='reuleaux-3.svg')
draw_poly(5, 175, math.pi/3, filename='reuleaux-5.svg')
draw_poly(11, 175, colour='#aee', filename='reuleaux-11.svg')
