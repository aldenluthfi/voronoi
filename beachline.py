from constants import HEIGHT
from decimal import Decimal as D
from structs import AVLTree, DoublyLinkedList
from geometry.edge import Edge
from geometry.arc import Arc
from geometry.point import Point
from event import SiteEvent, CircleEvent
from math import inf

class BeachLine:
    def __init__(self) -> None:
        self.tree: AVLTree = AVLTree()
        self.list: DoublyLinkedList = DoublyLinkedList()

    def insert_arc(self, arc: Arc, pos: Arc | None) -> Arc:
        self.list.insert(arc, pos)
        self.tree.insert(arc)
        arc.on_beachline = True

        return arc

    def delete_arc(self, arc: Arc) -> Arc:
        self.list.delete(arc)
        self.tree.delete(arc)
        arc.on_beachline = False

        return arc

    def cleanup(self) -> set[Edge]:
        edges: set[Edge] = set()

        arc: Arc | None = self.list.head

        while arc:
            arc.update(D(-10*HEIGHT))
            edges |= {arc.e1.extend(), arc.e2.extend()}

            arc = arc.next

        return edges

    def site(self, event: SiteEvent) -> list[CircleEvent]:
        events: list[CircleEvent] = []

        _, y = event.point

        if self.tree.root is None and len(self.list) == 0:
            e1 = Edge(Point(-inf, inf), Point(-inf, inf))
            e2 = Edge(Point(inf, inf), Point(inf, inf))
            arc: Arc = Arc(event.point, e1, e2)

            self.insert_arc(arc, self.list.head)

            return events

        a0: Arc | None = self.tree.search(Arc.dummy(event.point))

        assert a0 is not None

        if a0.focus.y == y:
            a1: Arc = Arc.dummy(event.point)
            intersection: Point | None = Arc.intersect(a0, a1, y)

            assert intersection is not None

            a1.e1 = Edge(intersection, intersection)
            a1.e2 = a0.e2
            a0.e2 = a1.e1

            self.insert_arc(a1, a0)

            return events

        a1: Arc = Arc.dummy(event.point)
        a2: Arc = Arc.dummy(a0.focus)

        intersection: Point | None = Arc.intersect(a0, a1, y)

        assert intersection is not None

        a2.e2 = a0.e2
        a0.e2 = Edge(intersection, intersection)
        a1.e2 = Edge(intersection, intersection)
        a1.e1 = a0.e2
        a2.e1 = a1.e2

        self.insert_arc(a1, a0)
        self.insert_arc(a2, a1)

        if ev := self.update_arc_event(a0, event.point):
            events.append(ev)
        if ev := self.update_arc_event(a2, event.point):
            events.append(ev)

        return events

    def circle(self, event: CircleEvent) -> tuple[set[Edge], list[CircleEvent]]:
        edges: set[Edge] = set()
        events: list[CircleEvent] = []

        if not event.arc.on_beachline:
            return edges, events

        assert event.arc.prev is not None
        assert event.arc.next is not None

        arc = event.arc

        a0: Arc = event.arc.prev
        a1: Arc = event.arc.next

        self.delete_arc(arc)

        arc.e1.b = event.center
        arc.e2.b = event.center

        arc.e1.finished = True
        arc.e2.finished = True

        edges |= {arc.e1.bound(), arc.e2.bound()}

        new_edge: Edge = Edge(event.center, event.center)

        a0.e2 = new_edge
        a1.e1 = new_edge

        if ev := self.update_arc_event(a0, event.point):
            events.append(ev)
        if ev := self.update_arc_event(a1, event.point):
            events.append(ev)

        return edges, events

    def update_arc_event(self, arc: Arc, point: Point) -> CircleEvent | None:

        if arc.prev is None or arc.next is None:
            return

        o, r = Point.empty_circle(arc.prev.focus, arc.focus, arc.next.focus)

        if o is not None and o.y - r <= point.y:
            return CircleEvent(o.y - r, o, arc)



