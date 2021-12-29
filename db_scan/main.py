import sys
import pygame

from db_scan.dbscan import add_points, dbscan

FPS = 60

points = []

pygame.init()
FramePerSec = pygame.time.Clock()

HEIGHT = 600
WIDTH = 800
surface = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("DBSCAN")

game_loop = True
while game_loop:
    surface.fill((255, 255, 255))

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        game_loop = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            add_points(*pygame.mouse.get_pos(), points)
            dbscan(points)

    for point in points:
        pygame.draw.circle(surface, point.color, (point.x, point.y), 2)

    pygame.display.update()

pygame.quit()
sys.exit()