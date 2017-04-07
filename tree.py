# coding=utf-8


class Tree:
    def __init__(self, num):
        self.left = None
        self.right = None
        self.num = num


# init a tree
def build(n):
    def expand(i):
        if i > n: return None
        node = Tree(i)
        node.left = expand(i*2)
        node.right = expand(i*2+1)
        return node
    return expand(1)


def find_last(root):
    if not root:
        return None
    depth, node = 0, root
    while node.left:
        node = node.left
        depth += 1
    good = node
    l, r = 1 << depth, 1 << (depth+1)
    while l+1 < r:
        m = (l+r) >> 1
        hit = True
        node = root
        for i in range(depth-1, -1, -1):
            if m & (1 << i):
                node = node.right
            else:
                node = node.left
            if not node:
                hit = False
                break
        if hit:
            l = m
            good = node
        else:
            r = m
    return good

if __name__ == '__main__':
    lst = root = build(5345674)
    lst = find_last(root)
    print(lst.num)

