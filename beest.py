import numpy as np

from utils import get_intersection, lin_dist


def sanity_check(c, p, links):
    assert len(links) == 11, "must have 11 links"
    max_ext_dist = lin_dist(*c, *p) + links[0]
    assert max_ext_dist < links[1] + links[3], "cannot extend 1 and 3 enough"
    assert max_ext_dist < links[2] + links[4], "cannot extend 2 and 4 enough"

    assert links[3] < links[5] + links[6], "3 must be shorter than 5 + 6"
    assert links[7] < links[9] + links[10], "7 must be shorter than 9 + 10"


def calculate_joints(c, p, links, angle):
    # Refer to `links.png`
    x0, y0 = c[0] + links[0]*np.cos(angle), c[1] + links[0]*np.sin(angle)

    x13, y13 = get_intersection(x0, y0, links[1], p[0], p[1], links[3], name=f"1-3 {angle:.2f}", ymax=True)
    x24, y24 = get_intersection(x0, y0, links[2], p[0], p[1], links[4], name=f"2-4 {angle:.2f}", ymax=False)
    x56, y56 = get_intersection(x13, y13, links[5], p[0], p[1], links[6], name=f"5-6 {angle:.2f}", xmax=False)
    x78, y78 = get_intersection(x56, y56, links[8], x24, y24, links[7], name=f"7-8 {angle:.2f}", xmax=False)
    x, y = get_intersection(x78, y78, links[9], x24, y24, links[10], name=f"9-10 {angle:.2f}", ymax=False)

    if y >= y24:
        raise ValueError(f"y >= y24 at {angle:.2f}")
    if y >= y78:
        raise ValueError(f"y >= y78 at {angle:.2f}")

    return [(x0, y0), (x13, y13), (x24, y24), (x56, y56), (x78, y78), (x, y)]

def get_holy_numbers(origin=(0, 0)):
    # https://www.strandbeest.com/explains - holy numbers
    # also see `links.png`
    a=38; b=41.5; c=39.3; d=40.1; e=55.8; f=39.4
    g=36.7; h=65.7; i=49; j=50; k=61.9; l=7.8; m=15

    p = (origin[0] - a, origin[1] - l)
    links = [m, j, k, b, c, e, d, g, f, h, i]

    return origin, p, links
