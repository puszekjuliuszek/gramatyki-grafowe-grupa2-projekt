from pathlib import Path
from node import Node
from edge import HyperEdge
from graph import Graph
from visualization import draw
from productions.p0 import P0
from productions.p1 import P1
from productions.p2 import P2
from productions.p3 import P3
from productions.p4 import P4
from productions.p5 import P5
from productions.p6 import P6
from productions.p7 import P7
from productions.p8 import P8

DRAW_DIR = Path(__file__).parent.parent / "draw" / "group7_prod"
DRAW_DIR.mkdir(exist_ok=True)
DRAW_PREFIX = "step"

def draw_step(graph: Graph, step: str) -> None:
    draw(graph, str(DRAW_DIR / f"{DRAW_PREFIX}_{step}.png"))

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
            r=0,
            b=1
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

# Graf początkowy
draw_step(g, "0")

# Oznacz pięciokąt do rozbicia
p6 = P6()
p6_applied = p6.apply(g)
print(f"P6 applied: {p6_applied}")
draw_step(g, "1")

# Oznacz dolny czworokąt do rozbicia
# TODO: to musi się aplikować deterministycznie do dolnego czworokąta, nie do górnego
p0 = P0()
p0_applied = g.apply(p0)
print(f"P0 applied: {p0_applied}")
draw_step(g, "2")

# Oznacz krawedzie pięciokąta do rozbicia
p7 = P7()
p7_applied = g.apply(p7)
print(f"P7 applied: {p7_applied}")
draw_step(g, "3")

# Złam krawędzie na brzegach (dopóki się da)
i = 0
p4_applied = True
while p4_applied:
    p4 = P4()
    p4_applied = g.apply(p4)
    print(f"P4 applied: {p4_applied}")

    if not p4_applied:
        break
    draw_step(g, f"4_{i+1}")
    i += 1

# Złam krawędzie wewnętrzne (dopóki się da)
# TODO: łamanie krawędzie powoduje powstanie nowego wierzchołka na istniejącej krawędzi, co jest nieczytelne; poprawić to jakoś
i = 0
p3_applied = True
while p3_applied:
    p3 = P3()
    p3_applied = g.apply(p3)
    print(f"P3 applied: {p3_applied}")

    if not p3_applied:
        break
    draw_step(g, f"5_{i+1}")
    i += 1

# Złam pięciokąt
p8 = P8()
p8_applied = g.apply(p8)
print(f"P8 applied: {p8_applied}")
draw_step(g, "6")

# Zaznacz krawędzie czworokąta do złamania
p1 = P1()
p1_applied = g.apply(p1)
print(f"P1 applied: {p1_applied}")
draw_step(g, "7")

# Złam krawędź brzegową czworokąta
p4 = P4()
p4_applied = g.apply(p4)
print(f"P4 applied: {p4_applied}")
draw_step(g, "8")

# Złam krawędź, jeśli krawedź została już złamany przez sąsiednią figurę
p2 = P2()
p2_applied = p2.apply(g)
print(f"P2 applied: {p2_applied}")
draw_step(g, "9")

# Złam krawędzie wewnętrzne (dopóki się da)
i = 0
p3_applied = True
while p3_applied:
    p3 = P3()
    p3_applied = g.apply(p3)
    print(f"P3 applied: {p3_applied}")

    if not p3_applied:
        break
    draw_step(g, f"10_{i+1}")
    i += 1

# Złam czworokąt oznaczony do złamania
p5 = P5()
p5_applied = g.apply(p5)
print(f"P5 applied: {p5_applied}")
draw_step(g, "11")

# Oznacz dwa czworokąty przy naszym "punkcie do którego łamiemy" do złamania
# TODO: jakoś to zrobić deterministycznie, a nie losowo; no i żeby to były te dwa właściwe czworokąty
p0 = P0()
p0_applied_1 = g.apply(p0)
print(f"P0 applied (1): {p0_applied_1}")
draw_step(g, "12_1")
p0_applied_2 = g.apply(p0)
print(f"P0 applied (2): {p0_applied_2}")
draw_step(g, "12_2")

# Co będzie w pętli (mam nadzieję, że dobrze zrozumiałem zadanie i się nie machnąłem, więc mnie sprawdźcie):
## Zaznacz oba czworokąty przy "punkcie, do którego łamiemy" do złamania (P0)
## Zaznacz krawędzie jednego oznaczonego czworokąta do złamania (P1)
## Złam krawędzie brzegowe (P4)
## Złam krawędzie wewnętrzne niezłamane przez figury sąsiednie (P3)
## Złam czworokąt (P5)
## Zaznacz krawędzie drugiego oznaczonego czworokąta do złamania (P1)
## Złam krawędzie brzegowe (P4)
## Złam krawędzie wspólne (P2)
## Złam krawędzie wewnętrzne niezłamane przez figury sąsiednie (P3)
## Złam czworokąt (P5)
## I tak w koło Macieju (to, ile razy ta pętla się obróci, możemy zadać np. parametrem na początku skryptu)
