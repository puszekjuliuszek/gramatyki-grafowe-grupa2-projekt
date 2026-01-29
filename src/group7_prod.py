from pathlib import Path
from node import Node
from edge import HyperEdge
from graph import Graph
from visualization import draw
from productions.p0 import P0
from productions.p6 import P6
from productions.p9 import P9

DRAW_DIR = Path(__file__).parent.parent / "draw" / "group7_prod"
DRAW_DIR.mkdir(exist_ok=True)

g = Graph()

# -----------------
# Outer contour (7 nodes)
# -----------------
n1  = Node(12, 3, "n1")
n2  = Node(9, 0, "n2")
n3  = Node(1, 0, "n3")
n4  = Node(0, 2, "n4")
n5 = Node(0, 4, "n5")
n6 = Node(1, 6, "n6")
n7 = Node(9, 6, "n7")

outer = [
    n1, n2, n3, n4, n5, n6, n7
]

for n in outer:
    g.add_node(n)

# outer boundary edges
for i in range(len(outer)):
    g.add_edge(
        HyperEdge(
            (outer[i], outer[(i + 1) % len(outer)]),
            "E",
            r=0
        )
    )

# -----------------
# Inner square (4 nodes)
# -----------------
a = Node(2, 4, "a")
b = Node(5, 4, "b")
c = Node(5, 2, "c")
d = Node(2, 2, "d")

inner = [a, b, c, d]

for n in inner:
    g.add_node(n)

# square edges
g.add_edge(HyperEdge((a, b), "E", r=0))
g.add_edge(HyperEdge((b, c), "E", r=0))
g.add_edge(HyperEdge((c, d), "E", r=0))
g.add_edge(HyperEdge((d, a), "E", r=0))

# -----------------
# Diagonal connections
# -----------------
g.add_edge(HyperEdge((a, n6), "E", r=0))
g.add_edge(HyperEdge((b, n7), "E", r=0))
g.add_edge(HyperEdge((c, n2),  "E", r=0))
g.add_edge(HyperEdge((d, n3),  "E", r=0))

# -----------------
# Central face hyperedges
# -----------------

# Upper quadrilateral
g.add_edge(
    HyperEdge(
        (a, n6, n7, b),
        "Q",
        r=0
    )
)

# Central quadrilateral
g.add_edge(
    HyperEdge(
        (a, b, c, d),
        "S",
        r=0
    )
)

# Lower quadrilateral
g.add_edge(
    HyperEdge(
        (n2, n3, d, c),
        "Q",
        r=0
    )
)

# Pentagon
g.add_edge(
    HyperEdge(
        (n2, c, b, n7, n1),
        "P",
        r=0
    )
)

# Hexagon
g.add_edge(
    HyperEdge(
        (n3, n4, n5, n6, a, d),
        "S",
        r=0
    )
)

# -----------------
# Draw
# -----------------
draw(g, str(DRAW_DIR / "group7_0.png"))

p6 = P6()
p6.apply(g)
draw(g, str(DRAW_DIR / "group7_1.png"))

p0 = P0()
p0_applied = g.apply(p0)
print(f"P0 applied: {p0_applied}")
draw(g, str(DRAW_DIR / "group7_2.png"))
