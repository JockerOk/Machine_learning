import random
from math import sqrt, inf, pi, sin, cos

GROUP_FACTOR = 3
PROXIMITY_DISTANCE = 15
POINTS_PER_CLICK = 5
ANGLE_RANGE = [0, 2 * pi]
RADIUS_RANGE = [0, 15]


class Point:
    def __init__(self, x, y, color='black'):
        self.x = x
        self.y = y
        self.color = color

    def __repr__(self):
        return str(self)

    def __iter__(self):
        for i in [self.x, self.y]:
            yield i

    def __str__(self):
        return f'Point({self.x:.2f}, {self.y:.2f})'


def distance(point_a, point_b):
    return sqrt((point_a.x - point_b.x) ** 2 + (point_a.y - point_b.y) ** 2)


def random_color():
    return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]


def color_for_cluster(index, cache_colors):
    if index >= len(cache_colors):
        for i in range(len(cache_colors) - index + 1):
            cache_colors.append(random_color())

    return cache_colors[index]


def dbscan(points_list):
    greens = []
    yellows = []
    boarded = {}
    cache_colors = []

    cache_points = [*points_list]

    for point1 in cache_points:
        neighbour_count = 0
        for point2 in points_list:

            if point1 == point2:
                continue

            if distance(point1, point2) <= PROXIMITY_DISTANCE:
                neighbour_count += 1

        if neighbour_count >= GROUP_FACTOR:
            point1.color = 'green'
            greens.append(point1)

    for green in greens:
        cache_points.remove(green)

    for point1 in cache_points:
        min_dist = inf
        nearest = None

        for point2 in points_list:

            if point1 == point2:
                continue

            if point2.color == 'red':

                if distance(point1, point2) > PROXIMITY_DISTANCE:
                    continue

                current_dist = distance(point1, point2)
                if current_dist <= min_dist:
                    min_dist = current_dist
                    nearest = point2

        if nearest is not None:
            point1.color = 'blue'
            yellows.append(point1)
            boarded.setdefault(nearest, []).append(point1)

    for yellow in yellows:
        cache_points.remove(yellow)

    clusters = []
    while len(greens) > 0:
        cluster = [greens.pop(0)]

        for point1 in cluster:
            for point2 in greens:
                if point1 is point2:
                    continue

                if distance(point1, point2) <= PROXIMITY_DISTANCE:
                    if point2 not in cluster:
                        greens.remove(point2)
                        cluster.append(point2)

        yellows_in_cluster = []
        for green in cluster:
            if green in boarded:
                yellows_in_cluster.extend(boarded[green])
        cluster.extend(yellows_in_cluster)
        clusters.append(cluster)

    for cluster_index, cluster in enumerate(clusters):
        rng_color = color_for_cluster(cluster_index, cache_colors)

        for p in cluster:
            p.color = rng_color


def add_points(x, y, points):
    for i in range(POINTS_PER_CLICK):
        angle = random.uniform(*ANGLE_RANGE)
        radius = random.randint(*RADIUS_RANGE)
        points.append(Point(x + sin(angle) * radius, y + cos(angle) * radius))