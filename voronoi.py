from __future__ import annotations

from beachline import BeachLine
from decimal import Decimal as D
from constants import HEIGHT, WIDTH
from event import Event, SiteEvent, CircleEvent
from geometry.point import Point
from geometry.edge import Edge
from queue import PriorityQueue

class Voronoi:
    def __init__(self, sites: set[Point]) -> None:
        self.sites: set[Point] = sites
        self.beachline: BeachLine = BeachLine()
        self._edges: set[Edge] = set()
        self.events: PriorityQueue[Event] = PriorityQueue()
        self.events_out: PriorityQueue[Event] = PriorityQueue()
        self.next_event: Event | None = None
        self.next_visible: Event | None = None

    @property
    def edges(self) -> set[Edge]:
        return {e for e in self._edges if not (e.border_edge or e.point_edge)}

    @edges.setter
    def edges(self, value: set[Edge]) -> None:
        self._edges = value

    @staticmethod
    def visible(ev: Event) -> bool:
        cond = True
        x, y = 0, 0

        if isinstance(ev, CircleEvent):
            x, y = ev.center
            cond &= ev.arc.on_beachline

        if isinstance(ev, SiteEvent):
            x, y = ev.point

        cond &= -WIDTH // 2 <= x <= WIDTH // 2
        cond &= -HEIGHT // 2 <= y <= HEIGHT // 2

        return cond

    def validate(self, q: list[Event], y: D, vis: bool=False) -> Event | None:
        for event in q:

            cond: bool = False

            if isinstance(event, CircleEvent):
                cond = event is None or event.point.y < y
            if isinstance(event, SiteEvent):
                cond = event is None or event.point.y < y

            if vis:
                cond &= Voronoi.visible(event)

            if cond:
                return event

    def voronoi(self, y: D | None=None) -> set[Edge]:
        for site in self.sites:
            self.events.put(SiteEvent(site.y, site.x))

        while not self.events.empty():
            ed: set[Edge] = set()
            ev: list[CircleEvent] = []

            event = self.events.get()
            self.events_out.put(event)

            if y is not None and event.point.y < y:
                break

            if isinstance(event, SiteEvent):
                ev = self.beachline.site(event)

            if isinstance(event, CircleEvent):
                ed, ev = self.beachline.circle(event)

                self.edges |= ed

            for e in ev:
                self.events.put(e)

        if y is None:
            self.edges |= self.beachline.cleanup()

        if y is not None:
            self.next_event = self.validate(self.events_out.queue, y)
            self.next_visible = self.validate(self.events_out.queue, y, True)

        return self.edges
