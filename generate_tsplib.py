import math
import tsplib95
import matplotlib.pyplot as plt


TANA = 3.0 / 4
SPEED_FLAT = 2
SPEED_UP = 1
SPEED_DOWN = 4


def pythagoras(x, y):
    return math.sqrt(x ** 2 + y ** 2)


def get_time(point1, point2):
    # this is techinically not the time, but a symetric weight,
    # where the sum of all weights adds to the total time :)
    x1, z1, y1 = point1
    x2, z2, y2 = point2

    if x1 == 0 and z1 == 0:
        if x2 == 0 and z2 == 0:
            return 4030000
        return get_time(point2, get_nearest_coast(point2))
    elif x2 == 0 and z2 == 0:
        return get_time(point1, get_nearest_coast(point1))
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1

    deltad = pythagoras(dx, dz)
    deltah = TANA * deltad  # distance is scalar
    if deltah < abs(dy):  # avoid the fate of being buries alive
        return 4040000  # no go
    deltah = min(deltah, abs(y1 + y2))  # if we hit y=0, we travel on a plane

    # time = distance_flat / speed_flat + distance_up / speed_up + distance_down / speed_down
    # HARD CODED
    time = (deltad / 2.0 + deltah / 6.0)
    return time * 1000 # convert to metres


def generate_matrix(problem, sf=1):
    for i in range(1, problem.dimension + 1):
        for j in range(1, problem.dimension + 1):
            print(int(round(problem.get_weight(i, j) * sf, 0)), end=" ")
        print()


def get_nearest_coast(point):
    min, cpoint = 4020000.0, (28, 0, 0)
    for i in points_on_coast:
        dx = point[0] - i[0]
        dz = point[1] - i[1]
        d = pythagoras(dx, dz)
        if d < min:
            min = d
            cpoint = i
    return cpoint


def print_solution(solution):
    time = 0.0
    plotcoords = []
    for node in range(len(solution)):
        dtime = problem.get_weight(solution[node - 1] + 1, solution[node] + 1)
        time += dtime

        coords1 = problem.node_coords[solution[node - 1] + 1]
        coords2 = problem.node_coords[solution[node] + 1]

        twodcoord = [coords2[0], coords2[1]]
        plotcoords.append(twodcoord)

        print([coords1[0], coords1[1]], "->",
              [coords2[0], coords2[1]], "=",
              dtime)
    print(time)
    coastal_points = [get_nearest_coast(problem.node_coords[solution[-1] + 1]),
                      get_nearest_coast(problem.node_coords[solution[1] + 1])]
    print(coastal_points)
    draw_polygon(plotcoords)
    for i in plotcoords:
        print(i)


def draw_polygon(points):
    points.pop(0)
    xs, ys = zip(*points)  # create lists of x and y values
    plt.figure()
    plt.plot(xs, ys)
    plt.show()

def get_points():
    counter = 1
    for i in points:
        print(counter, i[0], i[1], i[2])
        counter += 1


#############################
# MAIN
#############################

points = [(0, 0, 0.0)] + [(x, z, y * 0.1875) for x in range(0, 28) for z in range(0, 28) for y in range(0, 28) if
                          x ** 2 + z ** 2 + y ** 2 == 734]
points_on_coast = [(x, z, 0) for x in range(0, 30) for z in range(0, 30)
                   if pythagoras(x, z) >= 28]

problem = tsplib95.load("problem.tsp", special=get_time)
solution = [0, 8, 9, 4, 13, 15, 21, 25, 26, 18, 19, 22, 16, 14, 5, 10, 11,
            12, 2, 6, 20, 24, 29, 30, 32, 34, 38, 42, 37, 41, 44, 46, 50, 54,
            53, 49, 56, 58, 60, 59, 57, 55, 51, 45, 47, 52, 48, 43, 39, 40, 36,
            28, 27, 33, 35, 31, 23, 17, 3, 1, 7]  # Solved using generated matrix and solvetsp.py
solution2 = [ 0, 32, 30, 29, 34, 38, 42, 37, 41, 44, 46, 50, 54, 53, 49, 56, 58,
       60, 59, 57, 55, 51, 45, 47, 52, 48, 43, 39, 40, 36, 28, 27, 33, 35,
       31, 23, 17,  3,  1,  7,  8,  9,  4, 13, 15, 21, 25, 26, 18, 19, 22,
       24, 20, 16, 14,  5, 10, 11, 12,  2,  6]
# generate_matrix(problem, 100)
print_solution(solution2)
# print(get_nearest_coast((27, 2, 0)))
# get_points()
