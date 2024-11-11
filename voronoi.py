from queue import PriorityQueue
from beachline import BeachLine
from geometry.point import Point
from geometry.edge import Edge
from event import Event, SiteEvent, CircleEvent
from main import draw_beachline


class Voronoi:
    def __init__(self, sites: list[Point]) -> None:
        self.sites: list[Point] = sites
        self.beachline: BeachLine = BeachLine()
        self._edges: set[Edge] = set()
        self.events: PriorityQueue[Event] = PriorityQueue()

    @property
    def edges(self) -> set[Edge]:
        return {e for e in self._edges if not (e.border_edge or e.point_edge)}

    @edges.setter
    def edges(self, value: set[Edge]) -> None:
        self._edges = value

    def voronoi(self) -> set[Edge]:
        for site in self.sites:
            self.events.put(SiteEvent(site.y, site.x))

        while not self.events.empty():
            ed: set[Edge] = set()
            ev: list[CircleEvent] = []

            event = self.events.get()
            print(event) # REMOVE

            if isinstance(event, SiteEvent):
                ev = self.beachline.site(event)

            if isinstance(event, CircleEvent):
                ed, ev = self.beachline.circle(event)

                self.edges |= ed

            for e in ev:
                self.events.put(e)

        self.edges |= self.beachline.cleanup()

        return self.edges
