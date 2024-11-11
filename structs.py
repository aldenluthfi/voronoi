from geometry.arc import Arc

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

class AVLTree:
    def __init__(self):
        self.root = None

    def __str__(self) -> str:
        return self.print_tree(self.root)

    def __repr__(self) -> str:
        return str(self)

    def print_tree(self, node: Arc | None, level: int = 0, prefix: str = "N: ") -> str:
        if not node:
            return ""

        result = ""
        result += self.print_tree(node.left, level + 1, "N: ")
        result += prefix + str(node) + "\n"
        result += self.print_tree(node.right, level + 1, "N: ")


        return result

    def height(self, node: Arc | None) -> int:
        return node.height if node is not None else 0

    def balance(self, node: Arc | None) -> int:
        if node is None:
            return 0

        return self.height(node.left) - self.height(node.right)

    def update_height(self, node: Arc) -> None:
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

    def min(self, node: Arc) -> Arc:
        current = node
        while current.left:
            current = current.left
        return current

    def insert_arc(self, arc: Arc, node: Arc | None) -> Arc:

        if node is None:
            return arc

        if arc < node:
            node.left = self.insert_arc(arc, node.left)
        else:
            node.right = self.insert_arc(arc, node.right)

        self.update_height(node)
        balance = self.balance(node)

        if balance > 1 and arc < node.left:
            return self.rotate_right(node)

        if balance < -1 and arc > node.right:
            return self.rotate_left(node)

        if balance > 1 and arc > node.left:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if balance < -1 and arc < node.right:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def delete_arc(self, arc: Arc, node: Arc | None) -> Arc | None:
        if node is None:
            return None

        if arc < node:
            node.left = self.delete_arc(arc, node.left)
        elif arc > node:
            node.right = self.delete_arc(arc, node.right)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp: Arc = self.min(node.right)
            node.right = self.delete_arc(temp, node.right)
            temp.left = node.left
            temp.right = node.right
            node = temp


        self.update_height(node)
        balance = self.balance(node)

        if balance > 1 and self.balance(node.left) >= 0:
            return self.rotate_right(node)

        if balance < -1 and self.balance(node.right) <= 0:
            return self.rotate_left(node)

        if balance > 1 and self.balance(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if balance < -1 and self.balance(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def search_arc(self, arc: Arc, node: Arc | None) -> Arc | None:
        if not node:
            return None

        node.update(arc.focus.y)

        if arc < node:
            return self.search_arc(arc, node.left)
        elif arc > node:
            return self.search_arc(arc, node.right)
        else:
            return node

    def insert(self, arc: Arc) -> None:
        self.root = self.insert_arc(arc, self.root)

    def delete(self, arc: Arc) -> None:
        self.root = self.delete_arc(arc, self.root)

    def search(self, arc: Arc) -> Arc | None:
        return self.search_arc(arc, self.root)