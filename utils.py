import numpy as np


def lin_dist(x1, y1, x2, y2):
    return np.linalg.norm([x1-x2, y1-y2])


def find_circle_intersections(x1, y1, r1, x2, y2, r2):
    if x1 == x2 and y1 == y2:
        raise ValueError("same radius")

    # https://math.stackexchange.com/a/1367732
    d = np.linalg.norm([x1-x2, y1-y2])

    if d > r1 + r2:
        raise ValueError("no intersection (outside)")

    if d < np.abs(r1 - r2):
        raise ValueError("no intersection (inside)")

    a = (r1**2 - r2**2) / d**2
    b = (r1**2 + r2**2) / d**2

    xpref = (x1+x2)/2 + a/2*(x2-x1)
    ypref = (y1+y2)/2 + a/2*(y2-y1)
    suf_mult = np.sqrt(2*b-a**2-1)/2

    ix1 = xpref + suf_mult*(y2-y1)
    iy1 = ypref + suf_mult*(x1-x2)

    ix2 = xpref - suf_mult*(y2-y1)
    iy2 = ypref - suf_mult*(x1-x2)

    return ix1, iy1, ix2, iy2


def get_intersection(x1, y1, r1, x2, y2, r2, *, name: str, ymax=None, xmax=None):
    try:
        ix1, iy1, ix2, iy2 = find_circle_intersections(x1, y1, r1, x2, y2, r2)
    except ValueError as e:
        print(f"no intersection at {name} - {e}")
        return

    if xmax is None and ymax is None:
        return ix1, iy1, ix2, iy2

    elif ymax is not None:
        yi = np.argmax([iy1, iy2]) if ymax else np.argmin([iy1, iy2])
        x, y = [ix1, ix2][yi], [iy1, iy2][yi]
    else:
        xi = np.argmax([ix1, ix2]) if xmax else np.argmin([ix1, ix2])
        x, y = [ix1, ix2][xi], [iy1, iy2][xi]

    return x, y
