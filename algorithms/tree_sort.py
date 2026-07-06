def tree_sort(arr):
    class Node:
        __slots__ = ("val", "idx", "left", "right")
        def __init__(self, val, idx):
            self.val  = val
            self.idx  = idx
            self.left = self.right = None

    def insert(root_box, val, idx):
        if root_box[0] is None:
            root_box[0] = Node(val, idx)
            return
        node = root_box[0]
        while True:
            yield {"type": "compare", "idx": (idx, node.idx)}
            if val < node.val:
                if node.left is None:
                    node.left = Node(val, idx); break
                node = node.left
            else:
                if node.right is None:
                    node.right = Node(val, idx); break
                node = node.right

    root_box = [None]
    for i in range(len(arr)):
        yield from insert(root_box, arr[i], i)

    # iterative in-order traversal → sorted values
    result, stack, cur = [], [], root_box[0]
    while stack or cur:
        while cur:
            stack.append(cur); cur = cur.left
        cur = stack.pop()
        result.append(cur.val)
        cur = cur.right

    for i, v in enumerate(result):
        arr[i] = v
        yield {"type": "overwrite", "idx": i, "val": v}

    yield {"type": "done"}


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from core.engine import run_visualizer
    run_visualizer([("Tree Sort", tree_sort)])
