import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import numpy as np

from utils import find_circle_intersections

def plot_intersection(x1, y1, r1, x2, y2, r2):
    plt.figure(figsize=(6, 6))
    plt.plot([x1], [y1], 'go')
    plt.plot([x2], [y2], 'bo')
    c1 = plt.Circle((x1, y1), r1, color='g', fill=False)
    c2 = plt.Circle((x2, y2), r2, color='b', fill=False)
    plt.gca().add_patch(c1)
    plt.gca().add_patch(c2)

    try:
        ix1, iy1, ix2, iy2 = find_circle_intersections(x1, y1, r1, x2, y2, r2)
        plt.plot([ix1, ix2], [iy1, iy2], 'ro')
    except ValueError:
        print("no intersection")

    plt.show()


def get_plot_data(pts):
    """
    pts: list of list of (x, y) of joint positions
    """
    all_joints = np.array([j for j in pts]).reshape(-1, 2)
    st_path = np.array([j[0] for j in pts]) # steering path
    ee_path = np.array([j[-1] for j in pts]) # end effector path

    min_x = np.floor(all_joints[:, 0].min()) - 10
    max_x = np.ceil(all_joints[:, 0].max()) + 10
    min_y = np.floor(all_joints[:, 1].min()) - 10
    max_y = np.ceil(all_joints[:, 1].max()) + 10

    return st_path, ee_path, min_x, max_x, min_y, max_y


def plot_leg(ax, o, p, joints, st_path=None, ee_path=None):
    """
    ax: matplotlib axes
    o: (x, y) of origin
    p: (x, y) of the other fixed joint
    joints: list of (x, y) of joint positions
    st_path: list of (x, y) of steering position
    ee_path: list of (x, y) of end effector position
    """

    line_st, =(None,) if st_path is None else ax.plot(st_path[:, 0], st_path[:, 1], 'c-', lw=1)
    line_ee, = (None,) if ee_path is None else ax.plot(ee_path[:, 0], ee_path[:, 1], 'b-')

    (x0, y0), (x13, y13), (x24, y24), (x56, y56), (x78, y78), (x, y) = joints

    line1, = ax.plot([o[0], x0], [o[1], y0], 'c-')
    line2, = ax.plot([x0, x13, p[0]], [y0, y13, p[1]], 'g-', lw=1)
    line3, = ax.plot([x0, x24, p[0]], [y0, y24, p[1]], 'g-', lw=1)
    line4, = ax.plot([x13, x56, p[0]], [y13, y56, p[1]], 'g-', lw=1)
    line5, = ax.plot([x56, x78, x24], [y56, y78, y24], 'g-', lw=1)
    line6, = ax.plot([x78, x, x24], [y78, y, y24], 'g-', lw=1)

    line7, = ax.plot([o[0], p[0], x], [o[1], p[1], y], 'ro', markersize=4)
    line8, = ax.plot([x0], [y0], 'go', markersize=3)

    return line_ee, line_st, line1, line2, line3, line4, line5, line6, line7, line8



def animate(o, p, pts, file='animation.gif'):
    """
    o: (x, y) of origin
    p: (x, y) of the other fixed joint
    pts: list of list of (x, y) of joint positions
    """
    st_path, ee_path, min_x, max_x, min_y, max_y = get_plot_data(pts)

    fig, ax = plt.subplots()

    def animate(i):
        joints = pts[i]

        ax.clear()
        ax.set_xlim(min_x, max_x)
        ax.set_ylim(min_y, max_y)
        ax.set_aspect('equal')

        return plot_leg(ax, o, p, joints, st_path, ee_path)

    anim = FuncAnimation(fig, animate, frames=len(pts), interval=50, blit=True, repeat=True)
    anim.save(file, writer=PillowWriter(fps=15))


if __name__ == "__main__":
    # plot_intersection(2.5, 2.5, 1, 2, 3, 1)
    # plot_intersection(2.5, 2.5, 0.5, 2, 3, 2)
    # plot_intersection(2.5, 2.5, 0.5, 4, 3, 1)
    # plot_intersection(2.5, 2.5, 0.5, 2.5, 2.5, 1)

    import numpy as np
    from beest import calculate_joints, get_holy_numbers

    o, p, links = get_holy_numbers()

    pts = []
    for angle in np.linspace(0, 2*np.pi, 100):
        try:
            pts.append(calculate_joints(o, p, links, angle))
        except ValueError as e:
            print(f"failed at angle {angle} with {e}")
            break
    animate(o, p,pts, 'animation-2.gif')
