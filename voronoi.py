from beachline import BeachLine
from decimal import Decimal as D
from event import Event, SiteEvent, CircleEvent
from geometry.point import Point
from geometry.edge import Edge
from queue import PriorityQueue

class Voronoi:
    def __init__(self, sites: list[Point]) -> None:
        self.sites: list[Point] = sites
        self.beachline: BeachLine = BeachLine()
        self._edges: set[Edge] = set()
        self.events: PriorityQueue[Event] = PriorityQueue()
        self.events_out: PriorityQueue[Event] = PriorityQueue()
        self.next_event: Event = None

    @property
    def edges(self) -> set[Edge]:
        return {e for e in self._edges if not (e.border_edge or e.point_edge)}

    @edges.setter
    def edges(self, value: set[Edge]) -> None:
        self._edges = value

    def voronoi(self, y: D = None) -> set[Edge]:
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

        if y is None or self.events_out.empty() or y < min(self.events_out.queue, key=lambda x: x.point.y).point.y:
            self.next_event = None
        else:
            sites = [ev for ev in self.events_out.queue if ev.point.y < y]
            self.next_event = max(sites, key=lambda x: x.point.y)

        return self.edges
