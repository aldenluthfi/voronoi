from __future__ import annotations

from constants import *
from decimal import Decimal as D
from event import CircleEvent, Event
from geometry.point import Point
from geometry.edge import Edge
from geometry.arc import Arc
from math import ceil, floor
import pygame
from voronoi import Voronoi

def getattr(obj: object, name: str) -> object:
    try:
        return obj.__getattribute__(name)
    except AttributeError:
        return None


def process_site(dot: pygame.Rect) -> Point:
    return Point(*Point.center(dot.center))


def draw_diagram(voronoi: Voronoi) -> None:
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
            radius=DOTS_RADIUS
        )

def draw_beachline(sweep_line: pygame.Rect, voronoi: Voronoi, d: D) -> None:
    arc: Arc | None = voronoi.beachline.list.head

    surface: pygame.Surface = pygame.display.get_surface()
    surface.fill('white')

    pygame.draw.rect(
        surface=surface,
        color='red',
        rect=sweep_line
    )

    ev: Event | None = voronoi.next_visible

    for edge in voronoi.edges:
        u, v = Edge.uncenter(edge.to_tuple())
        pygame.draw.line(
            surface=surface,
            color='black',
            start_pos=u,
            end_pos=v
        )

    for site in voronoi.sites:
        if ev and site == ev.point:
            pygame.draw.circle(
                surface=surface,
                color='red',
                center=Point.uncenter(site.to_tuple()),
                radius=DOTS_RADIUS
            )
        else:
            pygame.draw.circle(
                surface=surface,
                color='black',
                center=Point.uncenter(site.to_tuple()),
                radius=DOTS_RADIUS
            )

    while arc:
        arc.update(d)

        if arc.e1 and not arc.e1.border_edge:
            u, v = Edge.uncenter(arc.e1.bound().to_tuple())
            pygame.draw.line(
                surface=surface,
                color='black',
                start_pos=u,
                end_pos=v
            )

        if arc.e2 and not arc.e2.border_edge:
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

            if x == start:
                x = max(arc.e1.b.x, x)
            if x == end - 1:
                x = min(arc.e2.b.x, x)

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

    if ev is not None:
        if isinstance(ev, CircleEvent):
            c = ev.center.to_tuple()
            r = ev.r

            pygame.draw.circle(
                surface=surface,
                color='red',
                center=Point.uncenter(c),
                radius=DOTS_RADIUS
            )

            pygame.draw.circle(
                surface=surface,
                color='black',
                center=Point.uncenter(c),
                radius=float(r),
                width=1
            )

def render_text_box(
        font: pygame.font.Font,
        instructions: list[str]
    ) -> list[pygame.Surface]:

    text_surfaces: list[pygame.Surface] = []
    for line in instructions:
        text_surface = font.render(line, True, (0, 0, 0))
        text_surfaces.append(text_surface)
    return text_surfaces


def draw_tutorial_box(
        surface: pygame.Surface,
        text_surfaces: list[pygame.Surface]
    ) -> pygame.Rect:

    padding: int = 20
    font_height: int = text_surfaces[0].get_height()

    max_width = max(text_surface.get_width() for text_surface in text_surfaces)
    box_width = max_width + padding * 2
    box_height = len(text_surfaces) * (font_height + 5) + padding * 2

    surface_width, surface_height = surface.get_size()
    x = (surface_width - box_width) // 2
    y = (surface_height - box_height) // 2

    box_rect = pygame.Rect(x, y, box_width, box_height)

    pygame.draw.rect(surface, (220, 220, 220), box_rect)
    pygame.draw.rect(surface, (0, 0, 0), box_rect, 1)

    text_y = y + padding
    for text_surface in text_surfaces:
        text_x = x + padding
        surface.blit(text_surface, (text_x, text_y))
        text_y += font_height + 5

    return box_rect


def draw_button(
        surface: pygame.Surface,
        rect: pygame.Rect,
        text: str,
        font: pygame.font.Font,
        bg_color: pygame.Color,
        text_color: pygame.Color
    ) -> None:

    pygame.draw.rect(surface, bg_color, rect)
    pygame.draw.rect(surface, (0, 0, 0), rect, 1)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


