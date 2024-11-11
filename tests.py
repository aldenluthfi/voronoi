import random
from voronoi import Voronoi
from geometry.point import Point
import pygame
from constants import WIDTH, HEIGHT
from main import draw_beachline
from decimal import Decimal as D

#sites = [Point(0, 0), Point(40, 40)] #PASSED
#sites = [Point(0, 0), Point(-60, 0), Point(60, 0), Point(90, 0)] #PASSED
#sites = [Point(0, -60), Point(0, 60), Point(0, 0), Point(0, 90)] #PASSED
#sites = [Point(0, 0), Point(30, 40), Point(60, 80), Point(75, 100)] #PASSED
#sites = [Point(0, 0), Point(-30, 40), Point(-60, 80), Point(-75, 100)] #PASSED
#sites = [Point(-60, 80), Point(60, 40), Point(0, -20)] #PASSED
#sites = [Point(-60, 80), Point(60, 40), Point(0, 0)] #PASSED
#sites = [Point(40, 40), Point(-40, 40), Point(0, 0)] #PASSED
#sites = [Point(40, 40), Point(-40, 40), Point(100, -100)] #PASSED
#sites = [Point(80, 40), Point(-80, 40), Point(0, -10), Point(0, 80)] #PASSED
#sites = [Point(40, 40), Point(-40, 40), Point(0, -80), Point(0, 80)] #PASSED
#sites = [Point(40, 40), Point(-40, 40), Point(0, 0), Point(0, 80)] #PASSED
#sites = [Point(-60, 80), Point(60, 40), Point(0, 0), Point(-10, 100)] #PASSED
#sites = [Point(-60, 80), Point(60, 40), Point(0, 0), Point(-10, -200)] #PASSED
#sites = [Point(-60, 80), Point(60, 40), Point(0, 0), Point(300, -300), Point(-50, -150)] # PASSED
#sites = [Point(-60, 80), Point(60, 40), Point(0, 0), Point(-140, -150)] # PASSED
#sites = [Point(60, 40), Point(0, 0), Point(-140, -150)] # PASSED
#sites = [Point(0.1, 0.1), Point(-150, 200), Point(150, -200)] # PASSED
#sites = [Point(-60, 80), Point(0, 0), Point(300, -300), Point(-50, -150), Point(-150, 200)] # PASSED
#sites = [Point(-60, 80), Point(60, 40), Point(0, 0), Point(300, -300), Point(-50, -150), Point(-150, 200)] # PASSED
#sites = [Point(-60, 80), Point(60, 40), Point(0, 0), Point(300, -300), Point(-50, -150), Point(-150, 200), Point(-200, -68)] # PASSED
#sites = [Point(-448, 65), Point(-140, 81), Point(339, -216), Point(-56, -360), Point(204, 4), Point(210, 295), Point(8, 33)] # PASSED
#sites = [Point(149, 326), Point(-166, -129), Point(129, 491), Point(-202, -9), Point(255, -102), Point(-365, 140), Point(409, -114), Point(256, -473)]
sites = [Point(random.randrange(-WIDTH // 2, WIDTH // 2), random.randrange(-HEIGHT // 2, HEIGHT // 2)) for _ in range(100)]
#sites = [Point(449.000, 123.000), Point(-434.000, 171.000), Point(-285.000, -432.000), Point(340.000, 148.000), Point(-200.000, 441.000), Point(-148.000, 213.000), Point(213.000, 249.000), Point(261.000, 341.000), Point(-93.000, 398.000), Point(-305.000, -280.000), Point(-15.000, -177.000), Point(-93.000, 444.000), Point(449.000, 250.000), Point(-394.000, -70.000), Point(-424.000, 129.000), Point(357.000, -397.000), Point(-203.000, 510.000), Point(-144.000, -47.000), Point(9.000, 491.000), Point(-181.000, -500.000), Point(386.000, 132.000), Point(128.000, 318.000), Point(119.000, 279.000), Point(-23.000, 93.000), Point(118.000, -467.000), Point(180.000, 351.000), Point(-502.000, -173.000), Point(254.000, 68.000), Point(-67.000, 297.000), Point(-236.000, -93.000), Point(124.000, 444.000), Point(-179.000, 416.000), Point(-82.000, 294.000), Point(-334.000, -427.000), Point(420.000, -384.000), Point(-22.000, -192.000), Point(389.000, 51.000), Point(-346.000, 381.000), Point(496.000, 184.000), Point(15.000, -178.000), Point(-207.000, -246.000), Point(-89.000, 283.000), Point(-64.000, 344.000), Point(400.000, 197.000), Point(413.000, -372.000), Point(-205.000, 178.000), Point(-23.000, -313.000), Point(-165.000, -339.000), Point(-140.000, 470.000), Point(272.000, -147.000), Point(-92.000, 134.000), Point(449.000, -58.000), Point(6.000, 300.000), Point(510.000, -443.000), Point(-487.000, 445.000), Point(-41.000, 360.000), Point(-501.000, -172.000), Point(177.000, -408.000), Point(179.000, 220.000), Point(-137.000, -225.000), Point(107.000, 84.000), Point(-380.000, 378.000), Point(-430.000, 313.000), Point(402.000, 39.000), Point(-268.000, 202.000), Point(-313.000, -352.000), Point(-450.000, -163.000), Point(473.000, 382.000), Point(482.000, 148.000), Point(-208.000, 223.000), Point(-100.000, 230.000), Point(-53.000, -50.000), Point(386.000, -484.000), Point(-30.000, 495.000), Point(-399.000, 483.000), Point(408.000, 41.000), Point(-330.000, 445.000), Point(98.000, -343.000), Point(-298.000, -82.000), Point(-481.000, 230.000), Point(-200.000, -503.000), Point(229.000, 323.000), Point(-450.000, 362.000), Point(-332.000, -169.000), Point(444.000, 482.000), Point(258.000, -469.000), Point(-72.000, 272.000), Point(-293.000, -497.000), Point(-406.000, 110.000), Point(247.000, 27.000), Point(446.000, 10.000), Point(-207.000, 207.000), Point(466.000, 206.000), Point(-107.000, 246.000), Point(463.000, -152.000), Point(289.000, 509.000), Point(-355.000, 200.000), Point(171.000, -340.000), Point(380.000, -192.000), Point(425.000, -183.000)]
print(str(sites).replace("(", "Point("))

pygame.init()
pygame.display.set_mode(size=(WIDTH, HEIGHT), vsync=1)

voronoi = Voronoi(sites)
edges = voronoi.voronoi()

while True:
    draw_beachline(voronoi, D(-10*HEIGHT))