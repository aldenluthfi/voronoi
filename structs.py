from __future__ import annotations

from decimal import Decimal as D
from geometry.arc import Arc
from geometry.point import Point

class DoublyLinkedList:

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def __len__(self) -> int:
        return self.length

    def __str__(self) -> str:
        current = self.head
        index = 0
        result = ""
        while current:
            result += f"{index}: {str(current)}\n"
            current = current.next
            index += 1
        return result

    def insert(self, arc: Arc, pos: Arc | None) -> Arc:

        self.length += 1

        if pos is None:
            arc.next = self.head
            self.head = arc

            if not self.tail:
                self.tail = arc

            if arc.next:
                arc.next.prev = arc

            return arc

        assert isinstance(arc, Arc)
        assert isinstance(pos, Arc)

        arc.prev = pos
        arc.next = pos.next

        if pos.next:
            pos.next.prev = arc

        pos.next = arc

        if pos == self.tail:
            self.tail = arc

        return arc

    def delete(self, arc: Arc) -> Arc:

        self.length -= 1

        assert isinstance(arc, Arc)

        if arc.prev:
            arc.prev.next = arc.next
        if arc.next:
            arc.next.prev = arc.prev
        if arc == self.head:
            self.head = arc.next
        if arc == self.tail:
            self.tail = arc.prev

        return arc

    def search(self, point: Point) -> Arc | None:
        current = self.head

        while current.e2.b.x < point.x:
            current.update(point.y)
            current = current.next

        return current

class AVLTree:
    def __init__(self):
        self.root = None

    def __str__(self) -> str:
        return self.print_inorder(self.root)

    def __repr__(self) -> str:
        return str(self)

    def print_inorder(self, node: Arc | None, prefix: str = "") -> str:
        result = ""

        if node is not None:
            result += self.print_inorder(node.left, prefix)
            result += f"{prefix}{str(node)}\n"
            result += self.print_inorder(node.right, prefix)

        return result

    def print_tree(self, node: Arc | None, lvl: int = 0, pref: str = "") -> str:
        result = ""

        if node is not None:
            result += self.print_tree(node.right, lvl + 1, pref)
            result += "    " * lvl + f"{pref}{str(node)}\n"
            result += self.print_tree(node.left, lvl + 1, pref)

        return result

    def height(self, node: Arc | None) -> int:
        return node.height if node is not None else 0

    def balance(self, node: Arc | None) -> int:
        if node is None:
            return 0

        return self.height(node.left) - self.height(node.right)

    def update_height(self, node: Arc) -> None:
        if node is None:
            return

        left: Arc | None = node.left
        right: Arc | None = node.right

        node.height = 1 + max(self.height(left), self.height(right))

    def rotate_right(self, y: Arc | None) -> Arc:
        assert y is not None

        x = y.left

        assert x is not None

        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)

        return x

    def rotate_left(self, x: Arc | None) -> Arc:
        assert x is not None

        y = x.right

        assert y is not None

        T2 = y.left

        y.left = x
        x.right = T2

        self.update_height(x)
        self.update_height(y)

        return y

    def rebalance(self, node: Arc) -> Arc:
        self.update_height(node)
        balance = self.balance(node)

        if balance > 1:
            if self.balance(node.left) < 0:
                node.left = self.rotate_left(node.left)
            node = self.rotate_right(node)

        elif balance < -1:
            if self.balance(node.right) > 0:
                node.right = self.rotate_right(node.right)
            node = self.rotate_left(node)

        return node

    def min(self, node: Arc) -> Arc:
        current = node
        while current.left:
            current = current.left
        return current

    def insert_arc(self, arc: Arc, node: Arc | None) -> Arc:

        if node is None:
            return arc

        node.update(arc.focus.y)

        if node.left:
            node.left.update(arc.focus.y)
        if node.right:
            node.right.update(arc.focus.y)

        if arc < node:
            node.left = self.insert_arc(arc, node.left)
        else:
            node.right = self.insert_arc(arc, node.right)

        node = self.rebalance(node)

        return node

    def delete_arc(self, arc: Arc, node: Arc | None, y: D) -> Arc | None:
        if node is None:
            return None

        node.update(y)

        if node.left:
            node.left.update(y)
        if node.right:
            node.right.update(y)

        if arc < node:
            node.left = self.delete_arc(arc, node.left, y)
        elif arc > node:
            node.right = self.delete_arc(arc, node.right, y)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp: Arc = self.min(node.right)
            node.right = self.delete_arc(temp, node.right, y)

            temp.left = node.left
            temp.right = node.right
            temp.height = node.height
            node = temp


        node = self.rebalance(node)

        return node

    def search_arc(self, arc: Arc, node: Arc | None) -> Arc | None:
        if node is None:
            return None

        node.update(arc.focus.y)

        if node.left:
            node.left.update(arc.focus.y)
        if node.right:
            node.right.update(arc.focus.y)

        if arc < node:
            return self.search_arc(arc, node.left)
        elif arc > node:
            return self.search_arc(arc, node.right)
        else:
            return node

    def insert(self, arc: Arc) -> None:
        self.root = self.insert_arc(arc, self.root)

    def delete(self, arc: Arc, y: D) -> None:
        self.root = self.delete_arc(arc, self.root, y)

    def search(self, arc: Arc) -> Arc | None:
        return self.search_arc(arc, self.root)