def main() -> None:
    global running

    pygame.init()
    pygame.font.init()  # Initialize the font module
    pygame.display.set_mode(size=(WIDTH, HEIGHT), vsync=1)
    pygame.display.set_caption("Voronoi Diagram")

    surface: pygame.Surface = pygame.display.get_surface()
    surface.fill('white')

    dots: list[pygame.Rect] = []

    try:
        with open("points.txt", "r") as inputs:
            inputted_points = inputs.readlines()
        for points in inputted_points:
            point_pair = tuple(int(_) for _ in points.strip()[1:-1].split(","))
            dot = pygame.draw.circle(
                surface=surface,
                color='black',
                center=Point.uncenter(point_pair),
                radius=DOTS_RADIUS
            )
            dots.append(dot)
    except FileNotFoundError as e:
        print("No input file detected.", e)

    sweep_line: pygame.Rect | None = None
    active_dot: pygame.Rect | None = None
    line_pause: bool = False
    line_speed: float = DEFAULT_SPEED
    sites: set[Point] = set()

    ev: Event | None = None
    visible: Event | None = None

    line_y: float = 0

    voronoi: Voronoi | None = None
    show_tutorial: bool = True

    font_size: int = 20
    font: pygame.font.Font = pygame.font.SysFont('Fira Code', font_size)
    instructions: list[str] = [
        "Controls:",
        "Left Click  : Add/Select Site",
        "Right Click : Remove Site",
        "Drag Mouse  : Move Site",
        "K           : Start/Pause Sweep Line",
        "J           : Decrease Sweep Line Speed",
        "L           : Increase Sweep Line Speed",
        "R           : Reset",
        "Q           : Quit",
        "",
        "By default, program will look for points.txt for file inputs.",
        "In the file, define points as tuples, line-separated, without space.",
        "Coordinates are from (-512,-512) to (512,512).",
        "",
        "TUTORIAL WILL NOT SHOW AGAIN IF CLOSED"
    ]

    text_surfaces = render_text_box(font, instructions)

    close_button_size = 30
    close_button_rect = None
    tutorial_box_rect = None

    while running:

        if voronoi is not None and sweep_line is None:
            draw_diagram(voronoi)

        if sweep_line is not None:

            _, y = Point.center(sweep_line.center)

            if voronoi is None:
                voronoi = Voronoi(sites)
                voronoi.voronoi(D(y))
                ev = voronoi.next_event
                visible = voronoi.next_visible

            if ev is not None and y < ev.point.y:
                voronoi = Voronoi(sites)
                voronoi.voronoi(D(y))
                ev = voronoi.next_event
                visible = voronoi.next_visible

            draw_beachline(sweep_line, voronoi, D(y))

        for dot in dots:
            if dot.x > WIDTH or dot.x < 0 or dot.y > HEIGHT or dot.y < 0:
                dots.remove(dot)
            elif voronoi is None:
                pygame.draw.rect(
                    surface=surface,
                    color='black',
                    rect=dot,
                    border_radius=DOTS_RADIUS
                )

        if sweep_line is not None:
            if not line_pause:
                line_y += line_speed
                sweep_line.move_ip(0, line_y - sweep_line.y)

            if line_y > HEIGHT and visible is None:
                sweep_line = None
                line_y = 0

                if voronoi is not None:
                    voronoi = Voronoi(sites)
                    voronoi.voronoi()
                    draw_diagram(voronoi)

        for event in pygame.event.get():

            assert isinstance(event, pygame.event.Event)

            type = getattr(event, 'type')
            button = getattr(event, 'button') or getattr(event, 'buttons')
            key = getattr(event, 'text') or getattr(event, 'key')

            match (type, button, key):
                case (pygame.MOUSEBUTTONDOWN, 1, _):
                    mouse_pos = event.pos
                    close_event = False
                    if show_tutorial:
                        if close_button_rect and close_button_rect.collidepoint(mouse_pos):
                            show_tutorial = False
                            tutorial_box_rect = None
                            close_button_rect = None
                            close_event = True
                        elif tutorial_box_rect and tutorial_box_rect.collidepoint(mouse_pos):
                            break
                    if not show_tutorial:
                        if sweep_line is not None:
                            sweep_line = None
                            line_y = 0

                        for dot in dots:
                            if dot.collidepoint(event.pos):
                                active_dot = dot
                                break
                        else:
                            if not close_event:
                                dot = pygame.draw.circle(
                                    surface=surface,
                                    color='black',
                                    center=event.pos,
                                    radius=DOTS_RADIUS
                                )

                                dots.append(dot)

                            sites = {process_site(dot) for dot in dots if dot}
                            voronoi = Voronoi(sites)
                            voronoi.voronoi()

                case (pygame.MOUSEBUTTONDOWN, 3, _):
                    if sweep_line is not None:
                        sweep_line = None
                        line_y = 0

                    for dot in dots:
                        if dot.collidepoint(event.pos):
                            dots.remove(dot)

                            sites = {process_site(dot) for dot in dots}
                            voronoi = Voronoi(sites)
                            voronoi.voronoi()

                case (pygame.MOUSEMOTION, (1, 0, 0), _):
                    if active_dot is not None:
                        active_dot.move_ip(event.rel)

                        sites = {process_site(dot) for dot in dots}
                        voronoi = Voronoi(sites)
                        voronoi.voronoi()

                case (pygame.MOUSEBUTTONUP, 1, _):
                    active_dot = None

                case (pygame.TEXTINPUT, _, 'j'):
                    line_speed = max(line_speed * 0.5, MIN_SPEED)

                case (pygame.KEYDOWN, _, pygame.K_k):
                    if sweep_line is not None:
                        line_pause = not line_pause
                    elif not show_tutorial:
                        sweep_line = pygame.draw.line(
                            surface=surface,
                            color='red',
                            start_pos=(0, 0),
                            end_pos=(WIDTH, 0),
                            width=1
                        )

                    voronoi = None

                case (pygame.TEXTINPUT, _, 'l'):
                    line_speed = min(line_speed * 2, MAX_SPEED)

                case (pygame.KEYDOWN, _, pygame.K_r):
                    dots = []
                    sites = set()
                    line_y = 0
                    voronoi = None
                    active_dot = None
                    sweep_line = None

                case (pygame.QUIT, _, _) | (pygame.KEYDOWN, _, pygame.K_q):
                    running = False

                case _:
                    pass

        if sweep_line is None and voronoi is None:
            surface.fill('white')

        if show_tutorial:
            tutorial_box_rect = draw_tutorial_box(surface, text_surfaces)

            close_button_rect = pygame.Rect(
                tutorial_box_rect.right - close_button_size - 10,
                tutorial_box_rect.top + 10,
                close_button_size,
                close_button_size
            )

            draw_button(surface,
                        close_button_rect,
                        '×',
                        font,
                        pygame.Color(200, 50, 50),
                        pygame.Color(255, 255, 255)
            )

        else:
            tutorial_box_rect = None
            close_button_rect = None

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    running: bool = True

    while running:
        main()
