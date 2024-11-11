from constants import *
from decimal import Decimal as D
from geometry.point import Point
from geometry.edge import Edge
from geometry.arc import Arc
from math import ceil, floor
import pygame
import voronoi


def getattr(obj: object, name: str) -> object:
    try:
        return obj.__getattribute__(name)
    except AttributeError:
        return None

def draw_beachline(voronoi: voronoi.Voronoi, d: D) -> None:
    arc: Arc | None = voronoi.beachline.list.head

    surface: pygame.Surface = pygame.display.get_surface()
    surface.fill('white')

    for edge in voronoi.edges:
        u, v = Edge.uncenter(edge.to_tuple())
        pygame.draw.line(
            surface=surface,
            color='black',
            start_pos=u,
            end_pos=v
        )

    for site in voronoi.sites:
        pygame.draw.circle(
            surface=surface,
            color='black',
            center=Point.uncenter(site.to_tuple()),
            radius=5
        )

    while arc:
        arc.update(d)

        if arc.e1:
            u, v = Edge.uncenter(arc.e1.bound().to_tuple())
            pygame.draw.line(
                surface=surface,
                color='black',
                start_pos=u,
                end_pos=v
            )

        if arc.e2:
            u, v = Edge.uncenter(arc.e2.bound().to_tuple())
            pygame.draw.line(
                surface=surface,
                color='black',
                start_pos=u,
                end_pos=v
            )

        start: int = int(floor(max(arc.e1.b.x, -WIDTH)))
        end: int = int(ceil(min(arc.e2.b.x, WIDTH)))

        for x in range(start, end):
            if arc.focus.y != d:
                first: Point = Point(x, arc.f(D(x), d))
                second: Point = Point(x + 1, arc.f(D(x + 1), d))

                edge: Edge = Edge(first, second)

                u, v = Edge.uncenter(edge.to_tuple())

                pygame.draw.line(
                    surface=surface,
                    color='black',
                    start_pos=u,
                    end_pos=v
                )

        arc = arc.next

    pygame.display.flip()

def main() -> None:

    pygame.init()
    pygame.display.set_mode(size=(WIDTH, HEIGHT), vsync=1)
    pygame.display.set_caption("Voronoi Diagram")

    dots: list[pygame.Rect] = []

    sweep_line: pygame.Rect | None = None
    active_dot: pygame.Rect | None = None
    line_pause: bool = False
    line_speed: float = 1

    line_y: float = 0
    running: bool = True

    while running:

        surface: pygame.Surface = pygame.display.get_surface()
        surface.fill('white')

        for dot in dots:
            if dot.x > WIDTH or dot.x < 0 or dot.y > HEIGHT or dot.y < 0:
                dots.remove(dot)
            else:
                pygame.draw.rect(
                    surface=surface,
                    color='black',
                    rect=dot,
                    border_radius=DOTS_RADIUS
                )

        if sweep_line is not None:
            if not line_pause:
                line_y = line_y + line_speed
                sweep_line.move_ip(0, floor(line_y - sweep_line.y))

            pygame.draw.rect(
                surface=surface,
                color='red',
                rect=sweep_line
            )

            if line_y > HEIGHT:
                sweep_line = None
                line_y = 0

        for event in pygame.event.get():

            assert isinstance(event, pygame.event.Event)

            type = getattr(event, 'type')
            button = getattr(event, 'button') or getattr(event, 'buttons')
            key = getattr(event, 'text') or getattr(event, 'key')

            match (type, button, key):
                case (pygame.MOUSEBUTTONDOWN, 1, _):
                    if sweep_line is not None:
                        sweep_line = None
                        line_y = 0

                    for dot in dots:
                        if dot.collidepoint(event.pos):
                            active_dot = dot
                            break
                    else:
                        dot = pygame.draw.circle(
                            surface=surface,
                            color='black',
                            center=event.pos,
                            radius=DOTS_RADIUS
                        )

                        dots.append(dot)

                case (pygame.MOUSEBUTTONDOWN, 3, _):
                    if sweep_line is not None:
                        sweep_line = None
                        line_y = 0

                    for dot in dots:
                        if dot.collidepoint(event.pos):
                            dots.remove(dot)

                case (pygame.MOUSEMOTION, (1, 0, 0), _):
                    if active_dot is not None:
                        active_dot.move_ip(event.rel)

                case (pygame.MOUSEBUTTONUP, 1, _):
                    active_dot = None

                case (pygame.TEXTINPUT, _, 'j'):
                    line_speed = max(line_speed * 0.5, MIN_SPEED)

                case (pygame.KEYDOWN, _, pygame.K_k):
                    if sweep_line is not None:
                        line_pause = not line_pause
                    else:
                        sweep_line = pygame.draw.line(
                            surface=surface,
                            color='red',
                            start_pos=(0, 0),
                            end_pos=(WIDTH, 0),
                            width=2
                        )

                case (pygame.TEXTINPUT, _, 'l'):
                    line_speed = min(line_speed * 2, MAX_SPEED)

                case (pygame.KEYDOWN, _, pygame.K_r):
                    if sweep_line is not None:
                        sweep_line = None
                        line_y = 0

                    dots.clear()

                case (pygame.QUIT, _, _) | (pygame.KEYDOWN, _, pygame.K_q):
                    running = False

                case _:
                    pass

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
