from __future__ import annotations

import random
from voronoi import Voronoi
from geometry.point import Point
import pygame
from constants import WIDTH, HEIGHT, DEBUG, TESTPOINTS
from main import draw_diagram

sites = [Point(0, 0), Point(40, 40)] #PASSED
sites = [Point(0, 0), Point(-60, 0), Point(60, 0), Point(90, 0)] #PASSED
sites = [Point(0, -60), Point(0, 60), Point(0, 0), Point(0, 90)] #PASSED
sites = [Point(0, 0), Point(30, 40), Point(60, 80), Point(75, 100)] #PASSED
sites = [Point(0, 0), Point(-30, 40), Point(-60, 80), Point(-75, 100)] #PASSED
sites = [Point(-60, 80), Point(60, 40), Point(0, -20)] #PASSED
sites = [Point(-60, 80), Point(60, 40), Point(0, 0)] #PASSED
sites = [Point(40, 40), Point(-40, 40), Point(0, 0)] #PASSED
sites = [Point(40, 40), Point(-40, 40), Point(100, -100)] #PASSED
sites = [Point(80, 40), Point(-80, 40), Point(0, -10), Point(0, 80)] #PASSED
sites = [Point(40, 40), Point(-40, 40), Point(0, -80), Point(0, 80)] #PASSED
sites = [Point(40, 40), Point(-40, 40), Point(0, 0), Point(0, 80)] #PASSED
sites = [Point(-60, 80), Point(60, 40), Point(0, 0), Point(-10, 100)] #PASSED
sites = [Point(-60, 80), Point(60, 40), Point(0, 0), Point(-10, -200)] #PASSED
sites = [Point(-60, 80), Point(60, 40), Point(0, 0), Point(300, -300), Point(-50, -150)] # PASSED
sites = [Point(-60, 80), Point(60, 40), Point(0, 0), Point(-140, -150)] # PASSED
sites = [Point(60, 40), Point(0, 0), Point(-140, -150)] # PASSED
sites = [Point(0.1, 0.1), Point(-150, 200), Point(150, -200)] # PASSED
sites = [Point(-60, 80), Point(0, 0), Point(300, -300), Point(-50, -150), Point(-150, 200)] # PASSED
sites = [Point(-60, 80), Point(60, 40), Point(0, 0), Point(300, -300), Point(-50, -150), Point(-150, 200)] # PASSED
sites = [Point(-60, 80), Point(60, 40), Point(0, 0), Point(300, -300), Point(-50, -150), Point(-150, 200), Point(-200, -68)] # PASSED
sites = [Point(-448, 65), Point(-140, 81), Point(339, -216), Point(-56, -360), Point(204, 4), Point(210, 295), Point(8, 33)] # PASSED
sites = [Point(167.000, 213.000), Point(479.000, -327.000), Point(497.000, 164.000), Point(226.000, 400.000)] # PASSED
sites = [Point(-18.000, 349.000), Point(-419.000, -34.000), Point(-112.000, -276.000), Point(-419.000, 177.000)]
sites = [Point(269.000, -432.000), Point(-11.000, -218.000), Point(306.000, -490.000), Point(345.000, 440.000)] # PASSED
sites = [Point(276.000, 270.000), Point(-199.000, 395.000), Point(177.000, -318.000), Point(90.000, -6.000)] # PASSED
sites = [Point(149, 326), Point(-166, -129), Point(129, 491), Point(-202, -9), Point(255, -102), Point(-365, 140), Point(409, -114), Point(256, -473)] # PASSED
sites = [Point(116.000, -337.000), Point(-380.000, 423.000), Point(-507.000, 446.000), Point(163.000, 48.000), Point(162.000, 484.000)] # PASSED
sites = [Point(-384.000, -316.000), Point(250.000, -119.000), Point(-506.000, -273.000), Point(463.000, 60.000), Point(285.000, -376.000)] # PASSED
sites = [Point(59.000, -463.000), Point(201.000, 425.000), Point(-231.000, 437.000), Point(447.000, 424.000), Point(493.000, -101.000)] # PASSED
sites = [Point(-428.000, -422.000), Point(58.000, 145.000), Point(-133.000, 356.000), Point(-356.000, 392.000), Point(-22.000, -240.000)] # PASSED
sites = [Point(-413.000, -154.000), Point(70.000, 379.000), Point(83.000, 413.000), Point(-205.000, -43.000), Point(-230.000, 13.000), Point(-86.000, -114.000)] # PASSED
sites = [Point(4.000, -114.000), Point(272.000, -30.000), Point(490.000, 118.000), Point(96.000, 301.000), Point(-303.000, 245.000), Point(-347.000, 219.000), Point(465.000, -3.000), Point(-330.000, -440.000), Point(336.000, -454.000), Point(-434.000, 392.000), Point(393.000, 95.000), Point(-287.000, 370.000), Point(-137.000, -221.000), Point(52.000, -164.000), Point(-17.000, 359.000), Point(463.000, 244.000), Point(119.000, 395.000), Point(-347.000, -222.000), Point(62.000, -330.000), Point(-87.000, 33.000), Point(390.000, -120.000), Point(510.000, 53.000), Point(-149.000, -145.000), Point(34.000, -296.000), Point(403.000, 286.000), Point(48.000, 280.000), Point(367.000, 418.000), Point(349.000, 246.000), Point(8.000, 301.000), Point(446.000, -165.000), Point(170.000, -173.000), Point(29.000, 355.000), Point(-43.000, 441.000), Point(-256.000, 383.000), Point(232.000, -147.000), Point(-275.000, -61.000), Point(350.000, -232.000), Point(107.000, -10.000), Point(395.000, 375.000), Point(-347.000, 180.000), Point(-336.000, -30.000), Point(236.000, -271.000), Point(-310.000, -441.000), Point(208.000, 114.000), Point(193.000, 236.000), Point(-198.000, 236.000), Point(-403.000, -384.000), Point(-136.000, 180.000), Point(77.000, 268.000), Point(-487.000, -129.000)] # PASSED
sites = [Point(301.000, 392.000), Point(342.000, -42.000), Point(280.000, 237.000), Point(-434.000, -288.000), Point(326.000, 23.000), Point(193.000, -404.000)]
sites = [Point(387.000, 102.000), Point(-192.000, -364.000), Point(-43.000, 472.000), Point(272.000, -456.000), Point(215.000, 369.000), Point(325.000, 259.000), Point(385.000, -355.000)] # PASSED
sites = [Point(177.000, 58.000), Point(-179.000, -89.000), Point(-335.000, 421.000), Point(-417.000, -421.000), Point(328.000, -288.000), Point(205.000, 355.000)] # PASSED
sites = [Point(406.000, 66.000), Point(242.000, 9.000), Point(-76.000, -380.000), Point(-84.000, -278.000), Point(-453.000, -220.000), Point(485.000, -12.000), Point(159.000, 165.000), Point(159.000, 165.000), Point(-164.000, 421.000), Point(-199.000, -354.000)] # PASSED
sites = [Point(8.000, 6.000), Point(-343.000, -74.000), Point(-240.000, 217.000), Point(-299.000, 502.000), Point(47.000, -207.000), Point(433.000, -497.000), Point(328.000, -274.000), Point(-280.000, 444.000)] # PASSED
sites = [Point(-382.000, 146.000), Point(-371.000, 205.000), Point(301.000, -143.000), Point(476.000, -399.000), Point(-463.000, -231.000), Point(-410.000, -138.000), Point(438.000, 366.000), Point(-383.000, 184.000), Point(367.000, 294.000), Point(-315.000, -140.000)] # PASSED
sites = [Point(139.000, 62.000), Point(-415.000, -177.000), Point(257.000, -295.000), Point(-435.000, -428.000), Point(-392.000, -168.000), Point(137.000, 31.000), Point(40.000, -413.000), Point(422.000, -179.000), Point(-231.000, 304.000), Point(-50.000, -189.000)] # PASSED
sites = [Point(185.000, 419.000), Point(-319.000, -50.000), Point(246.000, -225.000), Point(-44.000, 323.000), Point(-310.000, -500.000), Point(-336.000, 126.000), Point(-425.000, 185.000), Point(405.000, -313.000), Point(-294.000, -264.000), Point(439.000, 18.000), Point(-326.000, -264.000), Point(-148.000, -299.000), Point(-491.000, 153.000), Point(-431.000, -98.000), Point(-430.000, 474.000)] # PASSED
sites = [Point(-407.000, 423.000), Point(-196.000, -205.000), Point(449.000, 341.000), Point(-300.000, 465.000), Point(-443.000, 190.000), Point(-36.000, 293.000), Point(-108.000, -74.000), Point(475.000, -11.000), Point(459.000, -21.000), Point(-384.000, 320.000), Point(-318.000, 89.000), Point(-211.000, -386.000), Point(-457.000, 504.000), Point(-395.000, -438.000), Point(-502.000, 320.000)] # PASSED
sites = [Point(273.000, -124.000), Point(-199.000, 140.000), Point(-45.000, -15.000), Point(166.000, -356.000), Point(-77.000, -310.000), Point(-483.000, -346.000), Point(-479.000, 502.000), Point(298.000, 119.000), Point(-245.000, -106.000), Point(354.000, 61.000), Point(259.000, -380.000), Point(-474.000, 369.000), Point(45.000, -11.000), Point(378.000, 329.000), Point(315.000, 140.000)]
sites = set(sites)
DEBUG = True
if not DEBUG:
    fail = 0
    for i in range(1, 100000 + 1):

        try:
            sites = set()
            for _ in range(1, 1 + TESTPOINTS):
                x: int = random.randint(-WIDTH//2, WIDTH//2)
                y: int = random.randint(-HEIGHT//2, HEIGHT//2)
                sites.add(Point(x, y))

            voronoi = Voronoi(sites)
            edges = voronoi.voronoi()
        except AssertionError:
            print("ASSERTION")
            print(str(sites).replace("(", "Point("))
            fail += 1
        except RecursionError:
            print("RECURSION")
            print(str(sites).replace("(", "Point("))
            fail += 1
        except Exception as e:
            print("EXCEPTION")
            print(str(sites).replace("(", "Point("))
            fail += 1

        print(f"{i} Failed: {fail}")

else:
    pygame.init()
    pygame.display.set_mode(size=(WIDTH, HEIGHT), vsync=1)

    voronoi = Voronoi(sites)
    voronoi.voronoi()

    while True:
        draw_diagram(voronoi)